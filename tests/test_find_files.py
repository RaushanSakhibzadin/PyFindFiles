import unittest
from unittest.mock import patch

from find_files import find_files, file_size_over_than


class TestFileSizeOverThan(unittest.TestCase):
    def test_file_size_over_than_valid(self):
        with patch('os.path.getsize', return_value=1500):
            self.assertTrue(file_size_over_than("fake_path", "1k"))

    def test_file_size_over_than_invalid_unit(self):
        with patch('os.path.getsize', return_value=1500):
            with self.assertRaises(ValueError):
                file_size_over_than(".", "1z")

    def test_file_size_over_than_error_accessing_file(self):
        with patch('os.path.getsize', side_effect=OSError("Error accessing file")):
            self.assertFalse(file_size_over_than("fake_path", "1k"))


class TestFindFiles(unittest.TestCase):
    @patch('os.walk')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_find_files(self, mock_join, mock_walk):
        mock_walk.return_value = [
            ('/root', ('dir',), ('file1.txt', 'file2.txt')),
            ('/root/dir', (), ('file3.txt',))
        ]
        mock_join.side_effect = lambda *args: '/'.join(args)
        with patch('find_files.file_size_over_than', return_value=True):
            result = find_files('/root', '1k')
            self.assertEqual(len(result), 3)  # Assuming all files match the criteria


if __name__ == '__main__':
    unittest.main()
