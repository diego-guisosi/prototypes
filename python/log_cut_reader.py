import datetime
from subprocess import Popen, PIPE, TimeoutExpired
from elapsed_time_parser import make_parser

PIPELINE_TIMEOUT_IN_SECONDS = 10


def main(log_file_path, log_file_entries_regex, datetime_format='%Y-%m-%d %H:%M:%S'):
    datetime_entries = read_log_entries(log_file_path, log_file_entries_regex)

    elapsed_times = calculate_elapsed_times(datetime_entries, datetime_format)
    print_formatted(elapsed_times)

    total_elapsed_time = calculate_total(elapsed_times)
    print(total_elapsed_time)


def read_log_entries(log_file_path, log_file_entries_regex):
    grep_log_entries = Popen(["grep", "-P", log_file_entries_regex, log_file_path],
                             stdout=PIPE, stderr=PIPE)
    cut_datetimes = Popen(["cut", "-d", " ", "-f", "1,2"],
                          stdin=grep_log_entries.stdout, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    stdout = try_communicate_with(cut_datetimes)
    return [entry.strip() for entry in stdout.split('\n') if entry.strip()]


def try_communicate_with(process):
    try:
        stdout, stderr = process.communicate(timeout=PIPELINE_TIMEOUT_IN_SECONDS)

        if stderr:
            raise RuntimeError("Error during pipening of commands: {}", stderr)

        return stdout
    except TimeoutExpired as e:
        process.kill()
        raise e


def calculate_elapsed_times(datetime_entries, datetime_format):
    if len(datetime_entries) % 2 != 0:
        raise ValueError("Entries must be even to calculate elapsed time")

    start_datetimes = [entry for index, entry in enumerate(datetime_entries) if index % 2 == 0]
    end_datetimes = [entry for index, entry in enumerate(datetime_entries) if index % 2 != 0]

    parse = make_parser(datetime_format)
    return [parse(*datetimes_transposition) for datetimes_transposition in zip(start_datetimes, end_datetimes)]


def print_formatted(items):
    print(["{}".format(item) for item in items])


def calculate_total(elapsed_times):
    return sum(elapsed_times, datetime.timedelta())


if __name__ == '__main__':
    main(log_file_path="system.log", log_file_entries_regex="INFO.*?(Querying|queried)")
