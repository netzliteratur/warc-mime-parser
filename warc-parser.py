#!/usr/bin/env python2
"""
warc-parser parses warc files.
It can list MIME-Types and extract
files from the web archives bitstream.
"""
__version__ = '0.2'
__status__ = 'Developing'
__date__ = '20140331'
__author__ = 'steffen fritz'
__contact__ = 'fritz@dla-marbach.de'
__copyright__ = 'Copyright (c) 2014 Deutsches Literaturarchiv Marbach'
__license__ = 'The MIT License'
__maintainer__ = 'steffen fritz'


import sys
from collections import defaultdict


def usage_message():
    """
    print a usage message
    """
    print("\nUsage: ./warc-parser.py [-m|-e] WARC_FILE.warc")
    print(" -m  :  list MIME Types")
    print(" -e  :  extract files from bitstream (not implemented yet)\n")


def read_file(file_name):
    """
    read warc-file, cast create 
    an iter-Object and return 
    that object
    """
    fd = open(file_name, "r")
    warc_file = fd.readlines()
    fd.close()
    warc_file = iter(warc_file)

    return warc_file


def list_mime_types(warc_file):
    """
    parse the warc file for Content-Type:.+
    return the defaultdict mime_types
    """
    mime_types = defaultdict(int)
    
    for line in warc_file:
        if line.rstrip().startswith("Content-Type"):
            line_temp = line.split(":")[1]
            mime_types[line_temp.rstrip()] += 1

    return mime_types


def extract_mime_types(warc_file):
    """
    parse the warc file for Content-Type.+
    parse the warc file for Target-URI.*
    write contents to files
    """
    for line in warc_file:
        if line.rstrip().startswith("WARC-Target-URI"):
            if line.split(":")[1]:
                file_name_temp = line.split(":")[2]
                print(line)
                fd = open(file_name_temp, "w")
                fd.write("")
                fd.close()


def pretty_printing(title, in_dict):
    """
    takes a dict as input and does 
    some pretty printing
    """
    print("\n")
    print("* " * 24)
    print("{0:5}".format(title))
    print("\n")

    for element in in_dict:
        act_string = "{0:35}".format(element) + " : " + str(in_dict[element])
        print(act_string)
    print("* " * 24)
    print("\n")


def main():
    """
    the main function
    """
    if len(sys.argv) != 3:
        usage_message()
        sys.exit(0)

    try:
        file_name = sys.argv[2]
        warc_file = read_file(file_name)
    except IOError, err:
        print(str(err))
        sys.exit(1)

    if "-m" in sys.argv:
        mime_types = list_mime_types(warc_file)
        pretty_printing("MIME-Type-Counter", mime_types)

    elif "-e" in sys.argv:
        extract_mime_types(warc_file)

    else:
        print("Read the file but did nothing. You should use one of the switches.")
        usage_message()

if __name__ == '__main__':
    main()
