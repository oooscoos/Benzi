# Trajectory: django__django-15103

- model: deepseek-v4-flash (worker + verifier)
- turns: 26
- tool calls: 28
- source lines read: 139

## Tool-call sequence (recorded during inference)

- turn 1: `search_symbols` json_script
- turn 2: `read_source` django/utils/html.py::json_script
- turn 2: `read_source` django/template/defaultfilters.py::json_script
- turn 3: `get_callers` django/utils/html.py::json_script
- turn 3: `read_source` tests/utils_tests/test_html.py::TestUtilsHtml.test_json_scri
- turn 3: `read_source` tests/template_tests/filter_tests/test_json_script.py
- turn 4: `read_source` django/template/defaultfilters.py::json_script
- turn 4: `read_source` django/utils/html.py
- turn 5: `benzi_grep` django/template/defaultfilters.py
- turn 6: `edit_lines` django/utils/html.py
- turn 7: `edit_lines` django/template/defaultfilters.py
- turn 8: `execute_generated_testcase` 
- turn 9: `shell` ls tests/ | head -30; echo ---; ls *.txt *.cfg 2>/dev/null; 
- turn 10: `shell` python -V; pip install asgiref 2>&1 | tail -2
- turn 11: `execute_generated_testcase` 
- turn 12: `shell` python -c "import asgiref; print('ok', asgiref.__file__)"; w
- turn 13: `shell` python tests/runtests.py utils_tests.test_html template_test
- turn 14: `shell` python - <<'EOF'
import django
from django.conf import setti
- turn 15: `shell` python - <<'EOF'
import django
from django.conf import setti
- turn 17: `benzi_grep` 
- turn 17: `list_files` docs
- turn 19: `read_source` django/utils/html.py::json_script
- turn 20: `edit_lines` django/utils/html.py
- turn 21: `read_source` django/utils/html.py::json_script
- turn 22: `edit_lines` django/utils/html.py
- turn 23: `shell` python tests/runtests.py utils_tests.test_html template_test
- turn 25: `read_source` django/utils/html.py::json_script
- turn 25: `read_source` django/template/defaultfilters.py::json_script

## Verifier

- verdict: revise
- critique: 

## Final patch

```diff
diff --git a/django/template/defaultfilters.py b/django/template/defaultfilters.py
index 5ccef38048..469722d388 100644
--- a/django/template/defaultfilters.py
+++ b/django/template/defaultfilters.py
@@ -83,7 +83,8 @@ def escapejs_filter(value):
 
 
 @register.filter(is_safe=True)
-def json_script(value, element_id):
+@register.filter(is_safe=True)
+def json_script(value, element_id=None):
     """
     Output value JSON-encoded, wrapped in a <script type="application/json">
     tag.
diff --git a/django/utils/html.py b/django/utils/html.py
index da1b5675ec..be9f22312e 100644
--- a/django/utils/html.py
+++ b/django/utils/html.py
@@ -61,7 +61,7 @@ _json_script_escapes = {
 }
 
 
-def json_script(value, element_id):
+def json_script(value, element_id=None):
     """
     Escape all the HTML/XML special characters with their unicode escapes, so
     value is safe to be output anywhere except for inside a tag attribute. Wrap
@@ -69,10 +69,13 @@ def json_script(value, element_id):
     """
     from django.core.serializers.json import DjangoJSONEncoder
     json_str = json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
-    return format_html(
-        '<script id="{}" type="application/json">{}</script>',
-        element_id, mark_safe(json_str)
-    )
+    if element_id:
+        template = '<script id="{}" type="application/json">{}</script>'
+        args = (element_id, mark_safe(json_str))
+    else:
+        template = '<script type="application/json">{}</script>'
+        args = (mark_safe(json_str),)
+    return format_html(template, *args)
 
 
 def conditional_escape(text):

```
