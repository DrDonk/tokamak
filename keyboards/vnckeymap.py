#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: © 2022 David Parsons
# SPDX-License-Identifier: MIT
import base64
from collections import OrderedDict
import dictdiffer
import hashlib
import os.path
import sys
import vmx


if sys.version_info < (3, 10):
    sys.stderr.write('You need Python 3.10 or later\n')
    sys.exit(1)


def hex_to_string(hexstr):
    if hexstr[:2] == '0x':
        hexstr = hexstr[2:]
    string_value = bytes.fromhex(hexstr).decode('utf-8')
    return string_value


def printdiff(dict1, dict2):
    diffs = dictdiffer.diff(dict1, dict2, expand=True)
    for diff in list(diffs):
        print(diff)


def main():
    vncmap_1 = vmx.VMX('/Users/dave/work/vmware/vnckeymap/us')
    vncmap_2 = vmx.VMX('/Users/dave/work/vmware/vnckeymap/uk')
    test_1 = dict()
    for key, value in vncmap_1.items():
        test_1[vncmap_1.inline_comments[key]] = [key, value]
    test_2 = dict()
    for key, value in vncmap_2.items():
        test_2[vncmap_2.inline_comments[key]] = [key, value]

    printdiff(test_1, test_2)

    # for key, value in vncmap.items():
    #     print(f'{value} {hex_to_string(key)}')
    return


if __name__ == '__main__':
    main()
    pass
