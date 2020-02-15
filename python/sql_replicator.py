#!/usr/bin/env python3

import sys


FILE_NAME = "insert_limit.sql"
PROFILE_SEQ = "::PRFE_ID_SEQ::"
LIMIT_SEQ = "::LMTE_ID_SEQ::"


def main(num_profiles, num_limits):
    template_lines = load_template()

    seq_limit = 1
    with open(FILE_NAME, 'wt') as target:
        for seq_limit in range(0, num_limits):
            for seq_profile in range(0, num_profiles):
                for template_line in template_lines:
                    replaced_line = template_line\
                        .replace(PROFILE_SEQ, "{}".format(seq_profile + 1))\
                        .replace(LIMIT_SEQ, "{}".format(seq_limit + 1))
                    target.write(replaced_line)
                    if (num_profiles + 1) % 100 == 0:
                        write_commit(target)
        write_commit(target)


def load_template():
    with open('template_{}'.format(FILE_NAME), 'rt') as source:
        return source.readlines()


def write_commit(target):
    target.write("COMMIT;\n")


if __name__ == '__main__':
    main(int(sys.argv[1]),  # Number of profiles
         int(sys.argv[2]))  # Number of limits per profile
