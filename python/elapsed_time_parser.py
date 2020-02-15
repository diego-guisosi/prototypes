from datetime import datetime


def make_parser(datetime_format):
    def parser(start_string, end_string):
        start_datetime = datetime.strptime(start_string, datetime_format)
        end_datetime = datetime.strptime(end_string, datetime_format)
        return end_datetime - start_datetime
    return parser
