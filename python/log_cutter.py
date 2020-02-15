def main(log_file_path, delimiter, selected_fields):
    log_entries = read_log(log_file_path)
    unpacked_fields = unpack_selected_fields(selected_fields)
    entry_format = extract_entry_format(delimiter, unpacked_fields)

    for entry in log_entries:
        entry_fields = entry.split(delimiter)
        print(cut(entry_fields, unpacked_fields, entry_format))


def read_log(log_file_path):
    with open(log_file_path, mode='rt', encoding='utf-8') as log_file:
        return [entry.replace("\n") for entry in log_file]


def unpack_selected_fields(selected_fields):

    if not selected_fields:
        raise ValueError("Selected fields must be provided. E.g.: \"1, 2, -1\"")

    converted_fields = [int(field) for field in selected_fields.split(',') if field.strip()]
    return [field - 1 if field > 0 else field for field in converted_fields]


def extract_entry_format(delimiter, unpacked_fields):

    if not delimiter:
        raise ValueError("Delimiter must be provided. E.g.: \",\"")

    if not unpacked_fields:
        raise ValueError("At least one field must be provided. E.g.: \"1, 2, -1\"")

    return delimiter.join('{}' for _ in unpacked_fields)


def cut(entry_fields, unpacked_fields, entry_format):
    entry_formats = entry_format.split()

    validate_sizes(entry_fields, entry_formats, unpacked_fields)

    filtered_parts = [entry_fields[field] for field in unpacked_fields]
    return entry_format.format(*filtered_parts)


def validate_sizes(entry_fields, entry_formats, unpacked_fields):
    entry_fields_size = len(entry_fields)
    unpacked_fields_size = len(unpacked_fields)
    entry_formats_size = len(entry_formats)
    if unpacked_fields_size != entry_formats_size or entry_fields_size < unpacked_fields_size:
        raise ValueError("Number of fields mismatch. entry fields = {}, selected fields = {}".format(
            entry_fields_size, unpacked_fields_size
        ))


if __name__ == '__main__':
    main(log_file_path="system.log", delimiter=" ", selected_fields="1,2, -1,-2, 3")
