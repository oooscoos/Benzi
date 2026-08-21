# Trajectory: sympy__sympy-12096

- model: deepseek-v4-flash (worker + verifier)
- turns: 20
- tool calls: 20
- source lines read: 201

## Tool-call sequence (recorded during inference)

- turn 1: `get_definition` sympy/core/function.py::Function._eval_evalf
- turn 1: `read_reference` languages
- turn 2: `read_source` sympy/core/function.py::Function._eval_evalf
- turn 3: `benzi_grep` 
- turn 3: `benzi_grep` sympy/utilities/tests
- turn 4: `read_source` sympy/core/tests/test_evalf.py::test_implemented_function_ev
- turn 4: `read_source` sympy/utilities/lambdify.py::implemented_function
- turn 5: `read_source` sympy/core/evalf.py::EvalfMixin.evalf
- turn 6: `execute_generated_testcase` 
- turn 7: `shell` pip install mpmath 2>&1 | tail -2; python -c "import mpmath;
- turn 8: `shell` cat > /tmp/repro_evalf.py <<'EOF'
from sympy.utilities.lambd
- turn 9: `edit_lines` sympy/core/function.py
- turn 10: `shell` cd /testbed && python /tmp/repro_evalf.py 2>/dev/null && ech
- turn 11: `shell` cd /testbed && python -c "
from sympy.core.tests.test_evalf 
- turn 12: `shell` cd /testbed && python -c "
import sympy.utilities.tests.test
- turn 13: `shell` cd /testbed && python bin/test sympy/core/tests/test_evalf.p
- turn 14: `read_source` sympy/core/function.py::Function._eval_evalf
- turn 15: `shell` rm -f /tmp/repro_evalf.py && cd /testbed && git diff --stat
- turn 16: `shell` cd /testbed && git diff sympy/core/function.py
- turn 19: `shell` cd /testbed && git diff sympy/core/function.py

## Verifier

- verdict: revise
- critique: 

## Final patch

```diff
diff --git a/sympy/core/function.py b/sympy/core/function.py
index 1b8005e1d..8055236d5 100644
--- a/sympy/core/function.py
+++ b/sympy/core/function.py
@@ -507,7 +507,8 @@ def _eval_evalf(self, prec):
             func = getattr(mpmath, fname)
         except (AttributeError, KeyError):
             try:
-                return Float(self._imp_(*self.args), prec)
+                args = [arg.evalf(prec) for arg in self.args]
+                return Float(self._imp_(*args), prec)
             except (AttributeError, TypeError, ValueError):
                 return
 

```
