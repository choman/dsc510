# DSC 510
# Week 9
# Programming Assignment Week 9
# Author: Chad Homan
# 2021/01/05
#
# Abstract: We will create a program which performs three essential
#           operations. It will process this .txt file: Gettysburg.txt.
#           Calculate the total words, and output the number of
#           occurrences of each word in the file.
#
#           - Open the file and process each line.
#           - Either add each word to the dictionary with a frequency
#             of 1 or update the word’s count by 1.
#           - Nicely print the output, in this case from high to low
#             frequency. You should use string formatting for this.
#
#           We want to achieve each major goal with a function
#           (one function, one action). We can find four functions
#           that need to be created.
#
#           add_word: Add each word to the dictionary. Parameters are
#           the word and a dictionary. No return value.
#
#           Process_line: There is some work to be done to process
#           the line: strip off various characters, split out the words,
#           and so on. Parameters are a line and the dictionary. It calls
#           the function add word with each processed word. No return value.
#
#           Pretty_print: Because formatted printing can be messy and
#           often particular to each situation (meaning that we might
#           need to modify it later), we separated out the printing
#           function. The parameter is a dictionary. No return value.
#
#           main: We will use a main function as the main program. As
#           usual, it will open the file and call process_line on each
#           line. When finished, it will call pretty_print to print
#           the dictionary.
#
#           In the main function, you will need to open the file. We
#           will cover more regarding opening of files next week but
#           I wanted to provide you with the block of code you will
#           utilize to open the file, see below.
#
# Create a program with the following requirements:
#
#  - Your program must have a header.
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-12        final lint before subnitting
#  Chad Homan     2021-02-09        Added file checks to only write to
#                                   current directory or /tmp
#  Chad Homan     2021-02-08        Initial code to write and append to a
#                                   user specified file.
#  Chad Homan     2021-02-05        Still playing with the sorting, did not
#                                   like the multiple loops from the
#                                   pretty_print_sorted1(). After some
#                                   experimenting, added another function:
#                                      - pretty_print_sorted2()
#  Chad Homan     2021-02-02        Added a second sort to make the pretty
#                                   print sort alphabetically:
#                                      - pretty_print_sorted1()
#  Chad Homan     2021-01-27        resolved issue reading file into list
#                                   fixed pretty_print padding
#  Chad Homan     2021-01-25        initial code
#                                   linted
#                                   added function docstrings
#

import os
import string

PRETTY_PRINT         = 0
PRETTY_PRINT_SORTED1 = 1
PRETTY_PRINT_SORTED2 = 2
FILENAME             = "gettysburg.txt"
USE_BUFFER           = False


# function: main()
# abstract: Main program
#
def main():
    info = {}
    data = []
    filename = None

    option = greetings()

    if option > 1:
        filename = getFilename()

    if USE_BUFFER:
        openFile(data)
        for line in data:
            process_line(line, info)

    else:
        with open(FILENAME) as gba_file:
            for line in gba_file:
                process_line(line, info)

    if option == 1 or option == 3:
        if PRETTY_PRINT == PRETTY_PRINT_SORTED1:
            pretty_print_sorted1(info)

        elif PRETTY_PRINT == PRETTY_PRINT_SORTED2:
            pretty_print_sorted2(info)

        else:
            pretty_print(info)

    if option > 1 and filename is not None:
        write_header(filename, info)
        process_file(filename, info)


def getFilename():
    tmp   = "/tmp/"
    error = "Invalid, please enter a filename"

    while True:
        path = input("Please enter a filename: ")
        path = os.path.normpath(path)

        if "getty.py" in path or "gettysburg.txt" in path:
            print(error)
            continue

        if path.startswith(tmp) and len(path) > len(tmp):
            break

        if '/' in path or '\\' in path:
            print(error)
            continue

        break

    return path


def greetings():
    error = "Invalid option, please enter a valid option"
    msg = """
How would you like to see the Gettysburg info:

   1) On the Screen
   2) Output to file
   3) Output to both
"""
    print(f"{msg}")

    while True:
        ans = input("Enter Selection [1-3]: ")

        try:
            ans = int(ans)

            if ans < 1 or ans > 3:
                print(error)
                continue

            break

        except ValueError:
            print(error)

    return ans


# function: openFile()
# abstract: read in the file for processing
#
def openFile(data):
    """gets the contents of FILENAME"""
    with open(FILENAME) as fp:
        data.extend(fp.readlines())


# function: process_line()
# abstract: process the passed in line
#
def process_line(line, info):
    """Process_line: There is some work to be done to process
    the line: strip off various characters, split out the words,
    and so on. Parameters are a line and the dictionary. It calls
    the function add word with each processed word.

    No return value.
    """

    for item in line.split():
        if "--" in item:
            continue

        item = item.strip().lower()
        item = item.strip(string.punctuation)

        add_word(item, info)


# function: add_word()
# abstract: Add word to dict and increment count
#
def add_word(word, info):
    """add_word: Add each word to the dictionary. Parameters are
    the word and a dictionary.

    No return value.
    """

    info.setdefault(word, 0)
    info[word] += 1


# function: pretty_print()
# abstract: print list nice and clean
#
def pretty_print(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.

    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    for word in sorted(info, key=info.get, reverse=True):
        print(f"{word:<12}{info[word]:>5}")


def write_header(fname, info):
    with open(fname, "w") as fp:
        fp.write(f"Length of dictionary: {len(info)}\n")


def process_file(fname, info):
    with open(fname, "a") as fp:
        fp.write("Word          Count\n")
        fp.write("-------------------\n")

        for word in sorted(info, key=info.get, reverse=True):
            fp.write(f"{word:<12}{info[word]:>5}\n")

    print(f"\nOutput file: {fname}")


# function: pretty_print_sorted1()
# abstract: print list nice and clean and alphabetical
#
def pretty_print_sorted1(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.


    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    mydict = {}
    for word in sorted(info, key=info.get, reverse=True):
        mydict.setdefault(info[word], [])
        mydict[info[word]].append((word, info[word]))

    for k, v in reversed(sorted(mydict.items())):
        for i in sorted(v):
            print(f"{i[0]:<12}{i[1]:>5}")


# function: pretty_print_sorted2()
# abstract: print list nice and clean and alphabetical
#
def pretty_print_sorted2(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.

    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    for word in sorted(sorted(info), key=info.get, reverse=True):
        print(f"{word:<12}{info[word]:>5}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
