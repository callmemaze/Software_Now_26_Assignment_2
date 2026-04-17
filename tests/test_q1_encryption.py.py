import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import encryption_program 


class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.raw_file = "raw_text.txt"
        self.enc_file = "encrypted_text.txt"
        self.dec_file = "decrypted_text.txt"

    def write_raw(self, text):
        with open(self.raw_file, "w", encoding="utf-8") as f:
            f.write(text)

    # ---------------- BASIC TEST ----------------
    def test_basic_text(self):
        text = "Hello World"

        self.write_raw(text)
        encryption_program.main()

        with open(self.dec_file, "r", encoding="utf-8") as f:
            result = f.read()

        self.assertEqual(result, text)

    # ---------------- SYMBOLS ----------------
    def test_symbols(self):
        text = "ABC 123 !@# xyz"

        self.write_raw(text)
        encryption_program.main()

        with open(self.dec_file, "r", encoding="utf-8") as f:
            result = f.read()

        self.assertEqual(result, text)

    # ---------------- EMOJIS ----------------
    def test_emojis(self):
        text = "Hello 😄 Rocket 🚀"

        self.write_raw(text)
        encryption_program.main()

        with open(self.dec_file, "r", encoding="utf-8") as f:
            result = f.read()

        self.assertEqual(result, text)

    # ---------------- EMPTY FILE ----------------
    def test_empty(self):
        self.write_raw("")
        encryption_program.main()

        with open(self.dec_file, "r", encoding="utf-8") as f:
            result = f.read()

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()