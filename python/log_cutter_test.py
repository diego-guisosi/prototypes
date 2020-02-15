import unittest
import log_cutter


class LogCutterUnpackSelectedFieldsFormat(unittest.TestCase):

    def test_none(self):
        selected_fields = None

        with self.assertRaises(ValueError):
            log_cutter.unpack_selected_fields(selected_fields)

    def test_empty(self):
        selected_fields = ""

        with self.assertRaises(ValueError):
            log_cutter.unpack_selected_fields(selected_fields)

    def test_zero(self):
        selected_fields = "0"
        expected_unpacked_fields = [0]

        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_positive(self):
        selected_fields = "1"
        expected_unpacked_fields = [0]

        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_positives(self):
        selected_fields = "1,2"
        expected_unpacked_fields = [0, 1]

        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_negative(self):
        selected_fields = "-2"
        expected_unpacked_fields = [-2]

        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_negatives(self):
        selected_fields = "-1,-2"
        expected_unpacked_fields = [-1, -2]

        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_mixed(self):
        selected_fields = "1,2,-1"

        expected_unpacked_fields = [0, 1, -1]
        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_spaces(self):
        selected_fields = " 1, 2, -1 "

        expected_unpacked_fields = [0, 1, -1]
        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_missing(self):
        selected_fields = " 1, , -1 "

        expected_unpacked_fields = [0, -1]
        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_repeated(self):
        selected_fields = " 2, 2, 2 "

        expected_unpacked_fields = [1, 1, 1]
        unpacked_fields = log_cutter.unpack_selected_fields(selected_fields)

        self.assertEqual(expected_unpacked_fields, unpacked_fields)

    def test_non_numeric(self):
        selected_fields = "a, b, c"

        with self.assertRaises(ValueError):
            log_cutter.unpack_selected_fields(selected_fields)

    def test_wrong_delimiter(self):
        selected_fields = "1; 2; 3"

        with self.assertRaises(ValueError):
            log_cutter.unpack_selected_fields(selected_fields)


class LogCutterExtractEntryFormat(unittest.TestCase):

    def test_empty_delimiter(self):
        delimiter = ""
        unpacked_fields = [1]

        with self.assertRaises(ValueError):
            log_cutter.extract_entry_format(delimiter, unpacked_fields)

    def test_empty_unpacked_fields(self):
        delimiter = " "
        unpacked_fields = []

        with self.assertRaises(ValueError):
            log_cutter.extract_entry_format(delimiter, unpacked_fields)

    def test_single(self):
        delimiter = " "
        unpacked_fields = [1]
        expected_entry_format = "{}"

        entry_format = log_cutter.extract_entry_format(delimiter, unpacked_fields)

        self.assertEqual(expected_entry_format, entry_format)

    def test_multiple(self):
        delimiter = ";"
        unpacked_fields = [1, 2, -1]
        expected_entry_format = "{};{};{}"

        entry_format = log_cutter.extract_entry_format(delimiter, unpacked_fields)

        self.assertEqual(expected_entry_format, entry_format)


class LogCutterCutEntryTest(unittest.TestCase):

    def test_match(self):
        log_entry = ["2019-03-09", "15:26:10", "INFO", "Database", "queried", "successfully"]
        unpacked_fields = [0, 1, -1]
        entry_format = "{} {} {}"

        expected_cutted_entry = "2019-03-09 15:26:10 successfully"
        cutted_entry = log_cutter.cut(log_entry, unpacked_fields, entry_format)

        self.assertEqual(expected_cutted_entry, cutted_entry)

    def test_mismatch_log_entry(self):
        log_entry = ["15:26:10", "INFO"]
        unpacked_fields = [1, 2, -1]
        entry_format = "{} {} {}"

        with self.assertRaises(ValueError, msg="Number of fields mismatch. entry fields = 2, selected fields = 3"):
            log_cutter.cut(log_entry, unpacked_fields, entry_format)

    def test_mismatch_unpacked_fields(self):
        log_entry = ["2019-03-09", "15:26:10", "INFO", "Database", "queried", "successfully"]
        unpacked_fields = [1, -1]
        entry_format = "{} {} {}"

        with self.assertRaises(ValueError, msg="Number of fields mismatch. entry fields = 2, selected fields = 3"):
            log_cutter.cut(log_entry, unpacked_fields, entry_format)

    def test_mismatch_entry_format(self):
        log_entry = ["2019-03-09", "15:26:10", "INFO", "Database", "queried", "successfully"]
        unpacked_fields = [1, 2, -1]
        entry_format = "{} {}"

        with self.assertRaises(ValueError, msg="Number of fields mismatch. entry fields = 2, selected fields = 3"):
            log_cutter.cut(log_entry, unpacked_fields, entry_format)


if __name__ == '__main__':
    unittest.main()
