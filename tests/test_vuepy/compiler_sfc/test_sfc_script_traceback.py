"""
Test SFC script block error stack display functionality

These tests verify that when an SFC script block contains an error, the error stack can:
1. Display the correct file name (not '<ast>' or '__tmp_for_str.vue')
2. Display the accurate line number
3. Support 4 different import_sfc call formats when raw_content=True
"""
import pathlib
import unittest
import traceback
import tempfile
import os
import re
from pathlib import Path

from vuepy import import_sfc, create_app

class _TestBase:
    def _extract_error_line_from_traceback(self, tb_str, filename, func_name='setup'):
        """Extract the line number of the specified file from the error stack"""
        # Find lines containing the file name, typically in the format: File "filename", line X, in ...
        # Need to find the line number in the setup function
        pattern = rf'File\s+"{re.escape(filename)}",\s+line\s+(\d+),\s+in\s+{func_name}'
        match = re.search(pattern, tb_str)
        if match:
            return int(match.group(1))
        # If setup is not found, try to find any line containing the file
        pattern = rf'File\s+"{re.escape(filename)}",\s+line\s+(\d+)'
        match = re.search(pattern, tb_str)
        if match:
            return int(match.group(1))
        return None

    def _assert_traceback_correct(self, exception, current_file, expected_error_line, delta=0, func_name='setup'):
        """
        Verify that the error stack displays the correct file name and line number
        
        :param exception: Captured exception object
        :param current_file: Path to the current test file
        :param expected_error_line: Expected error line number
        :param delta: Allowed line number deviation (default 0, means exact match)
        """
        tb_str = ''.join(traceback.format_tb(exception.__traceback__))
        actual_line = self._extract_error_line_from_traceback(tb_str, current_file, func_name)
        
        self.assertIn(current_file, tb_str, 
                     f"Error stack should contain current file name {current_file}, actual:\n{tb_str}")
        self.assertNotIn('<ast>', tb_str, 
                        f"Error stack should not contain '<ast>', actual:\n{tb_str}")
        self.assertIsNotNone(actual_line, 
                           f"Cannot extract line number from error stack:\n{tb_str}")
        self.assertAlmostEqual(
            actual_line, expected_error_line, delta=delta,
            msg=f"Expected line number {expected_error_line}, actual line number {actual_line}.\nError stack:\n{tb_str}"
        )

    def _test_app_and_assert_traceback(self, app_component, import_line, line_offset, delta=0, func_name='setup'):
        """
        Create an application and verify that the error stack displays the correct file name and line number
        
        :param app_component: Component created by import_sfc
        :param import_line: Line number of import_sfc call
        :param line_offset: Offset of error line number relative to import_line
        :param delta: Allowed line number deviation (default 0, means exact match)
        """
        current_file = __file__
        expected_error_line = import_line + line_offset
        
        try:
            app = create_app(app_component, backend='ipywidgets')
            app.mount()
        except ZeroDivisionError as e:
            self._assert_traceback_correct(e, current_file, expected_error_line, delta=delta, func_name=func_name)


