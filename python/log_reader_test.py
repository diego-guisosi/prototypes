import unittest
import log_reader


class LogReaderCalculateElapsedTimesTest(unittest.TestCase):

    def test_calculate_elapsed_times(self):
        datetime_entries = [
            "2019-03-09 15:25:55",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:59",
            "2019-03-09 15:26:00",
            "2019-03-09 15:26:10"
        ]
        datetime_format = '%Y-%m-%d %H:%M:%S'

        elapsed_times = log_reader.calculate_elapsed_times(datetime_entries, datetime_format)

        self.assertEqual(3, len(elapsed_times))
        self.assertEqual(3, elapsed_times[0].seconds)
        self.assertEqual(1, elapsed_times[1].seconds)
        self.assertEqual(10, elapsed_times[2].seconds)

    def test_calculate_elapsed_times_odd(self):
        datetime_entries = [
            "2019-03-09 15:25:55",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:59",
            "2019-03-09 15:26:10"
        ]
        datetime_format = '%Y-%m-%d %H:%M:%S'

        with self.assertRaises(ValueError, msg="Entries must be even to calculate elapsed time"):
            log_reader.calculate_elapsed_times(datetime_entries, datetime_format)


class LogReaderExtractDatetimesTest(unittest.TestCase):

    def test_extract_datetimes(self):
        log_entries = [
            "2019-03-09 15:25:55 INFO Querying database...",
            "2019-03-09 15:25:58 INFO Database queried successfully",
            "2019-03-09 15:25:58 INFO Querying database...",
            "2019-03-09 15:25:59 INFO Database queried successfully",
            "2019-03-09 15:26:00 INFO Querying database...",
            "2019-03-09 15:26:10 INFO Database queried successfully"
        ]
        expected_datetime_entries = [
            "2019-03-09 15:25:55",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:58",
            "2019-03-09 15:25:59",
            "2019-03-09 15:26:00",
            "2019-03-09 15:26:10"
        ]

        datetime_entries = log_reader.extract_datetimes(log_entries)

        self.assertEqual(expected_datetime_entries, datetime_entries)


class LogReaderReadLogEntriesTest(unittest.TestCase):

    def test_read_log_entries(self):
        log_path = "system.log"
        log_entries_regex = "INFO.*?(Querying|queried)"

        expected_log_entries = [
            "2019-03-09 15:25:55 INFO Querying database...",
            "2019-03-09 15:25:58 INFO Database queried successfully",
            "2019-03-09 15:25:58 INFO Querying database...",
            "2019-03-09 15:25:59 INFO Database queried successfully",
            "2019-03-09 15:26:00 INFO Querying database...",
            "2019-03-09 15:26:10 INFO Database queried successfully"
        ]

        log_entries = log_reader.read_log_entries(log_path, log_entries_regex)

        self.assertEqual(expected_log_entries, log_entries)


if __name__ == '__main__':
    unittest.main()
