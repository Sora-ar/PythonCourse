from unittest.mock import patch

from quize57 import FileTextManipulator


@patch.object(FileTextManipulator, 'read_text_from_file')
@patch.object(FileTextManipulator, 'modify_text', return_value='😊')
def test_get_text(mock_modify_text, mock_read_text):
    obj = FileTextManipulator(None)
    actual = obj.get_text()
    expected = 'TEXT -- 😊'

    assert actual == expected
