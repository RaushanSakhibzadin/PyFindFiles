import os
import unittest
from unittest.mock import patch, ANY

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
    @patch('os.path.join')
    @patch('os.walk')
    def test_find_files(self, mock_walk, mock_join):
        # Set up the mock values using system-specific path separators
        mock_join.side_effect = lambda *args: os.sep.join(args)
        mock_walk.return_value = [
            (os.sep.join(['root', '']), ('dir',), ('file1.txt', 'file2.txt')),
            (os.sep.join(['root', 'dir', '']), (), ('file3.txt',))
        ]
        with patch('find_files.file_size_over_than') as mock_size_over_than:
            mock_size_over_than.side_effect = lambda filepath, size: size == '5M'
            result = find_files('/root', '5M')
            self.assertEqual(len(result), 3)  # Assuming all files match the criteria

            # Test with invalid size input
            mock_size_over_than.side_effect = lambda filepath, size: False
            result_invalid = find_files('/root', '1')
            self.assertEqual(len(result_invalid), 0)  # No files should match with invalid criteria

            # Verify that file_size_over_than was called correctly
            mock_size_over_than.assert_called_with(ANY, '1')


if __name__ == '__main__':
    unittest.main()
