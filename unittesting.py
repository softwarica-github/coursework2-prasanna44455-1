import unittest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch

import virus_scanner

class TestVirusScanner(unittest.TestCase):

    @patch('virus_scanner.filedialog.askopenfilename', return_value='/path/to/file.exe')
    def test_scan_file(self, mock_askopenfilename):
        # Create the main window
        window = tk.Tk()
        window.title("Antivirus Scanner")
        window.geometry("500x300")

        # Create label to display the scan result
        result_label = tk.Label(window, text="", font=("Arial", 18))

        # Mock the loading_screen() function
        with patch('virus_scanner.loading_screen') as mock_loading_screen:
            # Call the scan_file() function
            virus_scanner.scan_file()

            # Assert that loading_screen() was called
            mock_loading_screen.assert_called_once()

            # Mock the process_file() function
            with patch('virus_scanner.process_file') as mock_process_file:
                # Simulate the after() callback
                window.after(3000, lambda: mock_process_file('/path/to/file.exe'))

                # Assert that process_file() was called with the correct file path
                mock_process_file.assert_called_once_with('/path/to/file.exe')

        # Cleanup
        window.destroy()

    def test_process_file_safe(self):
        # Create the main window
        window = tk.Tk()
        window.title("Antivirus Scanner")
        window.geometry("500x300")

        # Create label to display the scan result
        result_label = tk.Label(window, text="", font=("Arial", 18))

        # Mock the open() function
        with patch('builtins.open', create=True) as mock_open:
            # Mock the read() method of the file object
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = b'file contents'

            # Call the process_file() function
            virus_scanner.process_file('/path/to/file.exe')

            # Assert that the result_label text is "File is safe."
            self.assertEqual(result_label['text'], "File is safe.")
            # Assert that the result_label text color is green
            self.assertEqual(result_label['fg'], "green")

        # Cleanup
        window.destroy()

    def test_process_file_malicious(self):
        # Create the main window
        window = tk.Tk()
        window.title("Antivirus Scanner")
        window.geometry("500x300")

        # Create label to display the scan result
        result_label = tk.Label(window, text="", font=("Arial", 18))

        # Mock the open() function
        with patch('builtins.open', create=True) as mock_open:
            # Mock the read() method of the file object
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = b'file contents'

            # Call the process_file() function
            virus_scanner.process_file('/path/to/malicious.exe')

            # Assert that the result_label text is "File is malicious!"
            self.assertEqual(result_label['text'], "File is malicious!")
            # Assert that the result_label text color is red
            self.assertEqual(result_label['fg'], "red")

        # Cleanup
        window.destroy()

    @patch('virus_scanner.messagebox.askquestion', return_value='no')
    def test_ask_scan_again_no(self, mock_askquestion):
        # Create the main window
        window = tk.Tk()
        window.title("Antivirus Scanner")
        window.geometry("500x300")

        # Create label to display the scan result
        result_label = tk.Label(window, text="", font=("Arial", 18))
        result_label.config(text="File is safe.", fg="green")

        # Call the ask_scan_again() function
        virus_scanner.ask_scan_again()

        # Assert that the result_label text is "Thank you!"
        self.assertEqual(result_label['text'], "Thank you!")
        # Assert that the result_label text color is blue
        self.assertEqual(result_label['fg'], "blue")

        # Assert that the scan_button state is set to DISABLED
        self.assertEqual(virus_scanner.scan_button['state'], tk.DISABLED)

        # Cleanup
        window.destroy()

    @patch('virus_scanner.messagebox.askquestion', return_value='yes')
    def test_ask_scan_again_yes(self, mock_askquestion):
        # Create the main window
        window = tk.Tk()
        window.title("Antivirus Scanner")
        window.geometry("500x300")

        # Create label to display the scan result
        result_label = tk.Label(window, text="", font=("Arial", 18))
        result_label.config(text="File is malicious!", fg="red")

        # Call the ask_scan_again() function
        virus_scanner.ask_scan_again()

        # Assert that the result_label text is an empty string
        self.assertEqual(result_label['text'], "")

        # Cleanup
        window.destroy()

if __name__ == '__main__':
    unittest.main()
