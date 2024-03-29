"""
$ python3 -m unittest tests/test_file.py 
"""


class TestFile(unittest.TestCase):
    path = None
    file_name = None
    testing = None

    def setUp(self):
        self.path = "/home/user/tests"
        self.testing = True

    def test_is_well_formatted_ok(self):
        self.file_name = "Subtitle 1x01.srt"

        f = File(self.path, self.file_name)

        self.assertTrue(f.is_well_formatted())

    def test_is_well_formatted_fail(self):
        self.file_name = "Subtitle101.srt"

        f = File(self.path, self.file_name)

        self.assertFalse(f.is_well_formatted())

    def test_rename_ok(self):
        self.file_name = "FileOriginalName.mp4"

        print("TestFile.test_rename_ok")
        f = File(self.path, self.file_name)
        f.new_file_name = "FileNewName.mp4"
        f._rename_file(True)

        self.assertTrue(True)

    def test_rename_fail(self):
        print("TestFile.test_rename_fail")
        self.file_name = "FileOriginalName.mp4"
        f = File(self.path, self.file_name)
        self.assertRaises(Exception, f._rename_file(True))

    def test_translate_ok(self):
        self.file_name = "Family Guy 0x00.mp4"
        expected = "Padre de familia 0x00.mp4"

        f = File(self.path, self.file_name)
        f.new_file_name = self.file_name
        f.show_name = "Family Guy"
        f._translate()
        self.assertEqual(f.new_file_name, expected)

    def test_translate_fail(self):
        self.file_name = "FileNewName.mp4"
        f = File(self.path, self.file_name)
        f.show_name = "NonExistentShowName"
        f._translate()
        self.assertIsNone(f.new_file_name)

    def test_wrap_year_1(self):
        self.file_name = "FileName (2015).mkv"

        f = File(self.path, self.file_name)
        f.new_file_name = f.file_name
        f.show_name = f.file_name
        f._wrap_year()

        self.assertEqual(self.file_name, f.new_file_name)

    def test_wrap_year_2(self):
        self.file_name = "FileName 2015.mkv"
        expected = "FileName (2015).mkv"

        f = File(self.path, self.file_name)
        f.show_name = self.file_name
        output = f._wrap_year()

        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
