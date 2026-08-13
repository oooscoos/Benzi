"""
harness.py -- controlled A/B: does Benzi's resolved index help an LLM?

ONE variable. Both arms are the same Claude Code binary, same model, same task,
same repo state, same permissions. The only difference is whether Benzi's index
is mounted as an MCP server:

    control    claude -p <task>
    benzi      claude -p <task> --mcp-config <benzi> --strict-mcp-config

Whatever delta shows up is attributable to the index rather than to a different
agent scaffold -- which is what makes the number defensible.

TASK SHAPE (SWE-bench): check out a real bug-FIX commit (so its new tests are
present), then revert only the SOURCE half. That leaves buggy code + the tests
that catch it. Grading is differential against a per-task baseline, because a
repo can have tests that already fail in this environment (sqlglot has one, a
zoneinfo issue) and those must never be counted against an arm:

    fail_to_pass -- failed with the bug present, must pass after the agent works
    pass_to_pass -- passed at baseline, must STILL pass (catches "fixed it by
                    breaking something else", which a naive grader rewards)

Usage:
    python harness.py --task sqlglot_7920 --arms control benzi --trials 3
    python harness.py --task sqlglot_7920 --prompt-tax     # measure MCP overhead
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import platform
import re
import shutil
import stat
import subprocess
import time
from datetime import datetime
from pathlib import Path

BENCH = Path(__file__).resolve().parent


def _find_claude_binary() -> Path:
    """The VS Code extension auto-updates and its version number is baked
    into the install path -- a hardcoded version goes stale the next time
    the extension updates (it did: 2.1.216 -> 2.1.217 between one session
    and the next, silently failing every arm with a WinError 2 before any
    API call, so at least that failure mode is free). Glob for whichever
    version is actually installed instead of pinning one."""
    ext_root = Path(os.environ.get("VSCODE_EXTENSIONS",
                                   Path.home() / ".vscode" / "extensions"))
    candidates = sorted(ext_root.glob("anthropic.claude-code-*-win32-x64"))
    for c in reversed(candidates):   # newest (lexicographically last) first
        exe = c / "resources" / "native-binary" / "claude.exe"
        if exe.exists():
            return exe
    raise RuntimeError(f"no claude.exe found under {ext_root} -- is the VS Code "
                       "extension installed?")


CLAUDE = _find_claude_binary()
# Where Benzi itself lives, and which interpreter runs it. Point BENZI_HOME at
# your checkout; BENZI_PY defaults to the interpreter running this harness,
# which is right unless Benzi needs its own virtualenv.
BENZI_HOME = Path(os.environ.get("BENZI_HOME", Path(__file__).resolve().parent.parent))
BENZI_MCP = BENZI_HOME / "benzi_mcp.py"
BENZI_HEADLESS = BENZI_HOME / "benzi_headless.py"
BENZI_PY = Path(os.environ.get("BENZI_PY", sys.executable))
RESULTS = BENCH / "results"

# Portable toolchains (installed under bench/tools, no admin). Globbed so a
# version bump doesn't hardcode-rot the path. Java tasks build+test via Maven;
# C++ tasks via CMake+Ninja+GCC. Python tasks use each repo's own .venv.
_TOOLS = BENCH / "tools"
JDK_HOME = next(iter(_TOOLS.glob("jdk/jdk-*")), None)
MAVEN_BIN = next(iter(_TOOLS.glob("maven/apache-maven-*/bin")), None)
CMAKE_BIN = next(iter(_TOOLS.glob("cmake/*/bin")), None)
NINJA_DIR = _TOOLS / "ninja"
GCC_BIN = _TOOLS / "gcc" / "mingw64" / "bin"
RUST_HOME = _TOOLS / "rust"                       # rustup + cargo (gnu target, links via GCC_BIN)


def _lang_env(lang: str) -> dict | None:
    """os.environ plus whatever the language's toolchain needs on PATH. None for
    Python (the repo venv is invoked by absolute path, no env change needed)."""
    if lang == "java":
        env = dict(os.environ)
        env["JAVA_HOME"] = str(JDK_HOME)
        env["PATH"] = f"{JDK_HOME}\\bin{os.pathsep}{MAVEN_BIN}{os.pathsep}" + env["PATH"]
        return env
    if lang in ("cpp", "c"):
        env = dict(os.environ)
        # ccache SHIM (ccache copied as gcc/g++) goes FIRST on PATH; the real GCC_BIN
        # sits behind it, so ccache-as-g++ finds the real g++ to run + caches its .o
        # by content hash. Covers cmake's build, the agent's own shell builds, and the
        # semantic gate alike -- and CCACHE_DIR is persistent, outside the dropped
        # worktree, so an edit recompiles only the changed file, the rest cache-hit.
        # Shared with plain C (cJSON): same CMake+GCC toolchain, no separate install.
        shim = _TOOLS / "ccache-shim"
        env["PATH"] = f"{shim}{os.pathsep}{GCC_BIN}{os.pathsep}{CMAKE_BIN}{os.pathsep}{NINJA_DIR}{os.pathsep}" + env["PATH"]
        env["CC"] = str(shim / "gcc.exe")
        env["CXX"] = str(shim / "g++.exe")
        env["CCACHE_DIR"] = str(BENCH / ".ccache")
        return env
    if lang == "go":
        env = dict(os.environ)
        env["GOROOT"] = str(_TOOLS / "go")
        env["PATH"] = f"{_TOOLS}\\go\\bin{os.pathsep}" + env["PATH"]
        # Persistent build/module cache OUTSIDE the (per-run, dropped) worktree --
        # same reasoning as CARGO_TARGET_DIR/CCACHE_DIR: a fresh worktree shouldn't
        # pay a cold compile of the same stdlib packages every run.
        env["GOCACHE"] = str(BENCH / ".gocache")
        env["GOPATH"] = str(BENCH / ".gopath")
        return env
    if lang == "ruby":
        env = dict(os.environ)
        # ucrt64/bin (gcc/make, for native-extension gems) + usr/bin (sh, needed
        # by extconf.rb-driven builds) from the embedded MSYS2 -- same layout
        # RubyInstaller's own DevKit variant ships, just installed after the
        # fact since the base install came without it.
        msys = _TOOLS / "ruby" / "msys64"
        env["PATH"] = (f"{_TOOLS}\\ruby\\bin{os.pathsep}{msys}\\ucrt64\\bin{os.pathsep}"
                       f"{msys}\\usr\\bin{os.pathsep}" + env["PATH"])
        # Gems installed once into a shared, persistent path (like NuGet's global
        # cache for csharp) -- bundler reuses it across worktrees instead of a
        # fresh `bundle install` per run.
        env["GEM_HOME"] = str(BENCH / ".gems")
        env["BUNDLE_PATH"] = str(BENCH / ".gems")
        # addressable's own opt-out for idn-ruby (a native libidn wrapper it
        # otherwise pulls in) -- the project provides this exact env var for
        # environments without that native dep, which is us.
        env["IDNA_MODE"] = "pure"
        # GCC 14+ (ours is 16.x) promotes a legacy Ruby C-extension pattern --
        # rb_define_method's 3rd arg expects VALUE(*)(ANYARGS) but old gems
        # (strscan included, an official stdlib-bundled gem) declare their
        # method funcs as VALUE(*)(VALUE) -- from a warning to a hard error
        # (-Wincompatible-pointer-types). Harmless on this calling convention
        # in practice; downgrading it back to a warning is the standard,
        # well-documented fix for compiling older native gems on a modern
        # MinGW GCC, so it's set globally here rather than per-gem.
        env["RUBY_CFLAGS"] = "-Wno-incompatible-pointer-types"
        env["CFLAGS"] = "-Wno-incompatible-pointer-types"
        return env
    if lang == "rust":
        env = dict(os.environ)
        env["RUSTUP_HOME"] = str(RUST_HOME / "rustup")
        env["CARGO_HOME"] = str(RUST_HOME / "cargo")
        # cargo/rustc on PATH + GCC for the gnu-target linker.
        env["PATH"] = f"{RUST_HOME}\\cargo\\bin{os.pathsep}{GCC_BIN}{os.pathsep}" + env["PATH"]
        # PERSISTENT target dir OUTSIDE the (per-run, dropped) worktree -- so cargo
        # compiles the crate's deps once and reuses them across runs instead of a
        # full cold rebuild every fresh worktree.
        env["CARGO_TARGET_DIR"] = str(BENCH / ".cargo-target")
        return env
    if lang == "csharp":
        env = dict(os.environ)
        env["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
        env["DOTNET_NOLOGO"] = "1"
        env["DOTNET_SKIP_FIRST_TIME_EXPERIENCE"] = "1"
        # NuGet restores to the global ~/.nuget cache (shared across worktrees), so
        # only the first run pays for restore -- no per-worktree install.
        return env
    if lang in ("javascript", "typescript"):
        # node + npm are on the machine PATH; node_modules is junctioned into each
        # worktree by make_worktree (installed once in the base repo, like .venv).
        # TypeScript compilation/typecheck happens INSIDE jest via ts-jest -- no
        # separate tsc invocation needed, so this needs nothing extra over JS.
        return dict(os.environ)
    return None

# A task is a real fix commit + which files were the SOURCE half + how to grade.
# `issue` is what the agent is told: a realistic bug report that does NOT name the
# file or the test, so finding them is part of the work being measured.
TASKS = {
    "sqlglot_7920": {
        "repo": "sqlglot",
        "fix": "c368c5eb2d",
        "parent": "c4020942",
        "source_files": ["sqlglot/generators/duckdb.py"],
        "target_tests": "tests/dialects/test_bigquery.py",
        "regression_tests": "tests/dialects",
        "issue": (
            "Transpiling BigQuery's ARRAY_CONCAT_AGG to DuckDB produces wrong SQL when "
            "the aggregate has an ORDER BY or a LIMIT inside it. For example "
            "`SELECT ARRAY_CONCAT_AGG(arr ORDER BY y) FROM ...` and "
            "`SELECT ARRAY_CONCAT_AGG(arr LIMIT 2) FROM ...` do not round-trip correctly "
            "to the duckdb dialect. LIMIT inside ARRAY_CONCAT_AGG has no DuckDB "
            "equivalent and should be reported as unsupported rather than silently "
            "mistranslated. Please fix the transpilation and make sure the existing "
            "test suite still passes."
        ),
    },
    "scrapy_proxy_auth_leak": {
        "repo": "scrapy",
        "fix": "fada8be1db6479e235d7e06afa057632dbc2adf1",
        "parent": "b7824db573ca5a50890024f3e2e63c714a62aa20",
        "source_files": [
            "scrapy/core/downloader/handlers/_base_streaming.py",
            "scrapy/core/downloader/handlers/_httpx.py",
        ],
        "target_tests": "tests/test_downloader_handler_httpx.py::TestMitmProxy::test_proxy_redirect",
        "regression_tests": "tests/test_downloader_handler_httpx.py::TestMitmProxy",
        "issue": (
            "BaseStreamingDownloadHandler extracts proxy credentials from the "
            "request by popping the Proxy-Authorization header off of "
            "request.headers, which mutates the shared Request object in "
            "place. When a request is redirected, Scrapy builds the new "
            "request from the original's headers -- but the header is "
            "already gone by then, so the redirected request goes out "
            "through the proxy with no Proxy-Authorization at all and the "
            "proxy rejects it. Fix proxy credential extraction so it reads "
            "the header without mutating the request, while still making "
            "sure Proxy-Authorization is never forwarded to the destination "
            "server itself, and keep the existing proxy test suite passing."
        ),
    },
    "fmt_4839": {
        "repo": "fmt",
        "lang": "cpp",
        "fix": "7852fc384ce4232284fc685f66f70ed99b0c2cd4",
        "parent": "d45179c1e7092c6b0d46e4f400fa537377623398",
        "source_files": ["include/fmt/format.h"],
        "cmake_opts": ["-DFMT_TEST=ON"],
        "target_tests": "format-test",
        "regression_tests": "format-test",   # a header edit recompiles this binary; narrower than a full sweep
        "issue": (
            "fmt mishandles out-of-range integers formatted with the 'c' presentation "
            "type. `fmt::format(\"{:c}\", 256)`, a negative value like "
            "`fmt::format(\"{:c}\", -1)`, and other values outside a single character's "
            "range are silently mistranslated instead of being rejected. The 'c' type "
            "treats character values as unsigned, so the representable range is [0, 255]; "
            "anything outside it (negative, or > 255) should raise a clear "
            "\"character value out of range\" error, while in-range values (e.g. 200, 255) "
            "must still format to the corresponding character. Please fix it and keep the "
            "existing test suite passing."
        ),
    },
    "yamlcpp_base64": {
        "repo": "yaml-cpp",
        "lang": "cpp",
        "fix": "80ea0028c7ba35e6a267e1778eab78a3ee82e8b9",
        "parent": "2e6383d272f676e1ad28ae5c47016045cbaff938",
        "source_files": ["src/binary.cpp"],
        "cmake_opts": ["-DYAML_CPP_BUILD_TESTS=ON"],
        "target_tests": "yaml-cpp-tests",
        "regression_tests": "yaml-cpp-tests",
        "issue": (
            "yaml-cpp's base64 decoder (YAML::DecodeBase64) does not reject malformed input. "
            "A base64 string whose length is not a valid multiple (i.e. truncated -- leftover "
            "characters that don't complete a 4-character group) should be treated as invalid "
            "and decode to an EMPTY result, but instead it silently decodes the partial input "
            "and returns garbage bytes. Make DecodeBase64 return an empty vector when the input "
            "is truncated / has an invalid number of base64 characters, and keep valid base64 "
            "decoding correct. Keep the existing test suite passing."
        ),
    },
    "commonscli_npe": {
        "repo": "commons-cli",
        "lang": "java",
        "fix": "57c08d0d16e0de5920d7211cf1c888397f71f558",
        "parent": "4384414639a7c49060a6d489368a4bea00484313",
        "source_files": ["src/main/java/org/apache/commons/cli/CommandLine.java"],
        "target_tests": "BugsTest",
        "regression_tests": "",   # empty => run the whole suite (see run_maven)
        "issue": (
            "commons-cli throws a NullPointerException when an option name of null is "
            "passed to CommandLine's option lookup. For example "
            "`commandLine.getOptionValue((String) null, \"default\")` should return the "
            "supplied default (\"default\"), and `commandLine.getOptionValue((String) null, "
            "null)` should return null -- but instead a null option name blows up with an NPE "
            "while resolving the option. Make a null option name resolve to no option "
            "(returning null / the default) rather than throwing, and keep the existing "
            "test suite passing."
        ),
    },
    "semver_prerelease": {
        "repo": "semver",
        "lang": "rust",
        "fix": "5742fc2f584dc14b46199d797de65305fe9b5144",
        "parent": "5742fc2f584dc14b46199d797de65305fe9b5144^",
        "source_files": ["src/eval.rs"],
        "target_tests": "",
        "regression_tests": "",
        # The real fix commit changed only src/eval.rs (no test), so we inject the
        # pinning test -- it fails on the buggy comparator eval, passes once fixed.
        "inject_files": {
            "tests/bench_less_pre.rs": (
                "use semver::{Version, VersionReq};\n\n"
                "#[test]\n"
                "fn less_than_excludes_boundary_prerelease() {\n"
                "    // `>=1.2.0-0` opts this requirement into 1.2.0 prereleases; the `<1.2`\n"
                "    // bound must still EXCLUDE every 1.2.0 prerelease.\n"
                "    let req = VersionReq::parse(\">=1.2.0-0, <1.2\").unwrap();\n"
                "    assert!(\n"
                "        !req.matches(&Version::parse(\"1.2.0-alpha.1\").unwrap()),\n"
                "        \"1.2.0-alpha.1 must NOT satisfy `>=1.2.0-0, <1.2`\"\n"
                "    );\n"
                "}\n"
            ),
        },
        "issue": (
            "semver's VersionReq matching wrongly accepts a prerelease of an excluded upper "
            "bound. For example the requirement `>=1.2.0-0, <1.2` should NOT match the version "
            "`1.2.0-alpha.1`: the `<1.2` bound excludes every 1.2.0 release, and that must "
            "include 1.2.0's prereleases -- but it is currently reported as matching. More "
            "generally, a `<I.J` bound must not match `I.J.0` prereleases. Fix the "
            "version-requirement matching so a `<` (and `<=`) bound correctly excludes "
            "prereleases of its boundary, and keep the existing test suite passing."
        ),
    },
    "csvhelper_nullable": {
        "repo": "CsvHelper",
        "lang": "csharp",
        "fix": "9a7f0934633687f8ec58b58b5d81cb69633c541c",
        "parent": "8599e80f2a40fe073eeb5a281348169db7641be9",
        "source_files": ["src/CsvHelper/TypeConversion/TypeConverter.cs"],
        "test_project": "tests/CsvHelper.Tests/CsvHelper.Tests.csproj",
        "target_tests": "FullyQualifiedName~TypeConverter1Tests",
        # Narrow regression (like c++): the full CsvHelper suite is large; the target
        # class rebuilds the same test dll, so reuse it.
        "regression_tests": "FullyQualifiedName~TypeConverter1Tests",
        "issue": (
            "A custom type converter that derives from CsvHelper's generic "
            "TypeConverter<T> base, where T is a nullable value type (for example a "
            "converter for bool?), throws System.InvalidCastException when it is asked "
            "to convert a null value to a string. Writing a null nullable value should "
            "serialize normally to an empty string, not blow up. Fix the generic "
            "converter so converting a null of a nullable type to string works, and "
            "keep the existing test suite passing."
        ),
    },
    "dayjs_duration_round": {
        "repo": "dayjs",
        "lang": "javascript",
        "fix": "a9d7d0398d22ebd4bfc3812ca0134a97606d54d9",
        "parent": "5f3f8786c796cd432fe6bcb6966a810daea89203",
        "source_files": ["src/plugin/duration/index.js"],
        "target_tests": "test/plugin/duration.test.js",
        "regression_tests": "test/plugin/duration.test.js",
        "issue": (
            "dayjs's duration formatting produces sub-second values polluted with "
            "floating-point noise. For example dayjs.duration(-2812).toISOString() "
            "returns '-PT2.8120000000000003S' instead of '-PT2.812S', and "
            "dayjs.duration(3121632.27382247).toISOString() returns "
            "'PT52M1.6320000000000001S' instead of 'PT52M1.632S'. The sub-second "
            "component of the ISO string is not rounded to millisecond precision. Fix "
            "the duration ISO serialization so sub-second values are rounded to at "
            "most millisecond precision, and keep the existing test suite passing."
        ),
    },
    "mux_hostport_vars": {
        "repo": "mux",
        "lang": "go",
        "fix": "98cb6bf42e086f6af920b965c38cacc07402d51b",
        "parent": "948bec34b5168796bf3fc4dbb09215baa970351a",
        "source_files": ["regexp.go"],
        "target_tests": "TestHostMatcher",
        "regression_tests": "",
        "issue": (
            "gorilla/mux's Host() route matcher lets you omit the port from a host "
            "pattern (e.g. Host(\"{subdomain}.example.com\")), and such a route should "
            "still match requests whose Host header includes a port, ignoring the port "
            "entirely. Route matching itself already does this correctly. But when a "
            "route matches and mux extracts the named variables from the host into the "
            "request's variables map, it does not ignore the port the same way -- so "
            "for a wildcard-port host pattern, the extracted variables are wrong or "
            "missing whenever the incoming request's Host header includes a port. Fix "
            "variable extraction so it treats the port the same way route matching "
            "does, and keep the existing test suite passing."
        ),
    },
    "cjson_null_deref": {
        "repo": "cJSON",
        "lang": "c",
        "fix": "b2890c8d76bbb64e710585ebc0a917196b9c67e7",
        "parent": "a3f3d6c7843f3021b648623d13bc4fbca0084838",
        "source_files": ["cJSON.c"],
        "target_tests": "misc_tests",
        "regression_tests": "misc_tests",
        # cJSON's own tests/CMakeLists.txt disables -Werror only on the `unity`
        # library target, not on misc_tests itself -- so misc_tests.c (which also
        # includes unity's headers) still hits -Werror=long-long under our GCC's
        # -std=c89 -pedantic. Unrelated to the actual bug; -Wno-long-long is GCC's
        # documented, ordering-safe override for exactly this ISO-C90 tension.
        "cmake_opts": ["-DCMAKE_C_FLAGS=-Wno-long-long"],
        "issue": (
            "cJSON_SetNumberHelper(object, number) dereferences `object` immediately "
            "without checking for NULL first, so calling it with a NULL object pointer "
            "crashes instead of failing gracefully. It should check for a NULL object "
            "at entry and return NAN in that case, consistent with how other cJSON "
            "setter functions handle NULL. Fix it and keep the existing test suite "
            "passing."
        ),
    },
    "tspattern_ismatching": {
        "repo": "ts-pattern",
        "lang": "typescript",
        "fix": "470e7b909680ebbbe388bb1f006b7cebf2282dc8",
        "parent": "1520b57b070235a5603eb53112c1452d970db307",
        "source_files": ["src/is-matching.ts"],
        "target_tests": "tests/is-matching.test.ts",
        "regression_tests": "tests/is-matching.test.ts",
        "issue": (
            "ts-pattern's isMatching(pattern, value), the two-argument form of its "
            "type-guard helper, fails to type-check for almost any pattern that isn't "
            "a plain object pattern -- array patterns (P.array(P.number)), primitive "
            "patterns (P.number, P.boolean), literal patterns (1, 'oops'), and "
            "union/intersection patterns all throw a compile error, even though the "
            "equivalent curried form isMatching(pattern)(value) works fine. Fix the "
            "type signature so non-object patterns type-check correctly in the "
            "two-argument form too, while still preserving the original object-pattern "
            "behavior (matching against objects with extra unknown properties), and "
            "keep the existing test suite passing."
        ),
    },
    "dryschema_maybe_hash_array": {
        "repo": "dry-schema",
        "lang": "ruby",
        "fix": "31e76cb79641dd033a4bfc63b345584d70acf06f",
        "parent": "e33c59236b992e5c5c97bdb5d950411f65ad3d24",
        "source_files": ["lib/dry/schema/key_validator.rb"],
        "target_tests": "spec/integration/schema/unexpected_keys_spec.rb",
        "regression_tests": "spec/integration/schema/unexpected_keys_spec.rb",
        "issue": (
            "In dry-schema, when config.validate_keys = true is enabled, a schema "
            "containing required(:locations).array(:hash) { required(:feedback_location)"
            ".maybe(:hash) { ... } } incorrectly raises an \"is not allowed\" "
            "unexpected-key error when feedback_location is nil inside an array "
            "element. Since the field is declared maybe(:hash), nil should be accepted "
            "without error. Fix the key validator so nil values for optional nested "
            "hashes inside arrays aren't flagged as unexpected keys, and keep the "
            "existing test suite passing."
        ),
    },
    "gson_duplicate_key_null": {
        "repo": "gson",
        "lang": "java",
        "maven_module": "gson",
        "fix": "f4d371d29c04066dbe7fdb31f642831f9c7f40cd",
        "parent": "27d9ba1eeeeb156540cf5397504a4f9f256e911f",
        "source_files": [
            "gson/src/main/java/com/google/gson/internal/bind/MapTypeAdapterFactory.java",
        ],
        "target_tests": "MapTest,MapAsArrayTypeAdapterTest",
        "regression_tests": "MapTest,MapAsArrayTypeAdapterTest",
        "issue": (
            "Gson's Map deserializer detects duplicate JSON object keys by "
            "checking whether Map.put(key, value) returns a non-null previous "
            "value -- but put() legitimately returns null when the key's FIRST "
            "occurrence had a null value, so {\"a\":null,\"a\":1} silently "
            "deserializes to {a=1} instead of throwing JsonSyntaxException. Fix "
            "the duplicate-key check (at both the plain-object call site and the "
            "enableComplexMapKeySerialization array-of-entries call site) so it "
            "correctly detects a repeated key regardless of the first value, and "
            "keep the existing test suite passing."
        ),
    },
    "hashie_deep_merge_dup": {
        "repo": "hashie",
        "lang": "ruby",
        "fix": "4f014e7fedad93fa2070166051947070cc8ac01c",
        "parent": "641bafcb44bd164c33ec6a9817ae6b79c3741491",
        "source_files": [
            "lib/hashie/extensions/deep_merge.rb",
            "lib/hashie/utils.rb",
        ],
        "text_patches": {
            # Windows/RubyGems can't extract the `git` gem's symlinked package
            # contents (pulled in transitively by this dev-tooling group); it's
            # CI-reporting/changelog tooling, untouched by the actual tests.
            "Gemfile": [
                ("\ngroup :test do\n"
                 "  gem 'codeclimate-test-reporter', '~> 1.0', require: false\n"
                 "  gem 'danger-changelog', '~> 0.1.0', require: false\n"
                 "end\n", "\n"),
            ],
            # pry is a REPL debugger from the (excluded) :development group;
            # spec_helper requiring it unconditionally blocks collection.
            "spec/spec_helper.rb": [
                ("require 'pry'\n", ""),
            ],
        },
        "target_tests": "spec/hashie/extensions/deep_merge_spec.rb",
        "regression_tests": "spec/hashie/extensions/deep_merge_spec.rb",
        "issue": (
            "Hashie::Extensions::DeepMerge#deep_merge uses a shallow dup before "
            "merging, so nested hash values inside the receiver are still shared "
            "references with the original -- mutating the 'merged' result silently "
            "corrupts the original hash's nested structures too. Fix deep_merge so "
            "it produces a true deep copy (nested hashes included) without raising "
            "on Ruby values that can't be dup'd (Symbol, true/false, nil, Integer, "
            "Rational, Complex, Method, ...), and keep the existing test suite "
            "passing."
        ),
    },
    "addressable_template_nonstring": {
        "repo": "addressable",
        "lang": "ruby",
        "fix": "c00d58b084597ef53c7621d866b39dd1c7aa133c",
        "parent": "bcaf766b0a91d889d0a0bfc5cfbdc07bd376924b",
        "source_files": ["lib/addressable/template.rb"],
        "target_tests": "spec/addressable/template_spec.rb",
        "regression_tests": "",
        "issue": (
            "Addressable::Template#expand crashes with a NoMethodError "
            "(\"undefined method 'to_str' for an instance of Symbol\") when "
            "expanding an RFC 6570 URI template with a composite (Hash or Array) "
            "variable whose leaf values aren't strings -- for example a Hash key "
            "that's a Symbol, or an Array of Integers. Fix template expansion so "
            "non-string leaf values in composite variables are stringified "
            "correctly instead of crashing, and keep the existing test suite "
            "passing."
        ),
    },
    "httpparser_line_folding": {
        "repo": "http-parser",
        "lang": "c",
        "c_build": "manual",
        "c_sources": ["http_parser.c", "test.c"],
        "c_defines": ["HTTP_PARSER_STRICT=1"],
        "c_binary": "test_g",
        "c_success_marker": "requests okay",
        "fix": "76f0f1690fb4ea80e655327a96c7549f4c1fdf5d",
        "parent": "5d9c3821729b194eef60f41fcc5f8b4657c3d8ff",
        "source_files": ["http_parser.c"],
        "target_tests": "",
        "regression_tests": "",
        "issue": (
            "The HTTP header-value parser mishandles a header whose value is "
            "empty on the field's own line and only appears on an RFC-2616 "
            "line-folding continuation line (e.g. \"Connection:\\r\\n close\\r\\n\"). "
            "When the parser hits the CR of the empty first line, it prematurely "
            "resets its internal header state and fires the value callback "
            "before it knows a continuation line follows. This means "
            "'interesting' headers (Connection, Content-Length, "
            "Transfer-Encoding) whose real value only arrives via a fold are "
            "never recognized as such -- e.g. 'Connection: close' split this way "
            "fails to set the close flag, so keep-alive stays on when it must be "
            "off. Fix the state machine so it looks ahead before deciding a "
            "header value is complete, and keep the existing test suite passing."
        ),
    },
    "nlohmannjson_diagnostic_offsets": {
        "repo": "nlohmann-json",
        "lang": "cpp",
        "cpp_test_framework": "doctest",
        "cmake_opts": ["-DJSON_BuildTests=ON"],
        "fix": "bacdabd176955be6b5157b7e26075ba9965584b2",
        "parent": "d5647e6a3be71adbcaac444f8cd1acae109c4046",
        "source_files": ["include/nlohmann/detail/input/lexer.hpp",
                         "include/nlohmann/detail/input/json_sax.hpp"],
        "target_tests": "test-diagnostic-positions_cpp11",
        "regression_tests": "test-diagnostic-positions_cpp11",
        "issue": (
            "nlohmann::json's diagnostic-positions feature (JSON_DIAGNOSTIC_POSITIONS) "
            "lets a parsed value report start_pos()/end_pos() -- byte offsets into "
            "the original source. For strings, the start offset is currently "
            "derived by subtracting the PARSED string's length from the end "
            "offset. This is wrong whenever the string contains escape sequences "
            "(\\n, \\t, \\\", \\\\, etc.): the source token is longer than the "
            "decoded value, so the computed start lands inside the string instead "
            "of at the opening quote. Fix it so start_pos()/end_pos() are correct "
            "for any mix of escapes and plain/multi-byte UTF-8 content, across "
            "both the DOM and streaming/callback SAX parser paths, and keep the "
            "existing test suite passing."
        ),
    },
    "marked_lexer_linebreaks": {
        "repo": "marked",
        "lang": "javascript",
        "js_test_framework": "jasmine",
        "fix": "a9696e28989c0bea2077885bab1844525e18a031",
        "parent": "6aacd133e4aadae3427879574a9279d8d85cdc8f",
        "source_files": ["src/Lexer.js", "src/Tokenizer.js"],
        "target_tests": "test/unit/Lexer-spec.js test/unit/marked-spec.js",
        "regression_tests": "test/unit/Lexer-spec.js test/unit/marked-spec.js",
        "issue": (
            "Markdown lists are sometimes misclassified as 'loose' (rendering "
            "with <p> tags inside <li>) when they shouldn't be, and single "
            "trailing newlines inside tokens are silently dropped instead of "
            "being retained in the token stream. The Lexer's line-accumulation "
            "logic and the Tokenizer's list-parsing logic each track newlines "
            "independently and disagree about how many consecutive line breaks "
            "should mark a list as loose vs. tight. Trace how the Lexer "
            "accumulates raw text between tokens and how the Tokenizer counts "
            "line breaks per list item, then fix both so a single newline is "
            "preserved but only multiple consecutive line breaks trigger "
            "loose-list formatting, and keep the existing test suite passing."
        ),
    },
    "zod_pipe_payload_flag": {
        "repo": "zod",
        "lang": "typescript",
        "js_test_framework": "pnpm_vitest",
        "vitest_project": "zod",
        "fix": "c2be4f819064eed62c7c350a2d399b5faecd15f8",
        "parent": "1cab69383fcdeae2a366d5e2a2fc4d8fc765d168",
        "source_files": [
            "packages/zod/src/v4/core/schemas.ts",
            "packages/zod/src/v4/classic/schemas.ts",
        ],
        "target_tests": ("packages/zod/src/v4/classic/tests/catch.test.ts "
                         "packages/zod/src/v4/classic/tests/preprocess.test.ts"),
        "regression_tests": ("packages/zod/src/v4/classic/tests/catch.test.ts "
                             "packages/zod/src/v4/classic/tests/preprocess.test.ts"),
        "issue": (
            "Zod's internal ParsePayload carries a caught/fallback flag so an "
            "outer .optional() knows to override a recovered value with "
            "undefined when the original input was undefined. This flag isn't "
            "propagated correctly through pipe boundaries (.pipe(), used "
            "internally by .transform() and .preprocess()): the pipe result "
            "handler builds a fresh payload for the right side of a pipe "
            "without carrying the flag forward, so a chain like "
            "z.string().catch('X').pipe(z.string()).optional().parse(undefined) "
            "wrongly returns 'X' instead of undefined. Separately, "
            "z.object({ a: z.preprocess(fn, T) }).parse({}) -- a preprocess "
            "function meant to fill in a value for a missing key -- throws an "
            "'expected nonoptional' error instead of running fn with undefined. "
            "Fix both, and keep the existing test suite passing."
        ),
    },
    "sqlparser_exponential_backtrack": {
        "repo": "sqlparser-rs",
        "lang": "rust",
        "fix": "fd5c1633a8633dd202e36a58609ccb7be0cb6387",
        "parent": "b3760221fa74844f0006a7bc65155318c6817920",
        "source_files": ["src/parser/mod.rs"],
        "target_tests": "",
        "regression_tests": "",
        "issue": (
            "Parsing deeply-nested parenthesized table factors, e.g. "
            "SELECT 1 FROM ((((... with many levels of nesting, causes "
            "catastrophic (exponential) parse time instead of failing or "
            "succeeding quickly. In parse_table_factor, a speculative attempt "
            "to parse a derived table fails and backtracks, but the nested-join "
            "fallback path then recurses back into parse_table_factor over the "
            "same remaining paren chain and retries the identical speculative "
            "parse -- doubling work at every nesting level. Find and fix the "
            "root cause so parsing such a chain completes in bounded time, and "
            "keep the existing test suite passing."
        ),
    },
    "natsserver_oversized_publish_raft": {
        "repo": "nats-server",
        "lang": "go",
        "fix": "dce0b028b523ad11f740800fbca2781eee09cb41",
        "parent": "a0f553bbcf1977df9be7855950dc71cdda1ae540",
        "source_files": ["server/filestore.go", "server/jetstream_batching.go", "server/stream.go"],
        "target_tests": "TestJetStreamRejectLargePublishes|TestJetStreamClusterRejectLargePublishesBeforeProposal",
        "regression_tests": "",
        "issue": (
            "JetStream file-storage streams must reject a publish whose message "
            "exceeds the file store's max on-disk record size with a 'message "
            "too large' error, and the stream must stay healthy afterward. The "
            "size check only exists deep in the file store's low-level write "
            "path, guarded on a single-server (R1) stream by a later "
            "consistency-check gate -- but that gate is explicitly disabled for "
            "clustered/replicated (R3) streams. So for a replicated stream, an "
            "oversized publish sails past every pre-check, gets proposed to and "
            "committed by the Raft group, and only then does each replica "
            "discover -- while applying the already-committed entry -- that the "
            "file store refuses to write it, leaving the stream unable to "
            "accept further publishes. Fix this so an oversized message is "
            "rejected BEFORE it ever reaches Raft, on both the single-server "
            "and clustered pre-proposal paths, and keep the existing test "
            "suite passing."
        ),
    },
    "quartznet_misfire_reschedule": {
        "repo": "quartznet",
        "lang": "csharp",
        "csharp_drop_global_json": True,
        "csharp_project_langversion": {"src/Quartz/Quartz.csproj": "preview"},
        "dotnet_props": ["TreatWarningsAsErrors=false", "WarningsAsErrors="],
        "text_patches": {
            # Ambiguous under our SDK's Roslyn (ties AutoVerify(bool) vs
            # AutoVerify(bool,bool)); the repo's own pinned SDK resolves it fine.
            # Only reached when a debugger is attached, unrelated to any test
            # assertion -- disambiguating the call doesn't touch behavior.
            "src/Quartz.Tests.Unit/Simpl/JsonObjectSerializerTest.cs": [
                ("verifier.AutoVerify();", "verifier.AutoVerify(true);"),
            ],
        },
        "fix": "417a5b20cec674bddc8be1142899563273ff7576",
        "parent": "bac5084d1ba765b815666e42a5a75e7f986e384d",
        "source_files": [
            "src/Quartz/Impl/Triggers/AbstractTrigger.cs",
            "src/Quartz/Impl/Triggers/SimpleTriggerImpl.cs",
            "src/Quartz/Impl/Triggers/CronTriggerImpl.cs",
            "src/Quartz/Impl/Triggers/CalendarIntervalTriggerImpl.cs",
            "src/Quartz/Impl/Triggers/DailyTimeIntervalTriggerImpl.cs",
            "src/Quartz/Impl/Triggers/RecurrenceTriggerImpl.cs",
            "src/Quartz/Impl/AdoJobStore/JobStoreSupport.cs",
            "src/Quartz/Simpl/RAMJobStore.cs",
            "src/Quartz/SPI/IOperableTrigger.cs",
        ],
        "test_project": "src/Quartz.Tests.Unit/Quartz.Tests.Unit.csproj",
        "target_tests": "FullyQualifiedName~RescheduleNextWithExistingCount_PastStartTime_DoesNotFireImmediately",
        "regression_tests": "FullyQualifiedName~RescheduleNextWithExistingCount_PastStartTime_DoesNotFireImmediately",
        "issue": (
            "Since v3.17, triggers using the DoNothing/RescheduleNextWith* "
            "misfire-handling instructions compute the rescheduled fire time "
            "using a time shifted back by the misfire threshold, instead of the "
            "actual current time. This means a trigger with a past StartAt and "
            "e.g. WithMisfireHandlingInstructionNextWithExistingCount can fire "
            "immediately at scheduler startup instead of waiting for its next "
            "legitimately scheduled occurrence, because the computed fire time "
            "can land inside the misfire-threshold window. Fix this across all "
            "trigger implementations and the job stores that call their "
            "misfire-handling methods, restoring the 'does not want to be "
            "fired now' semantics, while guarding against infinite loops when "
            "a calendar excludes all future times, and keep the existing test "
            "suite passing."
        ),
    },
    # ---- added python task (agent-built, fail->pass verified) ----
    "rich_softwrap_style_newline": {
        "repo": "rich",
        "lang": "python",
        "fix": "39ee57dfe70614381c3ebce34cb35cab557af2f5",
        "parent": "05ff970926cbd0b5d0acb6fc18cdbd1fc971e582",
        "source_files": ["rich/console.py"],
        "target_tests": "tests/test_text.py::test_soft_wrap_styled",
        # The whole suite runs in ~5s and is fully green at the fix commit
        # (962 passed, 23 skipped, 0 failed), so regression can be the real
        # thing rather than a single file.
        "regression_tests": "tests",
        "issue": (
            "When Console.print() is given a style AND soft_wrap=True, the style is "
            "wrongly applied to the line break itself, so the background colour bleeds "
            "past the end of the printed text instead of being reset at the end of the "
            "line. For example, with "
            "`console = Console(color_system=\"standard\", width=80, force_terminal=True)` "
            "then `console.print(\"soft wrap is on\", style=\"blue on white\", "
            "soft_wrap=True)` followed by `console.print(\"Next line\")` emits "
            "'\\x1b[34;47msoft wrap is on\\x1b[0m\\x1b[34;47m\\n\\x1b[0mNext line\\n' -- "
            "the styling sequence is re-opened around the newline and only reset "
            "afterwards. The expected output is "
            "'\\x1b[34;47msoft wrap is on\\x1b[0m\\nNext line\\n': the style must be "
            "closed BEFORE the newline, so soft-wrapped styled output does not paint "
            "the newline or leak its background into what follows. Note that the "
            "non-soft-wrap path already gets this right; only the soft-wrap path is "
            "affected. Fix it and keep the existing test suite passing."
        ),
    },

    # ---- added java task (agent-built, fail->pass verified) ----
    "jsoup_negative_nth_child": {
        "repo": "jsoup",
        "lang": "java",
        # jsoup is a SINGLE-module Maven project -- no "maven_module" key needed
        # (contrast gson, which is a reactor and needs -pl/-am).
        "fix": "62674f903bd2fc352601fa39a3d9dea348e59f4b",
        "parent": "d5acae96d5158d387ef70e62caad593202adc1a9",
        "source_files": [
            "src/main/java/org/jsoup/select/QueryParser.java",
            # CHANGES.md is reverted along with the real source file purely to
            # scrub a spoiler: the fix commit adds a release-note bullet that
            # states the diagnosis verbatim ("An `:nth-child` selector with a
            # negative digit-less step, such as `:nth-child(-n+2)`, would be
            # parsed incorrectly as a positive step"), which would hand the
            # agent the answer for free. Reverting a markdown file is inert for
            # the tests.
            "CHANGES.md",
        ],
        # run_maven turns this into -Dtest=<target>; same class-name convention
        # as commonscli_npe ("BugsTest") and gson_duplicate_key_null.
        "target_tests": "SelectorTest",
        "regression_tests": "",   # empty => run the WHOLE suite (see run_maven)
        "issue": (
            "jsoup's CSS selector engine mis-parses an :nth-child argument whose "
            "step has a minus sign but no digit, such as \":nth-child(-n+2)\". The "
            "leading minus is dropped, so the step is treated as +1 rather than -1 "
            "and the selector matches the wrong elements. Parsing the document "
            "\"<p>1</p> <p>2</p> <p>3</p> <p>4</p>\", the query "
            "\"p:nth-child(-n+2)\" should select exactly the first two paragraphs "
            "(own text \"1\" and \"2\"), which is what the equivalent explicit-digit "
            "form \"p:nth-child(-1n+2)\" already returns -- but the digit-less form "
            "returns more elements than that. Consequently a combined query like "
            "\"p:nth-child(n+2):nth-child(-n+2)\", which should narrow to just \"2\", "
            "is also wrong. The same argument parsing is shared by :nth-last-child, "
            ":nth-of-type and :nth-last-of-type, so those are affected too. All the "
            "other argument forms must keep working exactly as they do now: the "
            "positive digit-less step \"p:nth-child(n+2)\" (selecting \"2\", \"3\", "
            "\"4\"), explicit-digit steps such as \"p:nth-child(2n+2)\" (selecting "
            "\"2\", \"4\") and \"p:nth-child(-1n+2)\", plain numeric offsets, the "
            "\"odd\" and \"even\" keywords, and the SelectorParseException raised for "
            "genuinely unparseable arguments. Please fix it and keep the existing "
            "test suite passing."
        ),
    },

    # ---- added rust task (agent-built, fail->pass verified) ----
    "chrono_reverse_date_iterators": {
        "repo": "chrono",
        "lang": "rust",
        "fix": "7b6436f65e0c7ec2f9a7cdea88af1f3851a01f6f",
        "parent": "7fa24eac9514db65eb8bddf7fadeca71b68e414a",
        "source_files": ["src/naive/date/mod.rs"],
        # run_cargo ignores `target`; it always runs the whole `cargo test`.
        # Same convention as semver_prerelease / sqlparser_exponential_backtrack.
        "target_tests": "",
        "regression_tests": "",
        "issue": (
            "chrono's NaiveDate day and week iterators are double-ended, but reversing "
            "them is broken. Reversing a bounded window of NaiveDate::iter_days() or "
            "NaiveDate::iter_weeks() does not yield that window's own dates in reverse "
            "order -- it yields dates from a completely unrelated part of the calendar. "
            "For example, starting at 2025-10-10, taking a 10-day window and then "
            "reversing it should produce 2025-10-19 down to 2025-10-10; instead it "
            "produces a single date in the year -258092. Near the top of the "
            "representable range the same window that forward iteration correctly "
            "limits to 2 dates reports over 190 million dates once reversed, and the "
            "week iterator misbehaves in exactly the same way. Reverse iteration "
            "appears to run backwards from the date iteration STARTED at, walking below "
            "it, rather than over the range actually being iterated -- and the length "
            "these iterators report is likewise the distance to the end of the "
            "representable range rather than the length of the range being iterated, so "
            "anything that relies on that length to step in from the back lands far "
            "outside the intended window. Fix reverse iteration for both the day and "
            "the week iterator so that reversing a bounded window yields exactly the "
            "same dates as forward iteration, in reverse order, and keep the existing "
            "test suite passing."
        ),
    },

    # ---- added ruby task (agent-built, fail->pass verified) ----
    "money_divide_by_zero": {
        "repo": "money",
        "lang": "ruby",
        "fix": "f8582eb85c91e8e3de690a978d9aae8398a994c9",
        "parent": "b751843df2f2eaa35121677584b8c4b40819a6ed",
        # CHANGELOG.md is reverted along with the real source file purely to
        # scrub a spoiler: the fix commit adds the bullet "Not allow divide by
        # zero" to the unreleased section, which would hand the agent the
        # answer for free. Reverting a markdown file is inert for the specs.
        "source_files": [
            "lib/money/money/arithmetic.rb",
            "CHANGELOG.md",
        ],
        "text_patches": {
            "Gemfile": [
                # pry -> reline -> io-console is a NATIVE extension gem, and
                # io-console 0.9.x fails to compile under our MinGW GCC
                # (-Wincompatible-pointer-types is a hard error since GCC 14;
                # RUBY_CFLAGS/CFLAGS=-Wno-... does not survive mkmf's flag
                # ordering here). pry is a REPL debugger, require:false, and
                # nothing in spec/ touches it.
                ("gem 'pry', require: false\n", ""),
                # rbs + typeprof are RBS type-signature tooling; they drag in
                # prism, another native extension that fails to build for the
                # same reason. Unused by the specs.
                ("gem 'rbs', platforms: %i[mri mingw x64_mingw]\n"
                 "gem 'typeprof', platforms: %i[mri mingw x64_mingw]\n", ""),
                # money declares rspec/rake/yard as gemspec
                # add_development_dependency, which `gemspec` puts in the
                # :development group -- and run_rspec runs `bundle config set
                # without ... development`, so rspec itself would never be
                # installed ("can't find executable rspec for gem rspec-core").
                # Re-homing the gemspec's dev deps into :test keeps them.
                ("\ngemspec\n", "\ngemspec development_group: :test\n"),
            ],
            "money.gemspec": [
                # bigdecimal's C extension does not compile under our MinGW GCC
                # (same -Wincompatible-pointer-types hard error; verified for
                # both 3.1.5 and 4.1.2). Ruby 3.3 ships bigdecimal as a DEFAULT
                # gem, whose .so is on the interpreter's own $LOAD_PATH, so
                # `require "bigdecimal"` still resolves at runtime with the
                # bundler dependency removed -- confirmed by the full 497-example
                # suite passing green at the fix commit.
                ('  s.add_dependency "bigdecimal"\n', ""),
            ],
        },
        "target_tests": "spec/money/arithmetic_spec.rb",
        "regression_tests": "",   # whole suite: 497 examples, 0 pre-existing failures
        "issue": (
            "Money's division and divmod operations don't guard against a zero "
            "divisor, so dividing by zero produces nonsense instead of failing "
            "cleanly. Money.new(100, 'USD') / Money.new(0, 'USD') raises nothing "
            "at all and yields an infinite amount; Money.new(100, 'USD') / 0 "
            "(and / 0.0, / BigDecimal('0')) blows up with an unrelated "
            "\"ArgumentError: must be initialized with a finite value\" thrown "
            "from deep inside Money's own constructor; and "
            "Money.new(100, 'USD').divmod(Money.new(0, 'USD')) / "
            "Money.new(100, 'USD').divmod(0) leak BigDecimal's low-level "
            "\"divided by 0\" error instead of anything meaningful about money. "
            "All of these should fail fast with a ZeroDivisionError raised by "
            "Money itself: the message must be \"divided by Money(0)\" when the "
            "divisor is a zero-valued Money, and \"divided by zero\" when the "
            "divisor is a plain numeric zero (Integer, Float or BigDecimal). "
            "Division and modulo by non-zero values must behave exactly as "
            "before. Please fix it and keep the existing test suite passing."
        ),
    },

}


# Told to the benzi_told arm only. Deliberately DESCRIPTIVE, not directive about
# the task: it names the capability and when it applies, and contains nothing
# about this bug, this repo, or where the fix lives. Anything more would be
# coaching the treatment and the number would stop meaning anything.
INDEX_BRIEFING = (
    "This session has a precomputed, resolved index of this codebase available "
    "through the `benzi` MCP tools: list_files, search_symbols, get_definition, "
    "get_callers, profile, trace_path, backflow, skim_source, read_source. "
    "It answers structural questions by lookup rather than by reading or grepping "
    "files -- where a symbol is defined, who calls it, what a change would affect, "
    "how two functions connect, where a value comes from. Every symbol has a stable "
    "id (`file::scope::name`) that any of these tools accepts. For navigating and "
    "understanding this codebase, these are usually faster and more complete than "
    "grep; your normal tools remain available for everything else."
)


def sh(cmd: list[str] | str, cwd: Path | None = None, timeout: int = 900,
      env: dict | None = None) -> subprocess.CompletedProcess:
    # errors="replace": jest/node/dotnet emit UTF-8 (✓/✗, box-drawing); Windows'
    # default cp1252 decode would crash the reader thread on the first such byte.
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          timeout=timeout, shell=isinstance(cmd, str), env=env)


def repo_dir(task: dict) -> Path:
    return BENCH / task["repo"]


def venv_py(task: dict) -> Path:
    return repo_dir(task) / ".venv" / "Scripts" / "python.exe"


# -- pytest ------------------------------------------------------------------
_SUB = re.compile(r"^SUBFAILED\[(?P<case>.+)\]\s+(?P<node>\S+)", re.M)
_FAIL = re.compile(r"^FAILED\s+(?P<node>\S+)", re.M)


def run_pytest(task: dict, wt: Path, target: str) -> dict:
    """Failures as a SET of stable ids. sqlglot uses subtests, so a single test
    node can carry many independent cases -- keyed by node+case, they stay
    comparable between the baseline and a post-agent run."""
    env = dict(os.environ)
    env.update(task.get("pytest_env", {}))
    proc = sh([str(venv_py(task)), "-m", "pytest", target, "-q", "--no-header"],
              cwd=wt, timeout=1200, env=env)
    out = proc.stdout + proc.stderr
    failures = {f"{m.group('node')}::[{m.group('case')}]" for m in _SUB.finditer(out)}
    failures |= {m.group("node") for m in _FAIL.finditer(out)}
    tail = [ln for ln in out.strip().splitlines() if " passed" in ln or " failed" in ln]
    return {"failures": failures, "summary": tail[-1] if tail else "(no summary)",
            "collect_error": "error" in out.lower() and "passed" not in out.lower()}


def run_maven(task: dict, wt: Path, target: str) -> dict:
    """Java via Maven. Failures come from the surefire XML reports (robust across
    surefire's console formatting) keyed Class.method -- the JUnit analog of a
    pytest node id. `target` is a -Dtest pattern (a class, or a wildcard)."""
    import xml.etree.ElementTree as ET
    mvn = str(MAVEN_BIN / "mvn.cmd")
    cmd = [mvn, "-q", "-B", "-DfailIfNoTests=false", "-Dsurefire.failIfNoSpecifiedTests=false"]
    if task.get("maven_module"):
        # Self-contained multi-module reactor (gson-style: every module lives in
        # THIS repo, unlike jackson-databind's unpublished-sibling-POM dead end)
        # -- -am builds the module's own in-reactor dependencies first.
        cmd += ["-pl", task["maven_module"], "-am"]
    if target:                              # empty target => run the WHOLE suite (regression)
        cmd.append(f"-Dtest={target}")
    cmd.append("test")
    proc = sh(cmd, cwd=wt, timeout=1800, env=_lang_env("java"))
    out = proc.stdout + proc.stderr
    failures, total = set(), 0
    for xmlf in wt.glob("**/target/surefire-reports/TEST-*.xml"):
        try:
            root = ET.parse(xmlf).getroot()
        except ET.ParseError:
            continue
        for tc in root.iter("testcase"):
            total += 1
            if any(c.tag in ("failure", "error") for c in tc):
                failures.add(f"{tc.get('classname')}.{tc.get('name')}")
    return {"failures": failures, "summary": f"{total} run, {len(failures)} failed",
            "collect_error": total == 0}   # nothing ran -> compile error / bad pattern; never trust


def run_ctest(task: dict, wt: Path, target: str) -> dict:
    """C++ via CMake+Ninja+GCC. Configure once, build the target test, run its
    gtest binary, read `[ FAILED ] Suite.Case` lines. Regression reuses the same
    binary (a header edit recompiles it) -- narrower than Python's whole-suite
    sweep; a fair caveat, noted in the writeup."""
    env = _lang_env("cpp")
    cmake = str(CMAKE_BIN / "cmake.exe")
    build = wt / "build"
    if not (build / "build.ninja").exists():
        sh([cmake, "-S", str(wt), "-B", str(build), "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release", *task.get("cmake_opts", [])],
           cwd=wt, timeout=600, env=env)
    b = sh([cmake, "--build", str(build), "--target", target], cwd=wt, timeout=1800, env=env)
    # The gtest binary's location varies by project (build/bin, build/test, ...),
    # so glob for it rather than hardcode one layout.
    binp = next(iter(build.glob(f"**/{target}.exe")), None)
    if b.returncode != 0 or binp is None or not binp.exists():
        (RESULTS / "last_build_fail.txt").write_text((b.stdout or "") + (b.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(build failed)", "collect_error": True}
    proc = sh([str(binp)], cwd=wt, timeout=600, env=env)
    out = proc.stdout + proc.stderr
    failures = {m.group(1) for m in re.finditer(r"^\[\s*FAILED\s*\]\s+(\S+\.\S+)", out, re.M)}
    ran = re.search(r"\[=+\]\s+\d+ test", out)
    return {"failures": failures, "summary": (ran.group(0) if ran else "(no summary)"),
            "collect_error": ran is None}


def run_ctest_doctest(task: dict, wt: Path, target: str) -> dict:
    """C++ via CMake+Ninja+GCC, same build as run_ctest but for a doctest binary,
    not gtest -- different summary format (`[doctest] test cases: N | P passed |
    F failed | S skipped`), and doctest's per-CHECK failure lines are free-form
    (no stable `Suite.Case` id to regex out the way gtest's `[ FAILED ]` gives
    us). Coarse like run_ctest_c's crash fallback: a failure is reported under
    the TARGET's own name, not per-assertion -- fine here since these files
    typically hold one focused TEST_CASE anyway."""
    env = _lang_env("cpp")
    cmake = str(CMAKE_BIN / "cmake.exe")
    build = wt / "build"
    if not (build / "build.ninja").exists():
        sh([cmake, "-S", str(wt), "-B", str(build), "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release", *task.get("cmake_opts", [])],
           cwd=wt, timeout=600, env=env)
    b = sh([cmake, "--build", str(build), "--target", target], cwd=wt, timeout=1800, env=env)
    binp = next(iter(build.glob(f"**/{target}.exe")), None)
    if b.returncode != 0 or binp is None or not binp.exists():
        (RESULTS / "last_build_fail.txt").write_text((b.stdout or "") + (b.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(build failed)", "collect_error": True}
    proc = sh([str(binp)], cwd=wt, timeout=600, env=env)
    out = proc.stdout + proc.stderr
    summary = re.search(r"test cases:\s*(\d+)\s*\|\s*(\d+) passed\s*\|\s*(\d+) failed", out)
    if summary is None:
        return {"failures": {target}, "summary": "(crashed before completing)",
                "collect_error": False}
    n_fail = int(summary.group(3))
    failures = {target} if n_fail else set()
    return {"failures": failures, "summary": summary.group(0), "collect_error": False}


def run_ctest_c(task: dict, wt: Path, target: str) -> dict:
    """Plain C via CMake+Ninja+GCC, same toolchain as run_ctest but for a Unity
    test binary, not gtest -- different pass/fail text format, and (the reason
    this isn't just run_ctest with a regex swap) a real memory-safety bug can
    CRASH the whole binary instead of printing a clean FAIL line for one case.
    A crash means Unity never gets to print its summary, so there's nothing to
    parse -- but it's still a real, trustworthy failure signal (not a harness
    error), so it's folded into `failures` under the binary/ctest target's own
    name rather than surfaced as collect_error (which would make baseline()
    read a crashing bug as ZERO failing tests -- the opposite of the truth)."""
    env = _lang_env("c")
    cmake = str(CMAKE_BIN / "cmake.exe")
    build = wt / "build"
    if not (build / "build.ninja").exists():
        sh([cmake, "-S", str(wt), "-B", str(build), "-G", "Ninja",
            "-DCMAKE_BUILD_TYPE=Release", "-DENABLE_CJSON_TEST=ON",
            *task.get("cmake_opts", [])], cwd=wt, timeout=600, env=env)
    b = sh([cmake, "--build", str(build), "--target", target], cwd=wt, timeout=1800, env=env)
    binp = next(iter(build.glob(f"**/{target}.exe")), None)
    if b.returncode != 0 or binp is None or not binp.exists():
        (RESULTS / "last_build_fail.txt").write_text((b.stdout or "") + (b.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(build failed)", "collect_error": True}
    proc = sh([str(binp)], cwd=wt, timeout=120, env=env)
    out = proc.stdout + proc.stderr
    named_fails = {m.group(1) for m in re.finditer(r"^[^:\n]+:\d+:(\w+):FAIL", out, re.M)}
    summary = re.search(r"(\d+) Tests (\d+) Failures (\d+) Ignored", out)
    if summary is None:
        # Crashed (or otherwise never reached its own summary line) -- the whole
        # target is the failure signal; individual case names aren't recoverable.
        return {"failures": {target}, "summary": "(crashed before completing)",
                "collect_error": False}
    n_fail = int(summary.group(2))
    failures = named_fails if n_fail else set()
    if n_fail and not named_fails:
        failures = {target}   # Unity reported failures but the FAIL-line regex missed them
    return {"failures": failures, "summary": summary.group(0), "collect_error": False}


def run_c_manual(task: dict, wt: Path, target: str) -> dict:
    """Plain C via a direct gcc compile+link -- for a repo with no CMake/Makefile
    test target at all, just a self-contained test binary with its own main()
    and its own pass/fail signal (commonly hand-rolled asserts: a failure
    aborts immediately, a full run prints a known success marker and exits 0).
    Task config: c_sources (files to compile), c_defines (-D flags), c_binary
    (output name), c_success_marker (substring that must appear in stdout for
    a clean pass). `target` is unused -- like cargo, there's one binary, no
    sub-selection; regression is just rerunning the same binary."""
    env = _lang_env("c")
    gcc = str(GCC_BIN / "gcc.exe")
    sources = task.get("c_sources", [])
    defines = [f"-D{d}" for d in task.get("c_defines", [])]
    binary = task.get("c_binary", "test_bin")
    binp = wt / f"{binary}.exe"
    b = sh([gcc, "-I", str(wt), *defines, "-o", str(binp), *sources],
           cwd=wt, timeout=300, env=env)
    if b.returncode != 0 or not binp.exists():
        (RESULTS / "last_build_fail.txt").write_text((b.stdout or "") + (b.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(build failed)", "collect_error": True}
    proc = sh([str(binp)], cwd=wt, timeout=120, env=env)
    out = proc.stdout + proc.stderr
    marker = task.get("c_success_marker", "")
    if proc.returncode == 0 and marker and marker in out:
        return {"failures": set(), "summary": f"clean ({marker!r} seen)", "collect_error": False}
    # Nonzero exit (assert/abort) or the success marker never printed -- a real
    # failure, not a harness error; same reasoning as run_ctest_c's crash case.
    return {"failures": {binary}, "summary": f"(failed, exit={proc.returncode})",
            "collect_error": False}


def run_cargo(task: dict, wt: Path, target: str) -> dict:
    """Rust via `cargo test` (gnu toolchain, mingw linker). Failing tests show as
    `test NAME ... FAILED`; a `test result:` line anywhere means tests actually ran
    (its absence = a compile failure, so nothing ran -> collect_error)."""
    env = _lang_env("rust")
    cargo = str(RUST_HOME / "cargo" / "bin" / "cargo.exe")
    r = sh([cargo, "test"], cwd=wt, timeout=1800, env=env)
    out = (r.stdout or "") + (r.stderr or "")
    if re.search(r"test result:", out) is None:
        (RESULTS / "last_build_fail.txt").write_text(out[-4000:], encoding="utf-8")
        return {"failures": set(), "summary": "(build failed)", "collect_error": True}
    failures = set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M))
    summ = re.search(r"test result:[^\n]*", out)
    return {"failures": failures, "summary": summ.group(0) if summ else "cargo ran",
            "collect_error": False}


def run_go(task: dict, wt: Path, target: str) -> dict:
    """Go via `go test -json` -- structured, one JSON object per test event, so
    parsing is exact (no text-format guessing the way gtest/Unity need). `target`
    is a `-run` regex (empty = no filter, matching the "empty target = whole
    suite" convention used elsewhere). A package that never emits a single "run"
    event means it didn't even compile -- collect_error, same meaning as the
    other runners' "nothing ran"."""
    env = _lang_env("go")
    go = str(_TOOLS / "go" / "bin" / "go.exe")
    cmd = [go, "test", "-json", "./..."]
    if target:
        cmd += ["-run", target]
    proc = sh(cmd, cwd=wt, timeout=1200, env=env)
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    ran, failures, n_pass, n_fail = False, set(), 0, 0
    for line in out.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        act, test = ev.get("Action"), ev.get("Test")
        if act == "run" and test:
            ran = True
        elif act == "fail" and test:
            failures.add(test)
            n_fail += 1
        elif act == "pass" and test:
            n_pass += 1
    return {"failures": failures, "summary": f"{n_pass} passed, {n_fail} failed",
            "collect_error": not ran}


def run_rspec(task: dict, wt: Path, target: str) -> dict:
    """Ruby via `bundle exec rspec --format json`. `bundle install` is re-run
    every call, but gems land in the SHARED GEM_HOME/BUNDLE_PATH (see
    _lang_env), so after the first call it's a fast local no-network check, the
    same amortization NuGet gets for csharp. `target` is a spec file path (empty
    = whole suite, same convention as everywhere else)."""
    env = _lang_env("ruby")
    bundle = str(_TOOLS / "ruby" / "bin" / "bundle.bat")
    # Prefer precompiled Windows binary gems over source where they exist --
    # cheap and idempotent, so fine to run on every call/worktree (a fresh
    # worktree re-checks-out the tracked Gemfile.lock, so this can't be a
    # one-time fix in the base clone).
    sh([bundle, "lock", "--add-platform", "x64-mingw-ucrt"], cwd=wt, timeout=120, env=env)
    # A task's OWN :benchmarks/:tools/:development/:coverage Gemfile groups
    # (Rails, markdown renderers, linters, ...) are the project's internal
    # tooling, not anything `rspec` needs to run -- pulling them in was
    # dragging nokogiri->racc into a real native C compile for no reason.
    # Excluding groups that don't exist is a no-op, so this is safe to pass
    # unconditionally across every Ruby task.
    sh([bundle, "config", "set", "--local", "without", "benchmarks tools development coverage"],
       cwd=wt, timeout=60, env=env)
    inst = sh([bundle, "install", "--quiet"], cwd=wt, timeout=900, env=env)
    if inst.returncode != 0:
        (RESULTS / "last_build_fail.txt").write_text((inst.stdout or "") + (inst.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(bundle install failed)", "collect_error": True}
    report = wt / "_rspec_report.json"
    report.unlink(missing_ok=True)
    cmd = [bundle, "exec", "rspec", "--format", "json", "--out", str(report)]
    if target:
        cmd.append(target)
    sh(cmd, cwd=wt, timeout=900, env=env)
    if not report.exists():
        return {"failures": set(), "summary": "(rspec produced no report)", "collect_error": True}
    data = json.loads(report.read_text(encoding="utf-8"))
    failures = {e["full_description"] for e in data.get("examples", [])
                if e.get("status") == "failed"}
    summ = data.get("summary_line", "(no summary)")
    total = data.get("summary", {}).get("example_count", 0)
    return {"failures": failures, "summary": summ, "collect_error": total == 0}


def run_jest(task: dict, wt: Path, target: str) -> dict:
    """JS via jest --json. Failures keyed file::fullName -- stable between the
    baseline and a post-agent run. `target` is a test file; regression is scoped to
    that same file (the full ~90-file suite is timezone-flaky), the js analog of the
    c++ "reuse the target binary" caveat."""
    jest = wt / "node_modules" / "jest" / "bin" / "jest.js"
    report = wt / "_jest_report.json"
    report.unlink(missing_ok=True)
    cmd = ["node", str(jest), "--ci", "--json", f"--outputFile={report}"]
    if target:
        cmd.append(target)
    proc = sh(cmd, cwd=wt, timeout=1200, env=_lang_env("javascript"))
    if not report.exists():
        (RESULTS / "last_build_fail.txt").write_text((proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(jest produced no report)", "collect_error": True}
    data = json.loads(report.read_text(encoding="utf-8"))
    failures, total = set(), 0
    for tr in data.get("testResults", []):
        fname = Path(tr.get("name", "")).name
        assertions = tr.get("assertionResults", [])
        for a in assertions:
            total += 1
            if a.get("status") == "failed":
                failures.add(f"{fname}::{a.get('fullName') or a.get('title')}")
        # A file that fails to even RUN (a TS type error, a syntax error, a
        # throw at import time) reports status "failed" with ZERO assertionResults
        # -- no individual test ever started, so the loop above sees nothing.
        # Surfacing that as a real failure (not collect_error) matters: it's
        # exactly what a broken build/typecheck looks like, and treating it as
        # "0 run" would make baseline() read a compile-breaking bug as passing.
        if not assertions and tr.get("status") == "failed":
            total += 1
            failures.add(f"{fname}::<suite failed to run>")
    return {"failures": failures, "summary": f"{total} run, {len(failures)} failed",
            "collect_error": total == 0}


def run_jasmine(task: dict, wt: Path, target: str) -> dict:
    """JS via the `jasmine` CLI (not jest) -- older projects still on Jasmine's
    own runner. No JSON reporter without writing a custom one, so this parses
    the console output directly: numbered failure headers ("N) describe it")
    give named, stable-across-runs failure ids, and the closing "N specs, M
    failures" line is the ground truth for total/collect_error. `target` is a
    whitespace-separated list of spec file paths (jasmine takes several
    positionally), empty = whatever jasmine.json's spec_files glob covers."""
    jasmine = wt / "node_modules" / ".bin" / "jasmine.cmd"
    cmd = [str(jasmine), "--config=jasmine.json", *target.split()] if target else \
          [str(jasmine), "--config=jasmine.json"]
    proc = sh(cmd, cwd=wt, timeout=600, env=_lang_env("javascript"))
    out = (proc.stdout or "") + (proc.stderr or "")
    summary = re.search(r"(\d+) specs?, (\d+) failures?", out)
    if summary is None:
        (RESULTS / "last_build_fail.txt").write_text(out[-4000:], encoding="utf-8")
        return {"failures": set(), "summary": "(jasmine produced no summary)", "collect_error": True}
    n_fail = int(summary.group(2))
    named = set(re.findall(r"^\d+\)\s+(.+)$", out, re.M))
    failures = named if n_fail else set()
    if n_fail and not named:
        failures = {"<jasmine run>"}   # summary counted failures but the header regex missed them
    return {"failures": failures, "summary": summary.group(0), "collect_error": False}


def run_pnpm_vitest(task: dict, wt: Path, target: str) -> dict:
    """TypeScript/JS via pnpm + vitest, for a pnpm-WORKSPACE repo (multiple
    packages/*, its own lockfile) -- too structurally different from a plain
    single-package npm repo for _link_node_modules's one-directory junction
    (pnpm symlinks live inside each workspace package, not just the root), so
    this runs `pnpm install` fresh per worktree instead. Cheap after the
    first real worktree: pnpm's own content-addressable STORE (--store-dir,
    set to a persistent dir outside any worktree) is what's actually
    expensive to populate, and it's shared -- only the symlink relinking
    happens per worktree, not a redownload. Vitest's --reporter=json is
    jest-shaped (testResults[].assertionResults[]), so parsing mirrors
    run_jest exactly. `target` is a whitespace-separated list of spec files;
    task["vitest_project"] is passed as --project if set."""
    env = _lang_env("typescript")
    store = str(BENCH / ".pnpm-store")
    # "corepack" resolves to corepack.cmd on Windows -- subprocess with a list
    # arg (shell=False) skips cmd.exe's own PATHEXT resolution, so the bare
    # name 404s with WinError 2 unless the extension is explicit.
    corepack = "corepack.cmd" if platform.system() == "Windows" else "corepack"
    inst = sh([corepack, "pnpm", "install", "--frozen-lockfile", "--store-dir", store],
              cwd=wt, timeout=900, env=env)
    if inst.returncode != 0:
        (RESULTS / "last_build_fail.txt").write_text((inst.stdout or "") + (inst.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(pnpm install failed)", "collect_error": True}
    report = wt / "_vitest_report.json"
    report.unlink(missing_ok=True)
    cmd = [corepack, "pnpm", "vitest", "run", *(target.split() if target else [])]
    if task.get("vitest_project"):
        cmd += ["--project", task["vitest_project"]]
    cmd += ["--reporter=json", f"--outputFile={report}"]
    sh(cmd, cwd=wt, timeout=600, env=env)
    if not report.exists():
        return {"failures": set(), "summary": "(vitest produced no report)", "collect_error": True}
    data = json.loads(report.read_text(encoding="utf-8"))
    failures, total = set(), 0
    for tr in data.get("testResults", []):
        fname = Path(tr.get("name", "")).name
        assertions = tr.get("assertionResults", [])
        for a in assertions:
            total += 1
            if a.get("status") == "failed":
                failures.add(f"{fname}::{a.get('fullName') or a.get('title')}")
        if not assertions and tr.get("status") == "failed":
            total += 1
            failures.add(f"{fname}::<suite failed to run>")
    return {"failures": failures, "summary": f"{total} run, {len(failures)} failed",
            "collect_error": total == 0}


def run_dotnet(task: dict, wt: Path, target: str) -> dict:
    """C# via `dotnet test` (TFMs pinned to net8.0 in make_worktree so the net8 SDK
    can build). Failures parsed from the TRX report keyed by testName -- the
    surefire/JUnit analog. `target` is a --filter expression; empty => whole suite."""
    import xml.etree.ElementTree as ET
    ns = "{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}"
    trx_dir = wt / "_trx"
    shutil.rmtree(trx_dir, ignore_errors=True)
    trx_dir.mkdir(parents=True, exist_ok=True)
    proj = task.get("test_project", "")
    cmd = ["dotnet", "test", *([proj] if proj else []), "-c", "Release",
           "--logger", "trx;LogFileName=r.trx", "--results-directory", str(trx_dir)]
    if target:
        cmd += ["--filter", target]
    # Per-task MSBuild property overrides -- e.g. a repo written against a
    # newer C# language version than our SDK defaults to (LangVersion=preview),
    # or a repo whose CI treats warnings as errors more strictly than our
    # toolchain's baseline warns on. Makes the tree buildable here; the bug
    # itself is untouched, same spirit as _normalize_csharp_tfm.
    for prop in task.get("dotnet_props", []):
        cmd += [f"-p:{prop}"]
    proc = sh(cmd, cwd=wt, timeout=1800, env=_lang_env("csharp"))
    trx = next(iter(trx_dir.glob("*.trx")), None)
    if trx is None:
        (RESULTS / "last_build_fail.txt").write_text((proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
        return {"failures": set(), "summary": "(no trx -- build failed)", "collect_error": True}
    root = ET.parse(trx).getroot()
    failures, total = set(), 0
    for r in root.iter(f"{ns}UnitTestResult"):
        total += 1
        if (r.get("outcome") or "") == "Failed":
            failures.add(r.get("testName"))
    return {"failures": failures, "summary": f"{total} run, {len(failures)} failed",
            "collect_error": total == 0}


def run_tests(task: dict, wt: Path, target: str) -> dict:
    """Language dispatch -- all return the SAME {failures, summary, collect_error}
    shape, so the differential grading below is language-blind."""
    lang = task.get("lang", "python")
    if lang == "java":
        return run_maven(task, wt, target)
    if lang == "cpp":
        if task.get("cpp_test_framework") == "doctest":
            return run_ctest_doctest(task, wt, target)
        return run_ctest(task, wt, target)
    if lang == "c":
        if task.get("c_build") == "manual":
            return run_c_manual(task, wt, target)
        return run_ctest_c(task, wt, target)
    if lang == "rust":
        return run_cargo(task, wt, target)
    if lang == "csharp":
        return run_dotnet(task, wt, target)
    if lang in ("javascript", "typescript"):
        if task.get("js_test_framework") == "jasmine":
            return run_jasmine(task, wt, target)
        if task.get("js_test_framework") == "pnpm_vitest":
            return run_pnpm_vitest(task, wt, target)
        return run_jest(task, wt, target)
    if lang == "go":
        return run_go(task, wt, target)
    if lang == "ruby":
        return run_rspec(task, wt, target)
    return run_pytest(task, wt, target)


# -- worktrees ---------------------------------------------------------------
def make_worktree(task: dict, name: str, buggy: bool) -> Path:
    """Fresh checkout at the fix commit. buggy=True reverts the source half, which
    is the state an arm actually works in; buggy=False is the baseline used to
    learn which tests were already failing in this environment."""
    wt = BENCH / "wt" / name
    drop_worktree(task, wt)
    wt.parent.mkdir(parents=True, exist_ok=True)
    add = sh(["git", "worktree", "add", "--quiet", "--detach", str(wt), task["fix"]],
             cwd=repo_dir(task))
    # CONFIRMED FAILURE MODE: a leftover non-empty `wt` (e.g. drop_worktree's
    # rmtree silently losing to a file locked by an orphaned process from a
    # prior run) makes `git worktree add` fail with returncode 128 ("already
    # exists") while wt.exists() stays True throughout -- checking existence
    # alone let this slip through and silently hand an agent a stale,
    # possibly-already-edited worktree instead of a fresh one at the fix
    # commit. Check the actual exit code too.
    if add.returncode != 0 or not wt.exists():
        raise RuntimeError(f"worktree add failed for {wt}: {add.stderr.strip()[:300]}")
    if buggy:
        sh(["git", "checkout", task["parent"], "--", *task["source_files"]], cwd=wt)
    # Some fix commits change only source (no regression test). inject_files writes
    # the pinning test into EVERY worktree (buggy, fixed baseline, and the agent's),
    # so the differential grader has a fail_to_pass to measure.
    for rel, content in task.get("inject_files", {}).items():
        p = wt / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    # Literal find/replace patches applied to EVERY worktree, unconditionally --
    # for SDK/compiler-compat fixes in files that aren't the bug and aren't the
    # regression test (e.g. an unrelated test-infra call that's ambiguous under
    # our toolchain's Roslyn version but not the repo's own pinned SDK).
    for rel, pairs in task.get("text_patches", {}).items():
        p = wt / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8-sig")
        for old, new in pairs:
            s = s.replace(old, new)
        p.write_text(s, encoding="utf-8")
    lang = task.get("lang", "python")
    if lang == "csharp":
        _normalize_csharp_tfm(wt)      # pin TFMs so the net8 SDK can build
        if task.get("csharp_drop_global_json"):
            # global.json pinning a newer SDK major version (with
            # rollForward: latestMinor, which won't roll DOWN to net8) makes
            # `dotnet` refuse to build at all with our SDK. Removing it just
            # falls back to whatever SDK IS installed -- doesn't touch the bug.
            (wt / "global.json").unlink(missing_ok=True)
        if task.get("csharp_project_langversion"):
            _apply_csharp_langversion(wt, task["csharp_project_langversion"])
    if lang in ("javascript", "typescript") and task.get("js_test_framework") != "pnpm_vitest":
        # pnpm workspaces (zod-style) install fresh per worktree instead --
        # see run_pnpm_vitest -- a junctioned node_modules here would collide
        # with pnpm's own per-package symlinks and the shared install below.
        _link_node_modules(task, wt)   # junction the shared node_modules in
    return wt


def drop_worktree(task: dict, wt: Path) -> None:
    """git worktree commands must run inside the REPO, not the bench folder --
    running them from a non-repo cwd fails silently, leaving the path still
    REGISTERED after the directory is deleted ("prunable"), and the next add with
    that name collides. prune afterwards clears any such stale registration."""
    repo = repo_dir(task)
    if wt.exists():
        sh(["git", "worktree", "remove", "--force", str(wt)], cwd=repo)
        shutil.rmtree(wt, ignore_errors=True)
        if wt.exists():
            # CONFIRMED: a file locked by an orphaned process from a previous
            # run (we've hit stray cargo/dotnet/go processes doing exactly
            # this) can survive rmtree even with ignore_errors=True. Silently
            # continuing past that used to let the NEXT make_worktree() reuse
            # this same dirty directory -- an agent starting from whatever a
            # PRIOR run left behind instead of a fresh checkout. Fail loud
            # instead of handing out a stale worktree.
            raise RuntimeError(
                f"could not fully remove {wt} -- a file is likely still locked "
                f"by an orphaned process from a previous run; find and kill it "
                f"(check for stray cargo/dotnet/go/node processes) before retrying")
    sh(["git", "worktree", "prune"], cwd=repo)


def _normalize_csharp_tfm(wt: Path) -> None:
    """The net8 SDK can't target net9.0, and these repos multi-target
    (net9.0;net8.0;net48;...); pin every csproj to net8.0 so a plain `dotnet build`/
    `dotnet test` works for the AGENT (which won't know a -f/-p override) and the
    grader alike. Doesn't touch the bug -- purely makes the tree buildable here."""
    import re as _re
    for f in wt.rglob("*.csproj"):
        s = f.read_text(encoding="utf-8-sig"); o = s
        s = _re.sub(r"<TargetFrameworks>.*?</TargetFrameworks>",
                    "<TargetFrameworks>net8.0</TargetFrameworks>", s, flags=_re.S)
        s = _re.sub(r"<TargetFramework>(?!net8\.0<).*?</TargetFramework>",
                    "<TargetFramework>net8.0</TargetFramework>", s, flags=_re.S)
        if s != o:
            f.write_text(s, encoding="utf-8")


def _apply_csharp_langversion(wt: Path, overrides: dict) -> None:
    """Some projects need a newer LangVersion than our SDK defaults to (e.g. the
    C# 13 Lock pattern), but forcing that onto the WHOLE build graph via a global
    -p:LangVersion CLI property also reaches sibling/test projects that don't
    need it and can change their overload resolution in surprising ways. Instead
    patch just the named .csproj files, keyed by path relative to the worktree
    root, by injecting a scoped <LangVersion> into their first <PropertyGroup>."""
    import re as _re
    for rel, ver in overrides.items():
        f = wt / rel
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8-sig")
        s2 = _re.sub(r"(<PropertyGroup>)", rf"\1\n    <LangVersion>{ver}</LangVersion>",
                     s, count=1)
        if s2 != s:
            f.write_text(s2, encoding="utf-8")


def _link_node_modules(task: dict, wt: Path) -> None:
    """node resolves node_modules from the cwd upward, but the worktree lives outside
    the base repo, so junction the base repo's installed node_modules into it
    (installed once, like python's shared .venv). Junctions need no admin on Windows."""
    base = repo_dir(task) / "node_modules"
    dest = wt / "node_modules"
    if base.exists() and not dest.exists():
        sh(["cmd", "/c", "mklink", "/J", str(dest), str(base)])


# -- the arms ----------------------------------------------------------------
def mcp_config(task: dict, wt: Path) -> Path:
    """Point the MCP server at the worktree the agent is editing -- the index must
    describe the code under the agent's hands, not the pristine clone."""
    cfg = wt.parent / f"mcp_{wt.name}.json"
    cfg.write_text(json.dumps({"mcpServers": {"benzi": {
        "command": str(BENZI_PY), "args": [str(BENZI_MCP), str(wt)]}}}), encoding="utf-8")
    return cfg


# Anthropic per-token pricing (USD / token), Sonnet 5 -- used only to give the
# benzi_product arm a cost figure comparable to Claude Code's own total_cost_usd
# (which the CLI computes itself; agentchat only tracks raw token COUNTS).
SONNET5_PRICE = {"input": 3e-6, "output": 15e-6, "cache_read": 0.3e-6, "cache_write": 3.75e-6}
# deepseek-v4-flash published rates (USD/token). ESTIMATED -- same caveat as the
# Sonnet estimate; V4 (2026) rates move, so CONFIRM against the DeepSeek console
# before quoting a cost. The raw token COUNTS in each row are exact regardless,
# so a wrong rate here is a one-line recompute, never a re-run. Cache hit is far
# cheaper than miss; a miss is billed at the input rate (no separate write fee).
DEEPSEEK_PRICE = {"input": 0.28e-6, "output": 1.14e-6, "cache_read": 0.028e-6, "cache_write": 0.28e-6}
# Claude Haiku 4.5 -- Anthropic's published rates (stable, unlike the DeepSeek
# estimate). Anthropic input_tokens EXCLUDE cache, so the non-deepseek branch of
# the cost calc bills them correctly.
HAIKU5_PRICE = {"input": 1e-6, "output": 5e-6, "cache_read": 0.1e-6, "cache_write": 1.25e-6}
# OpenRouter cheap-model rows for the family bake-off (per-token, from OpenRouter
# $/M). No separate cache tier exposed -> cache prices = input (no false discount).
GLM_FLASH_PRICE  = {"input": 0.06e-6, "output": 0.40e-6, "cache_read": 0.06e-6, "cache_write": 0.06e-6}
QWEN_NEXT_PRICE  = {"input": 0.11e-6, "output": 0.80e-6, "cache_read": 0.11e-6, "cache_write": 0.11e-6}
QWEN_CODER_PRICE = {"input": 0.30e-6, "output": 1.00e-6, "cache_read": 0.30e-6, "cache_write": 0.30e-6}
QWEN_FLASH_PRICE = {"input": 0.20e-6, "output": 0.97e-6, "cache_read": 0.20e-6, "cache_write": 0.20e-6}
QWEN_30B_PRICE   = {"input": 0.07e-6, "output": 0.27e-6, "cache_read": 0.07e-6, "cache_write": 0.07e-6}
CODESTRAL_PRICE  = {"input": 0.30e-6, "output": 0.90e-6, "cache_read": 0.30e-6, "cache_write": 0.30e-6}
# MID-TIER arms (>$1/M out, still < Sonnet). Same no-cache caveat: cache = input.
GLM_FULL_PRICE   = {"input": 0.40e-6, "output": 1.75e-6, "cache_read": 0.40e-6, "cache_write": 0.40e-6}
DEVSTRAL_PRICE   = {"input": 0.40e-6, "output": 2.00e-6, "cache_read": 0.40e-6, "cache_write": 0.40e-6}
KIMI_K2_PRICE    = {"input": 0.57e-6, "output": 2.30e-6, "cache_read": 0.57e-6, "cache_write": 0.57e-6}
# deepseek-v4-flash via OpenRouter (OpenRouter's own $/M, cache=input: no caching).
DEEPSEEK_OR_PRICE = {"input": 0.14e-6, "output": 0.28e-6, "cache_read": 0.14e-6, "cache_write": 0.14e-6}
# Qwen via DashScope-direct (US). Tiered by context length; these are the 0-32K base
# tier (compaction keeps our loop in the cheap tiers). Auto-caches -> cache_read is
# an ESTIMATE (~0.4x input) pending the exact DashScope rate; recompute from real
# tokens if it matters. Output is the driver here and is never cached.
QWEN_FLASH_DS_PRICE = {"input": 0.30e-6, "output": 1.50e-6, "cache_read": 0.12e-6, "cache_write": 0.30e-6}
QWEN_PLUS_DS_PRICE  = {"input": 1.00e-6, "output": 5.00e-6, "cache_read": 0.40e-6, "cache_write": 1.00e-6}
BENZI_PRICE = {"sonnet": SONNET5_PRICE, "deepseek": DEEPSEEK_PRICE, "haiku": HAIKU5_PRICE,
               "glm": GLM_FLASH_PRICE, "qwen-next": QWEN_NEXT_PRICE, "qwen": QWEN_CODER_PRICE,
               "qwen-flash": QWEN_FLASH_PRICE, "qwen-30b": QWEN_30B_PRICE, "codestral": CODESTRAL_PRICE,
               "glm-full": GLM_FULL_PRICE, "devstral": DEVSTRAL_PRICE, "kimi-k2": KIMI_K2_PRICE,
               "deepseek-or": DEEPSEEK_OR_PRICE,
               "qwen-flash-direct": QWEN_FLASH_DS_PRICE, "qwen-plus-direct": QWEN_PLUS_DS_PRICE}

# Experimental variants for the benzi_product arm: preset env that ablates a
# tool or nudges the prompt (via ChatSession's BENZI_DISABLE_TOOLS /
# BENZI_PROMPT_EXTRA hooks). Each run self-documents which knob was on.
BENZI_VARIANTS = {
    "": {},
    "nogrep": {"BENZI_DISABLE_TOOLS": "benzi_grep"},   # kept (inert unless selected); grepsteer removed -- steering didn't move the model
    "paceon":  {"BENZI_PACE": "1"},   # "MOVE EFFICIENTLY" addendum ON  -- A/B treatment
    "paceoff": {"BENZI_PACE": "0"},   # "MOVE EFFICIENTLY" addendum OFF -- A/B control
    "notestcase": {"BENZI_DISABLE_TOOLS": "execute_generated_testcase"},  # nudge live, dedicated tool OFF -- can it self-debug via shell?
}


@contextlib.contextmanager
def _hidden_git_history(task: dict, wt: Path):
    """INTEGRITY, for real this time: hiding wt/.git alone was NOT enough --
    CONFIRMED EXPLOITED. wt/.git for a worktree is just a pointer FILE, so
    renaming it away only blocks git commands run FROM INSIDE the worktree.
    An agent's shell can cd anywhere, and the BASE REPO CLONE (repo_dir(task))
    sits right next to every worktree under BENCH with its own untouched,
    complete .git -- a control run `cd`'d there and ran `git show <fix-sha>`
    to read the real patch instead of finding the bug. Both are hidden now,
    both restored in `finally` even on a timeout. Safe under the sequential-
    only execution model this harness already requires -- nothing else
    touches this repo's .git while one arm's turn is in flight."""
    targets = [wt / ".git", repo_dir(task) / ".git"]
    moved = []
    for gitref in targets:
        hidden = gitref.parent / (gitref.name + "__hidden_during_run")
        if gitref.exists():
            try:
                gitref.rename(hidden)
                moved.append((gitref, hidden))
            except OSError:
                pass
    try:
        yield
    finally:
        for gitref, hidden in moved:
            try:
                hidden.rename(gitref)
            except OSError:
                pass


AIDER_PY = BENCH / ".aider-venv" / "Scripts" / "aider.exe"
# aider names models provider-first; ours is the same DeepSeek endpoint the
# benzi arm uses, so the model variable is held fixed across the two.
AIDER_MODELS = {"deepseek": "deepseek/deepseek-chat",
                "sonnet": "anthropic/claude-sonnet-5"}   # match benzi's alias, not 4-5


def _rmtree_readonly(path: Path) -> None:
    """rmtree that survives git's read-only object files (Windows)."""
    def _clear(func, p, _exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except OSError:
            pass
    if path.exists():
        shutil.rmtree(path, onerror=_clear)


def _fresh_git_repo(wt: Path) -> None:
    """Give the worktree its OWN one-commit repo containing the BUGGY state.

    Aider will not run without git and commits what it changes. The other arms
    get .git hidden; that would simply break aider. A fresh repo whose only
    commit IS the buggy tree gives it working git with nothing to mine: no fix
    commit, no upstream history, no remote.
    """
    gitref = wt / ".git"
    if gitref.is_dir():
        _rmtree_readonly(gitref)
    elif gitref.exists():
        gitref.unlink()
    sh(["git", "init", "-q"], cwd=wt)
    sh(["git", "config", "user.email", "bench@local"], cwd=wt)
    sh(["git", "config", "user.name", "bench"], cwd=wt)
    sh(["git", "add", "-A"], cwd=wt)
    sh(["git", "commit", "-q", "-m", "buggy state"], cwd=wt)


def _aider_test_cmd(task: dict, wt: Path) -> str | None:
    """The shell command aider should run after each edit, per language.

    Mirrors run_tests()'s invocation so aider iterates against the SAME signal
    the grader uses. Returns None where a one-line command isn't meaningful, in
    which case aider runs unverified and the row must be read as such.
    """
    lang = task.get("lang", "python")
    target = task.get("regression_tests") or task.get("target_tests") or ""
    if lang == "python":
        return f'"{venv_py(task)}" -m pytest {target} -q --no-header'.strip()
    if lang == "rust":
        return "cargo test"
    if lang == "go":
        return "go test ./..."
    if lang == "java":
        sel = f" -Dtest={target}" if target else ""
        return f"mvn -q -B test{sel}"
    if lang == "ruby":
        return f"bundle exec rspec {target}".strip()
    if lang in ("javascript", "typescript"):
        return "npm test"
    if lang == "csharp":
        return "dotnet test -c Release"
    return None   # c / c++ build via cmake+ctest -- not a single portable line


def run_aider(task: dict, wt: Path, issue: str, model: str = "deepseek",
              lang: str = "python") -> dict:
    """Third-party arm. Same issue text, same worktree, same grader."""
    if not AIDER_PY.exists():
        return {"error": f"aider not installed at {AIDER_PY}"}
    _fresh_git_repo(wt)
    prompt = (f"{issue}\n\nThe repository is at the current working directory. "
              f"Find and fix the bug. Do not modify any test files.")
    env = _lang_env(lang) or dict(os.environ)
    # aider reads DEEPSEEK_API_KEY / ANTHROPIC_API_KEY from the environment,
    # the same keys the other arms use -- nothing extra to configure.
    cmd = [str(AIDER_PY), "--model", AIDER_MODELS.get(model, model),
           "--message", prompt, "--yes-always", "--no-stream",
           "--no-analytics", "--no-check-update", "--no-auto-commits"]
    # Aider has no shell tool -- it cannot choose to run the suite the way the
    # other arms do. --auto-test defaults to False, so without this it makes one
    # edit and exits, and its wall time measures "first plausible edit" rather
    # than "verified fix". Passing the task's own test command puts it on the
    # same footing: edit, run, read the failure, iterate.
    test_cmd = _aider_test_cmd(task, wt)
    if test_cmd:
        cmd += ["--auto-test", "--test-cmd", test_cmd]
    t0 = time.time()
    proc = sh(cmd, cwd=wt, timeout=2400, env=env)
    wall = time.time() - t0
    out = (proc.stdout or "") + (proc.stderr or "")
    # aider prints a running cost line: "Tokens: 12k sent, 500 received. Cost: $0.0123 message, $0.0456 session."
    # aider wraps its cost line, so "$0.0025 \nsession." -- allow any whitespace
    costs = re.findall(r"\$([0-9.]+)\s+session", out)
    cost = float(costs[-1]) if costs else 0.0
    # it has no turn concept; count its edit rounds as the closest analogue
    turns = out.count("Applied edit to") or out.count("SEARCH/REPLACE")
    # Remove the standalone repo we created. Git's objects are read-only on
    # Windows, so drop_worktree's plain rmtree would fail here and kill the run
    # AFTER the work was done, losing the row. The agent's file edits stay --
    # only .git goes -- so the grader still sees exactly what aider wrote.
    _rmtree_readonly(wt / ".git")
    return {"wall_s": wall, "cost_usd": cost, "num_turns": turns,
            "tool_calls": turns, "tools": {}, "benzi_calls": 0,
            "aider_verified": bool(test_cmd),   # False = edit-only, not comparable
            "raw_tail": out[-800:]}


# Use the REAL binary the npm package ships, never the opencode.cmd shim next
# to it. A .cmd is executed by cmd.exe, which parses the prompt we pass as a
# command line -- so an issue containing < > & | dies before opencode starts
# ("< was unexpected at this time", MEASURED on jsoup, and 5 of 26 tasks carry
# one of those characters). The .exe is exec'd directly, no interpreter, no
# metacharacter parsing.
_OC_EXE = (Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules"
           / "opencode-ai" / "bin" / "opencode.exe")
OPENCODE_BIN = _OC_EXE if _OC_EXE.exists() else (
    Path(os.environ.get("APPDATA", "")) / "npm" / "opencode.cmd")
# opencode names models provider/model. "deepseek" here is deepseek-v4-flash at
# api.deepseek.com -- byte-identical to what OPENAI_MODELS["deepseek"] gives
# benzi_product, which is the whole point of this arm.
# These MUST name the same generation agentchat.py's OPENAI_MODELS/ANTHROPIC
# aliases resolve to, or the arms are not running the same model and the whole
# comparison is void: benzi's "sonnet" is claude-sonnet-5, NOT claude-sonnet-4-5.
OPENCODE_MODELS = {"deepseek": "deepseek/deepseek-v4-flash",
                   "deepseek-pro": "deepseek/deepseek-v4-pro",
                   "sonnet": "anthropic/claude-sonnet-5"}


def run_opencode(task: dict, wt: Path, issue: str, model: str = "deepseek",
                 lang: str = "python") -> dict:
    """Third-party agentic control. Same issue text, same worktree, same grader."""
    if not OPENCODE_BIN.exists():
        return {"error": f"opencode not installed at {OPENCODE_BIN}"}
    prompt = (f"{issue}\n\nThe repository is at the current working directory. "
              f"Find and fix the bug. Do not modify any test files.")
    env = _lang_env(lang) or dict(os.environ)
    cmd = [str(OPENCODE_BIN), "run",
           "--model", OPENCODE_MODELS.get(model, model),
           "--format", "json",   # one JSON event per line: tool_use / step_finish
           "--auto",             # auto-approve permissions; without it, it blocks
           "--pure",             # no external plugins, so runs stay reproducible
           prompt]
    t0 = time.time()
    with _hidden_git_history(task, wt):
        # stdin MUST be DEVNULL. With an inherited stdin opencode finishes the
        # work and then never exits -- MEASURED: 16.6s of real work followed by
        # a hang until the timeout killed it. Closing stdin makes it exit 0
        # immediately. This is the single thing that makes the arm usable.
        proc = subprocess.run(cmd, cwd=wt, capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              timeout=2400, env=env, stdin=subprocess.DEVNULL)
    wall = time.time() - t0

    (RESULTS / "transcripts").mkdir(parents=True, exist_ok=True)
    (RESULTS / "transcripts" / f"{wt.name}_opencode.jsonl").write_text(
        proc.stdout or "", encoding="utf-8")

    tools: dict[str, int] = {}
    turns = cost = 0
    inp = out = cr = cw = 0
    text_tail = ""
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = ev.get("part") or {}
        kind = ev.get("type")
        if kind == "tool_use":
            name = part.get("tool", "?")
            tools[name] = tools.get(name, 0) + 1
        elif kind == "step_start":
            # one step == one model call, the closest analogue to a "turn" in the
            # other arms (which count assistant messages the same way)
            turns += 1
        elif kind == "step_finish":
            cost += part.get("cost") or 0.0
            tk = part.get("tokens") or {}
            inp += tk.get("input") or 0
            out += tk.get("output") or 0
            cache = tk.get("cache") or {}
            cr += cache.get("read") or 0
            cw += cache.get("write") or 0
        elif kind == "text":
            text_tail = part.get("text") or text_tail
    if not turns and not tools:
        return {"error": "opencode produced no steps", "wall_s": wall,
                "raw": ((proc.stdout or "") + (proc.stderr or ""))[-600:]}
    # Price it with the SAME table benzi_product uses, or the cost columns are
    # not comparable: opencode reports its own per-step cost from models.dev
    # rates, which differ from our published-rate estimate (on mux: $0.012
    # self-reported vs $0.051 by our table, for the same model). Its own number
    # is kept alongside, not thrown away.
    # NB: unlike the DeepSeek API, opencode's tokens.input EXCLUDES cache reads
    # (measured: input=46 alongside cache.read=7424 in one step), so cache is
    # added here rather than subtracted the way run_arm does for deepseek.
    price = BENZI_PRICE.get(model, DEEPSEEK_PRICE)
    est = (inp * price["input"] + out * price["output"]
           + cr * price["cache_read"] + cw * price["cache_write"])
    # Record the model. Without it the row lands with model=None and every
    # later query that filters on model silently drops the arm -- which already
    # happened once while comparing mux runs.
    return {"model": model,
            "wall_s": wall, "cost_usd": round(est, 4), "cost_provider_usd": round(cost, 4),
            "num_turns": turns,
            "tool_calls": sum(tools.values()), "tools": tools, "benzi_calls": 0,
            "in_tokens": inp, "out_tokens": out,
            "cache_read": cr, "cache_write": cw,
            "result_text": text_tail[:2000],
            "raw_tail": (proc.stderr or "")[-400:]}


def run_arm(task: dict, wt: Path, arm: str, max_turns: int, benzi_model: str = "sonnet",
            variant: str = "", control_model: str = "sonnet") -> dict:
    """Arm FAMILIES:
      control / benzi / benzi_told  -- Claude Code (claude.exe), the index
        mounted as MCP tools ALONGSIDE its normal ones (optionally briefed).
        stream-json (not plain json) because the event stream is the only
        place the CLI exposes WHICH tools got called -- without that, a tie
        is unreadable: an agent that ignored the index and one that used it
        with no benefit look identical.
      benzi_only  -- Claude Code with Read/Grep/Glob/Edit/Write/Bash ALL
        denied -- the index isn't offered as an option alongside its normal
        tools, it's the ONLY option. Closes the exact gap benzi/benzi_told
        measured (benzi_calls=0 -- given a choice, the agent just grepped).
        Requires benzi_mcp's edit_lines/create_file (a real Read-deny also
        blocks Claude Code's own Edit on that path, so the fix has to be
        written through a tool the deny rule never touches).
      benzi_product  -- the PRODUCT itself (agentchat.ChatSession) via
        benzi_headless.py. Head-to-head against Claude Code: same model, same
        task, same repo, but the whole system (prompt/tools/edit loop/index),
        not an isolated variable."""
    if arm == "benzi_product":
        return run_benzi_product(task, wt, task["issue"], max_turns, benzi_model, variant,
                                 task.get("lang", "python"))
    if arm == "aider":
        return run_aider(task, wt, task["issue"], benzi_model,
                         task.get("lang", "python"))
    if arm == "opencode":
        return run_opencode(task, wt, task["issue"], benzi_model,
                            task.get("lang", "python"))

    prompt = (f"{task['issue']}\n\nThe repository is at the current working directory. "
              f"Find and fix the bug. Do not modify any test files.")
    cmd = [str(CLAUDE), "-p", prompt, "--model", control_model,
           "--output-format", "stream-json", "--verbose",
           "--permission-mode", "bypassPermissions"]
    # NO --max-turns: benzi_product's own --max-turns arg is parsed but never
    # enforced anywhere in agentchat.py -- it runs until it converges or the
    # shared 2400s wall-clock timeout below kills it. Passing --max-turns here
    # was a REAL, hard-enforced cap on Claude Code alone (confirmed: every
    # control run in this batch hit exactly 41 turns, wins and losses alike,
    # with terminal_reason=max_turns on the losses) -- an asymmetric ceiling
    # that made "faster wall-clock" wins possibly just "ran out of turns
    # sooner," not genuine speed. Dropping it makes both arms bounded by the
    # same 2400s wall-clock timeout and nothing else.
    if arm in ("benzi", "benzi_told", "benzi_only"):
        cmd += ["--mcp-config", str(mcp_config(task, wt)), "--strict-mcp-config"]
    if arm == "benzi_told":
        # MEASURED: with the tools merely PRESENT, adoption was 0 -- the agent
        # grepped past a resolved index it never touched. Claude Code's own prompt
        # describes its native tools at length while MCP tools arrive as bare
        # schemas, so this levels that up. It states what the index IS and when it
        # helps; it says nothing about this bug, this repo, or where to look.
        cmd += ["--append-system-prompt", INDEX_BRIEFING]
    if arm == "benzi_only":
        # No briefing here on purpose -- unlike benzi_told, this arm needs no
        # nudge toward preferring the index; there's nothing else left to
        # reach for. The tool list alone (mcp__benzi__* is all that remains)
        # is the treatment.
        cmd += ["--disallowedTools", "Read,Grep,Glob,Edit,Write,Bash",
                "--allowedTools", "mcp__benzi__*"]
    # Claude Code defers MCP tool schemas behind its OWN ToolSearch lookup by
    # default -- names load upfront, full schemas only load once ToolSearch
    # surfaces them, and that's a keyword match against tool name/description,
    # independent of --allowedTools/--disallowedTools entirely. MEASURED: a
    # benzi_only run called ToolSearch 16 times and never surfaced
    # edit_lines/create_file, then gave up and reported the fix as TEXT
    # instead of writing it. ENABLE_TOOL_SEARCH=false forces every MCP tool's
    # full schema to load immediately, no discovery step, no keyword-miss
    # risk -- applies to every arm that mounts the MCP server, not just this
    # one, since benzi/benzi_told's original benzi_calls=0 finding could be
    # this exact mechanism rather than a real preference.
    # Every arm gets the language toolchain on PATH (so Claude Code can build/test
    # too, not just Benzi). ENABLE_TOOL_SEARCH only matters to the MCP-mounting arms.
    base = _lang_env(task.get("lang", "python")) or dict(os.environ)
    if arm in ("benzi", "benzi_told", "benzi_only"):
        base = {**base, "ENABLE_TOOL_SEARCH": "false"}
    t0 = time.time()
    with _hidden_git_history(task, wt):
        proc = sh(cmd, cwd=wt, timeout=2400, env=base)
    wall = time.time() - t0

    # Persist the raw stream-json (every tool call, every result) so a postmortem
    # on a surprising solved=False doesn't have to re-run the arm to find out
    # WHY -- benzi_headless's own transcript isn't saved anywhere either, but that
    # one's harder to get at (it isn't stream-json); this is the cheap half of
    # the fix and covers exactly the case in front of us.
    (RESULTS / "transcripts").mkdir(parents=True, exist_ok=True)
    (RESULTS / "transcripts" / f"{wt.name}_{arm}.jsonl").write_text(
        proc.stdout or "", encoding="utf-8")

    tools: dict[str, int] = {}
    payload = None
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            payload = ev
        elif ev.get("type") == "assistant":
            for block in ((ev.get("message") or {}).get("content") or []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tools[block.get("name", "?")] = tools.get(block.get("name", "?"), 0) + 1
    if payload is None:
        return {"error": "no result event", "wall_s": wall,
                "raw": (proc.stdout or proc.stderr)[-600:]}
    u = payload.get("usage") or {}
    benzi_calls = sum(n for t, n in tools.items() if t.startswith("mcp__benzi__"))
    return {
        "model": control_model,              # claude.exe arm model (Sonnet unless --control-model)
        "wall_s": round(wall, 1),
        "duration_ms": payload.get("duration_ms"),
        "num_turns": payload.get("num_turns"),
        "cost_usd": payload.get("total_cost_usd"),
        "in_tokens": u.get("input_tokens"),
        "out_tokens": u.get("output_tokens"),
        "cache_read": u.get("cache_read_input_tokens"),
        "cache_write": u.get("cache_creation_input_tokens"),
        "is_error": payload.get("is_error"),
        "denials": len(payload.get("permission_denials") or []),
        "tool_calls": sum(tools.values()),
        "benzi_calls": benzi_calls,          # 0 here means the index was IGNORED
        "tools": tools,
        "result_text": (payload.get("result") or "")[:400],
    }


def run_benzi_product(task: dict, wt: Path, issue: str, max_turns: int, model: str = "sonnet",
                      variant: str = "", lang: str = "python") -> dict:
    prompt = (f"{issue}\n\nThe repository is at the current working directory. "
              f"Find and fix the bug. Do not modify any test files.")
    # Give the product the same compiler on PATH a real user would have, so its
    # edit gate can run g++ -fsyntax-only / javac to catch non-compiling edits.
    env = {**(_lang_env(lang) or os.environ), **BENZI_VARIANTS.get(variant, {})}
    t0 = time.time()
    with _hidden_git_history(task, wt):
        proc = sh([str(BENZI_PY), str(BENZI_HEADLESS), str(wt), prompt,
                  "--model", model, "--max-turns", str(max_turns)],
                  cwd=wt, timeout=2400, env=env)
    wall = time.time() - t0
    try:
        payload = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else {}
    except (json.JSONDecodeError, IndexError):
        return {"error": "unparseable benzi_headless output", "wall_s": wall,
                "raw": (proc.stdout or proc.stderr)[-600:]}

    # PERSIST THE TRACE -- one JSON line per tool call: turn, tool, FULL args,
    # and the tool's result. benzi_headless always returned this and the harness
    # always dropped it, leaving benzi the only arm with no record of what it
    # did; control and opencode both write one. Best-effort: a logging failure
    # must never fail the run it is describing.
    try:
        (RESULTS / "transcripts").mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(e, default=str, ensure_ascii=False)
                 for e in (payload.get("trace") or [])]
        (RESULTS / "transcripts" / (wt.name + "_benzi.jsonl")).write_text(
            chr(10).join(lines), encoding="utf-8")
    except OSError:
        pass
    if payload.get("is_error"):
        return {"error": payload.get("error", "benzi_headless raised"), "wall_s": wall}
    u = payload.get("usage") or {}
    price = BENZI_PRICE.get(model, SONNET5_PRICE)
    inp = u.get("input_tokens", 0)
    cr = u.get("cache_read_tokens", 0)
    # PROVIDER DIFFERENCE that bit us: DeepSeek's prompt_tokens INCLUDE the cache
    # hits, Anthropic's input_tokens EXCLUDE them. So the uncached input we bill
    # at the miss rate is (input - cache_read) for DeepSeek but plain input for
    # Anthropic -- otherwise a cached token is charged at full price AND again at
    # the cache rate (on this task that was a 9x overstatement: $3.94 vs ~$0.42).
    uncached = (inp - cr) if model.startswith("deepseek") else inp
    cost = (max(uncached, 0) * price["input"]
            + cr * price["cache_read"]
            + u.get("output_tokens", 0) * price["output"]
            + u.get("cache_write_tokens", 0) * price["cache_write"])
    return {
        "model": model,
        "variant": variant,
        "wall_s": round(wall, 1),
        "duration_ms": payload.get("duration_ms"),
        "num_turns": payload.get("num_turns"),
        "cost_usd": round(cost, 4),          # ESTIMATED from published per-token
                                              # pricing, not CLI-reported like the
                                              # other arms -- flagged, not hidden
        "in_tokens": u.get("input_tokens"),
        "out_tokens": u.get("output_tokens"),
        "cache_read": u.get("cache_read_tokens"),
        "cache_write": u.get("cache_write_tokens"),
        "is_error": False,
        "denials": 0,
        "tool_calls": payload.get("tool_calls"),
        "benzi_calls": payload.get("benzi_calls"),
        "source_lines_read": payload.get("source_lines_read"),
        # Cold start: building the index for this repo, paid on EVERY
        # run here because every task gets a fresh worktree. In the product it is
        # paid once per repo and cached in .benzi. Recorded separately so wall
        # time can be reported with and without it -- neither number alone is the
        # honest one: with it overstates steady-state cost, without it hides a
        # real first-run wait.
        "index_build_ms": payload.get("index_build_ms"),
        "tools": payload.get("tools"),
        "result_text": (payload.get("result") or "")[:400],
    }


# -- grading -----------------------------------------------------------------
def baseline(task: dict) -> dict:
    """Cache the two reference points per task: which tests fail at the FIX commit
    (environment noise we must forgive) and which fail with the bug present
    (the ones an arm has to turn green)."""
    cache = RESULTS / f"baseline_{task['fix']}.json"
    if cache.exists():
        d = json.loads(cache.read_text())
        return {k: set(v) if isinstance(v, list) else v for k, v in d.items()}
    fixed = make_worktree(task, "baseline_fixed", buggy=False)
    f_t = run_tests(task, fixed, task["target_tests"])
    f_r = run_tests(task, fixed, task["regression_tests"])
    drop_worktree(task, fixed)
    bug = make_worktree(task, "baseline_buggy", buggy=True)
    b_t = run_tests(task, bug, task["target_tests"])
    drop_worktree(task, bug)
    env_broken = f_t["failures"] | f_r["failures"]      # already red before anything
    f2p = b_t["failures"] - env_broken                  # the bug's own signature
    out = {"env_broken": env_broken, "fail_to_pass": f2p,
           "regression_ok": f_r["failures"]}
    RESULTS.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({k: sorted(v) for k, v in out.items()}, indent=1))
    return out


def grade(task: dict, wt: Path, base: dict) -> dict:
    t = run_tests(task, wt, task["target_tests"])
    r = run_tests(task, wt, task["regression_tests"])
    now = t["failures"] | r["failures"]
    still_failing = base["fail_to_pass"] & now              # bug not actually fixed
    newly_broken = now - base["env_broken"] - base["fail_to_pass"]   # collateral damage
    # MEASURED, real false positive: an arm that gave up mid-task (hit a
    # transient tool error, never wrote a fix) left pytest with NOTHING to
    # collect -- zero "FAILED" lines to regex-match is indistinguishable from
    # "everything passed" unless collection itself is checked. A run that
    # never produced a real pass/fail summary line, or that pytest flagged as
    # a collection error, can never be trusted as solved, however empty
    # still_failing/newly_broken came out.
    grading_ok = not t["collect_error"] and not r["collect_error"] and t["summary"] != "(no summary)"
    return {
        "f2p_total": len(base["fail_to_pass"]),
        "f2p_fixed": len(base["fail_to_pass"]) - len(still_failing),
        "regressions": len(newly_broken),
        "solved": grading_ok and not still_failing and not newly_broken,
        "grading_ok": grading_ok,
        "newly_broken_sample": sorted(newly_broken)[:3],
        "target_summary": t["summary"],
    }


# -- driver ------------------------------------------------------------------
def one_run(task_name: str, arm: str, trial: int, max_turns: int,
            benzi_model: str = "sonnet", variant: str = "", control_model: str = "sonnet") -> dict:
    task = TASKS[task_name]
    base = baseline(task)
    # Include the model in the worktree name: parallel benzi_product runs that
    # differ ONLY by --benzi-model would otherwise share one worktree path and
    # stomp each other's .git (the hide/restore dance collides).
    wt = make_worktree(task, f"{task_name}_{arm}_{benzi_model}{('_'+variant) if variant else ''}_{trial}", buggy=True)
    try:
        metrics = run_arm(task, wt, arm, max_turns, benzi_model, variant, control_model)
        scores = {} if "error" in metrics else grade(task, wt, base)
        row = {"task": task_name, "arm": arm, "trial": trial,
               "ts": datetime.now().isoformat(timespec="seconds"), **metrics, **scores}
    finally:
        drop_worktree(task, wt)
    RESULTS.mkdir(parents=True, exist_ok=True)
    # BENCH_RUNS_FILE lets a parallel run write to its own jsonl (no append
    # collision with a concurrent harness), merged back later.
    runs_file = Path(os.environ.get("BENCH_RUNS_FILE") or (RESULTS / "runs.jsonl"))
    with runs_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, default=str) + "\n")
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="sqlglot_7920", choices=list(TASKS))
    # control vs benzi_product is the honest head-to-head: two complete agents,
    # same model. The MCP arms (benzi/benzi_told/benzi_only) are opt-in
    # diagnostics -- Claude Code mostly ignored a merely-mounted index.
    ap.add_argument("--arms", nargs="+", default=["control", "benzi_product"])
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--benzi-model", default="sonnet",
                    help="model for the benzi_product arm (e.g. deepseek = deepseek-v4-flash)")
    ap.add_argument("--control-model", default="sonnet",
                    help="model alias for the claude.exe control/benzi arms (default sonnet; "
                         "e.g. haiku to run Claude Code on Haiku)")
    ap.add_argument("--variant", default="", choices=list(BENZI_VARIANTS),
                    help="benzi_product experiment knob: nogrep (drop grep) / grepsteer (nudge "
                         "the prompt to use the index) / '' (as shipped)")
    ap.add_argument("--baseline-only", action="store_true")
    args = ap.parse_args()

    if args.baseline_only:
        b = baseline(TASKS[args.task])
        print(f"fail_to_pass ({len(b['fail_to_pass'])}):")
        for f in sorted(b["fail_to_pass"]):
            print("   ", f)
        print(f"env_broken (forgiven): {len(b['env_broken'])}")
        return

    for trial in range(1, args.trials + 1):
        for arm in args.arms:
            row = one_run(args.task, arm, trial, args.max_turns, args.benzi_model, args.variant,
                          args.control_model)
            flag = "" if row.get("grading_ok", True) else "  ** GRADING INCONCLUSIVE -- pytest never produced a real summary; do not trust solved/f2p **"
            print(f"[{row['task']} {arm} #{trial}] solved={row.get('solved')} "
                  f"f2p={row.get('f2p_fixed')}/{row.get('f2p_total')} "
                  f"regressions={row.get('regressions')} "
                  f"turns={row.get('num_turns')} wall={row.get('wall_s')}s "
                  f"cost=${row.get('cost_usd')} "
                  f"tools={row.get('tool_calls')} benzi={row.get('benzi_calls')}{flag}")


if __name__ == "__main__":
    main()
