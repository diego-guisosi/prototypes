import datetime
from elapsed_time_parser import make_parser
from subprocess import run, PIPE


def read_log_entries(log_file_path, log_file_entries_regex):
    grep_result = run(["grep", "-P", log_file_entries_regex, log_file_path], stdout=PIPE, universal_newlines=True)

    if grep_result.returncode != 0:
        raise RuntimeError("Exit Code = {}, Error = {}", grep_result.returncode, grep_result.stderr)

    return [entry.strip() for entry in grep_result.stdout.split("\n") if entry.strip()]


def extract_datetimes(log_entries):
    datetime_entries = []
    for entry in log_entries:
        entry_parts = entry.split()
        datetime_entries.append("{} {}".format(entry_parts[0], entry_parts[1]))
    return datetime_entries


def calculate_elapsed_times(datetime_entries, datetime_format):
    if len(datetime_entries) % 2 != 0:
        raise ValueError("Entries must be even to calculate elapsed time")

    start_datetimes = [entry for index, entry in enumerate(datetime_entries) if index % 2 == 0]
    end_datetimes = [entry for index, entry in enumerate(datetime_entries) if index % 2 != 0]

    parser = make_parser(datetime_format)
    return [parser(start_datetime, end_datetimes[index]) for index, start_datetime in enumerate(start_datetimes)]


def main(log_file_path, log_file_entries_regex, datetime_format='%Y-%m-%d %H:%M:%S'):
    entries = read_log_entries(log_file_path, log_file_entries_regex)
    datetime_entries = extract_datetimes(entries)

    elapsed_times = calculate_elapsed_times(datetime_entries, datetime_format)
    print(["{}".format(elapsed_time) for elapsed_time in elapsed_times])

    total_elapsed_time = sum(elapsed_times, datetime.timedelta())
    print(total_elapsed_time)


if __name__ == '__main__':
    log_path = "system.log"
    log_entries_regex = "INFO.*?(Querying|queried)"
    main(log_path, log_entries_regex)
