"""Test Class for ContentHandler Class."""
from .context import mathcontentconverter

from mathcontentconverter import ContentHandler
import mock


class FakeRequest(object):

    def text(self):
        return "<span class='katex'>faked-content</span>"


def return_fake_request_object(url, **kwargs):
    return FakeRequest()


class TestContentHandler:
    """Test Class for TestContentHandler."""

    def test_line_breaking_single_item(self):
        """Test line breaks."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        obj1 = {"text": "Foo", "inline": False}
        args = [obj1]
        result = ch.break_into_lines(args)
        expected_result = [[obj1]]
        assert(result == expected_result)

    def test_line_breaking_inline_false(self):
        """Test line breaks."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        obj1 = {"text": "Foo", "inline": False}
        obj2 = {"text": "Bar", "inline": False}
        args = [obj1, obj2]
        result = ch.break_into_lines(args)
        expected_result = [[obj1], [obj2]]
        assert(result == expected_result)

    def test_line_breaking_multiple_inline(self):
        """Test line breaks."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        obj1 = {"text": "Foo", "inline": False}
        obj2 = {"text": "Bar", "inline": True}
        obj3 = {"text": "Baz", "inline": False}
        obj4 = {"text": "Bo", "inline": True}
        args = [obj1, obj2, obj3, obj4]
        result = ch.break_into_lines(args)
        expected_result = [[obj1, obj2], [obj3, obj4]]
        assert(result == expected_result)

    def test_line_breaking_multiple_inline_2(self):
        """Test line breaks."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        obj1 = {"text": "Foo", "inline": False}
        obj2 = {"text": "Bar", "inline": True}
        obj3 = {"text": "Baz", "inline": True}
        obj4 = {"text": "Bo", "inline": False}
        args = [obj1, obj2, obj3, obj4]
        result = ch.break_into_lines(args)
        expected_result = [[obj1, obj2, obj3], [obj4]]
        assert(result == expected_result)

    def test_formatted_content_inline_false(self):
        """Test that content is formatted."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        args = [
            {"text": "Foo", "inline": False},
            {"text": "Bar", "inline": False},
        ]
        result = ch.get_formatted_content(args)
        expected_result = "<p>Foo</p><p>Bar</p>"
        assert(result == expected_result)

    def test_formatted_content_inline_true(self):
        """Test that content is formatted."""
        ch = ContentHandler(
            src_image_file_path="/fake",
            dest_image_file_path="/fake",
            reference_url="/fake",
            image_conversion_url="/fake")

        args = [
            {"text": "Foo", "inline": False},
            {"text": "Bar", "inline": True},
        ]
        result = ch.get_formatted_content(args)
        expected_result = "<p>FooBar</p>"
        assert(result == expected_result)

    def test_formatted_content_image(self):
        """Test that content is formatted."""
        ch = ContentHandler()
        args = [
            {"text": "Foo", "inline": False},
            {"image": "Bar.jpg", "inline": False},
        ]
        result = ch.get_formatted_content(args)
        expected_result = "<p>Foo</p><p><img src='Bar.jpg' /></p>"
        assert(result == expected_result)

    @mock.patch('requests.post', return_fake_request_object)
    def test_get_katex(self):
        """Check that katex is returned."""
        ch = ContentHandler()
        result = ch.create_katex("\frac{1}{2}")
        assert(isinstance(result, type("a")))
        assert(result == "<span class='katex'>faked-content</span>")