class TestSFCScriptStrTraceback(unittest.TestCase, _TestBase):
    """Test SFC script block error stack display"""
    def test_traceback_format1_same_line(self):
        """Test format 1: import_sfc(\"\"\"<template...  (same line)"""
        # Format 1: same line, triple quotes followed by content
        # Record the actual line number of import_sfc call
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc("""<template>
<div>Test</div>
</template>
<script lang="py">
from vuepy import ref

# Error here
x = 1 / 0
</script>""", raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 8)

    def test_traceback_format2_quote_newline(self):
        """Test format 2: import_sfc(\"\"\"\n<template...  (triple quotes followed by newline)"""
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc("""
<template>
  <div>Test</div>
</template>
<script lang="py">
from vuepy import ref

# Error here
x = 1 / 0
</script>
""", raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 9)

    def test_traceback_format3_paren_newline(self):
        """Test format 3: import_sfc(\n\"\"\"<template...  (parentheses followed by newline, triple quotes on the same line)"""
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc(
"""<template>
  <div>Test</div>
</template>
<script lang="py">
from vuepy import ref

# Error here
x = 1 / 0
</script>
""", raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 9)

    def test_traceback_format4_both_newline(self):
        """Test format 4: import_sfc(\n\"\"\"\n<template...  (parentheses followed by newline, triple quotes also followed by newline)"""
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc(
            """
                <template>
                <div>Test</div>
                </template>
                <script lang="py">
                from vuepy import ref

                # Error here
                x = 1 / 0
                def f():
                    pass
                </script>
            """, raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 10)

    def test_traceback_format5_from_var(self):
        import_line = __import__('inspect').currentframe().f_lineno
        sfc_content = """
            <template>
            <div>Test</div>
            </template>
            <script lang="py">
            from vuepy import ref
            x = 1 / 0  # Error from var
            def f():
                pass
            </script>
        """
        App = import_sfc(sfc_content, raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 7)

    def test_traceback_with_multiple_errors(self):
        """Test when there are multiple errors, the error stack can display correctly"""
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc("""
<template>
  <div>Test</div>
</template>
<script lang="py">
from vuepy import ref

def func1():
    x = 1 / 0  # error here

def func2():
    y = 2 / 0

# Call function to trigger error
func1()
</script>
""", raw_content=True)
        
        self._test_app_and_assert_traceback(App, import_line, 9, func_name='func1')
        # App = import_sfc(sfc_content, raw_content=True)
        # current_file = __file__
        
        # try:
        #     app = create_app(App, backend='ipywidgets')
        #     app.mount()
        # except ZeroDivisionError as e:
        #     tb_str = ''.join(traceback.format_tb(e.__traceback__))
        #     # Check if the error stack contains the current file name
        #     self.assertIn(current_file, tb_str, 
        #                  f"Error stack should contain current file name {current_file}")
        #     self.assertNotIn('<ast>', tb_str, 
        #                     f"Error stack should not contain '<ast>'")

    def test_traceback_with_nested_function_calls(self):
        """Test when there are nested function calls, the error stack is correct"""
        import_line = __import__('inspect').currentframe().f_lineno
        App = import_sfc("""
<template>
  <div>Test</div>
</template>
<script lang="py">
from vuepy import ref

def outer():
    def inner():
        x = 1 / 0  # Error here
    inner()

outer()
</script>
""", raw_content=True)
        self._test_app_and_assert_traceback(App, import_line, 10, func_name='inner')


class TestVueFileTraceback(unittest.TestCase, _TestBase):
    def test_format1(self):
        """Test when loading from a file, the error stack displays the correct file name and line number"""
        sfc_content = """
<template>
  <div>Test</div>
</template>
<script lang="py">
from vuepy import ref
# This line of code will trigger an error
x = 1 / 0  # This is the 8th line of the file
</script>
"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vue', delete=False) as f:
            f.write(sfc_content)
            temp_file = f.name
        
        try:

            App = import_sfc(temp_file, raw_content=False)
            
            try:
                app = create_app(App, backend='ipywidgets')
                app.mount()
            except ZeroDivisionError as e:
                self._assert_traceback_correct(e, temp_file, 8)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_format2(self):
        sfc_content = """
<template>
  <div>Test</div>
</template>
<script lang="py">
def func1():
    x = 1 / 0  # error here

def func2():
    y = 2 / 0

func1()
</script>
"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vue', delete=False) as f:
            f.write(sfc_content)
            temp_file = f.name
        
        try:

            App = import_sfc(temp_file)
            
            try:
                app = create_app(App, backend='ipywidgets')
                app.mount()
            except ZeroDivisionError as e:
                self._assert_traceback_correct(e, temp_file, 7, func_name='func1')
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_format3(self):
        sfc_content = """
<template>
  <div>Test</div>
</template>
<script lang="py">
def func1():
    app.tt_app # error here 

def func2():
    y = 2 / 0

func1()
</script>
"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vue', delete=False) as f:
            f.write(sfc_content)
            temp_file = f.name
        
        try:

            App = import_sfc(temp_file)
            
            try:
                app = create_app(App, backend='ipywidgets')
                app.mount()
            except AttributeError as e:
                self._assert_traceback_correct(e, temp_file, 7, func_name='func1')
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file):
                os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
