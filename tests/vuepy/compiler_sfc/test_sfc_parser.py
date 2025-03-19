import unittest

from vuepy.compiler_sfc.sfc_parser import SFCParser
from vuepy.compiler_sfc.sfc_parser import SFCTag


class TestFirstLevelTagValidator(unittest.TestCase):
    def test_single_tag_should_return_correct_sfctag_when_html_is_simple(self):
        html = "<div>Hello World</div>"
        validator = SFCParser()
        sfc_tags = validator.parse(html)

        expected_tag = SFCTag(
            name="div",
            attrs={},
            start_pos=(1, 0),
            end_pos=(1, 16),
            inner_html="Hello World"
        ).to_dict()

        self.assertEqual(expected_tag, sfc_tags[0].to_dict())

    def test_nested_tags_should_return_only_first_level_tag_when_html_has_nested_tags(self):
        html = "<div><p>Hello</p><p>World</p></div>"
        validator = SFCParser()
        sfc_tags = validator.parse(html)

        expected_tag = SFCTag(
            name="div",
            attrs={},
            start_pos=(1, 0),
            end_pos=(1, 29),
            inner_html="<p>Hello</p><p>World</p>"
        ).to_dict()

        self.assertEqual(expected_tag, sfc_tags[0].to_dict())

    def test_multiple_first_level_tags_should_return_all_tags_when_html_has_multiple_first_level_tags(self):
        # html = "<Div a='>'>Hello</div><p>World</p>"
        html = "<Div>Hello</div><p>World</p>"
        validator = SFCParser()
        sfc_tags = validator.parse(html)

        expected_tags = [
            SFCTag(
                name="div",
                attrs={},
                start_pos=(1, 0),
                end_pos=(1, 10),
                inner_html="Hello"
            ).to_dict(),
            SFCTag(
                name="p",
                attrs={},
                start_pos=(1, 16),
                end_pos=(1, 24),
                inner_html="World"
            ).to_dict(),
        ]

        self.assertEqual(expected_tags, [tag.to_dict() for tag in sfc_tags])

    def test_tag_with_attributes_should_return_correct_attrs_when_html_tag_has_attributes(self):
        html = '<div class="container" id="main">Content</div>'
        validator = SFCParser()
        sfc_tags = validator.parse(html)

        expected_tag = SFCTag(
            name="div",
            attrs={"class": "container", "id": "main"},
            start_pos=(1, 0),
            end_pos=(1, 40),
            inner_html="Content"
        ).to_dict()

        self.assertEqual(expected_tag, sfc_tags[0].to_dict())

    def test_invalid_html_should_raise_error_when_level1_tags_mismatch(self):
        htmls = [
            "<div><p>Hello</div></p>",
            "<template>xx</templates><div>yyy</div>",
            "<temp>xx</temp><a></a><script>aaa</scripts>"
        ]
        for html in htmls:
            validator = SFCParser()
            with self.assertRaises(ValueError) as context:
                print(validator.parse(html))

        # self.assertTrue("First level tag mismatch" in str(context.exception))

    def test_multiline_html_should_return_correct_positions_when_html_is_multiline(self):
        html = '<div>\n'\
               '  <p>Hello</p>\n'\
               '  <p>World</p>\n'\
               '</div>'
        validator = SFCParser()
        sfc_tags = validator.parse(html)

        expected_tag = SFCTag(
            name="div",
            attrs={},
            start_pos=(1, 0),
            end_pos=(4, 0),
            inner_html="\n  <p>Hello</p>\n  <p>World</p>\n"
        ).to_dict()

        self.assertEqual(expected_tag, sfc_tags[0].to_dict())
