import unittest

from ipywui import wui
from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.compiler_sfc.template_compiler import DomCompiler
from vuepy.runtime.core.api_create_app import App


class TestCompileTraceback(unittest.TestCase):

    def setUp(self):
        self.app = App({}).use(wui)
        self.vm = VueComponent({'l': [1, 2, 3]}, app=self.app)
        self.compiler = DomCompiler(self.vm, self.app)

    def test_v_for_start_error(self):
        html_content = """
        <VBox>
          <HBox><p>hello</p></HBox>
          <HBox>
            <Label v-for="index, item in var_not_exist">xx</Label>
          </HBox>
        </VBox>
        """
        expected_error_message = '''\
<VBox>
  <HBox>...</HBox>
  <HBox>
    <Label> start <----- compile failed, name 'var_no_exist' is not defined
'''
        with self.assertRaises(Exception) as context:
            self.compiler.compile(html_content)
        traceback_output = self.compiler._compile_traceback_info
        self.assertEqual(expected_error_message, traceback_output)

    def test_custom_tag_v_for_in_process_error(self):
        html_content = """
        <VBox>
          <HBox><p>hello</p></HBox>
          <HBox>
            <Label v-for="index, item in l">xx</Label>
            <VBox>
              <Box v-for="index, item in l">
                <p>xx</p>
                <Button v-for="index, item in l">{{ 1 / (index - 2) }}</Button>
              </Box>
            </VBox>
          </HBox>
        </VBox>
        """
        expected_error_message = '''\
<VBox>
  <HBox>...</HBox>
  <HBox>
    <Label v-for: (0,)>...</Label>
    <Label v-for: (1,)>...</Label>
    <Label v-for: (2,)>...</Label>
    <VBox>
      <Box v-for>
        <Button v-for>
        </Button> inner <----- compile failed, division by zero
'''
        with self.assertRaises(Exception) as context:
            self.compiler.compile(html_content)
        traceback_output = self.compiler._compile_traceback_info
        self.assertEqual(expected_error_message, traceback_output)

    def test_html_tag_v_for_in_process_error(self):
        html_content = """
        <VBox>
          <HBox>
            <p v-for="index, item in l">{{ 1 / (index - 1) }}</p>
          </HBox>
        </VBox>
        """
        expected_error_message = '''\
<VBox>
  <HBox>
    <p v-for: (0,)>...</p>
    </p> end <----- compile failed, division by zero
'''
        with self.assertRaises(Exception) as context:
            self.compiler.compile(html_content)
        traceback_output = self.compiler._compile_traceback_info
        self.assertEqual(expected_error_message, traceback_output)

    def test_no_root(self):
        html_content = """
        <HBox><p>hello</p></HBox>
        <div>world</div>
        <HBox>
          <Label v-for="index, item in l">xx</Label>
          <VBox>
            <Box v-for="index, item in l">
              <p>xx</p>
              <Button v-for="index, item in l">{{ 1 / (index - 2) }}</Button>
            </Box>
          </VBox>
        </HBox>
        """
        expected_error_message = '''\
<HBox>...</HBox>
<div>...</div>
<HBox>
  <Label v-for: (0,)>...</Label>
  <Label v-for: (1,)>...</Label>
  <Label v-for: (2,)>...</Label>
  <VBox>
    <Box v-for>
      <Button v-for>
      </Button> inner <----- compile failed, division by zero
'''
        with self.assertRaises(Exception) as context:
            self.compiler.compile(html_content)
        traceback_output = self.compiler._compile_traceback_info
        self.assertEqual(expected_error_message, traceback_output)
