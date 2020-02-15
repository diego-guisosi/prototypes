import unittest
from elapsed_time_parser import make_parser


def format_timedelta(timedelta):
    return "days={delta.days} seconds={delta.seconds} microseconds={delta.microseconds}".format(delta=timedelta)


class ElapsedTimeParserTest(unittest.TestCase):

    def setUp(self):
        self.format_pattern = '%Y-%m-%d %H:%M:%S'
        self.parser = make_parser(self.format_pattern)

    def test_parse(self):
        start = '2019-03-09 14:55:30'
        end = '2019-03-09 14:55:35'
        expected_elapsed_time_in_seconds = 5

        elapsed_time = self.parser(start, end)

        self.assertEqual(expected_elapsed_time_in_seconds,
                         elapsed_time.seconds,
                         "Elapsed time between {} and {} should be 5 seconds. Actual timedelta=({})".format(
                             start, end, format_timedelta(elapsed_time)))

    def test_parse_invalid_order(self):
        start = '2019-03-09 14:55:35'
        end = '2019-03-09 14:55:30'
        expected_elapsed_time_in_days = -1

        elapsed_time = self.parser(start, end)
        self.assertEqual(expected_elapsed_time_in_days,
                         elapsed_time.days,
                         "Elapsed time between {} and {} should have negative days. Actual timedelta=({})".format(
                             start, end, format_timedelta(elapsed_time)))


if __name__ == '__main__':
    unittest.main()
