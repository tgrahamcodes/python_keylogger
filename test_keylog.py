import unittest
from unittest.mock import patch, mock_open
from pynput.keyboard import Key, Listener
from keylogger import on_press, on_release, write_to_file, clear_file

class TestKeylogger(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_file):
        write_to_file("Test Key")
        mock_file.assert_called_once_with("log.txt", "a")
        mock_file().write.assert_called_once_with("Test Key")
    
    @patch("builtins.open", new_callable=mock_open)
    def test_clear_file(self, mock_file):
        clear_file()
        mock_file.assert_called_once_with("log.txt", "w")
        mock_file().write.assert_called_once_with("Keylogger started...\n\n")

    def test_on_press(self):
        with patch("keylogger.write_to_file") as mock_write:
            on_press("a")
            mock_write.assert_called_once_with('a')

    def test_on_release_escape_key(self):
        # Test the release of the escape key, expect False
        self.assertFalse(on_release(Key.esc))

    def test_on_release_other_key(self):
        # Test the release of any key other than escape, expect None
        self.assertIsNone(on_release(Key.space))

if __name__ == "__main__":
    unittest.main()
