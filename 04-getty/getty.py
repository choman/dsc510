# DSC 510
# Week 8
# Programming Assignment Week 8
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
#  Chad Homan     2021-01-25        initial code
#                                   linted
#

FILENAME = "gettysburg.txt"


# function: main()
# abstract: Main program
#
def main():
    info = {}
    data = openFile()

    for line in data:
        process_line(line, info)

    pretty_print(info)


# function: openFile()
# abstract: read in the file for processing
#
def openFile():
    data = []

    with open(FILENAME) as fp:
        data = fp.readlines()

    return data


# function: process_line()
# abstract: process the passed in line
#
def process_line(line, info):
    tmp = line.split()

    for item in tmp:
        if "--" in item:
            continue

        item = item.lower()
        item = item.replace(".", "")
        item = item.replace(",", "")

        add_word(item, info)


# function: add_word()
# abstract: Add word to dict and increment count
#
def add_word(word, info):
    if word not in info:
        info.setdefault(word, 0)

    info[word] += 1


# function: pretty_print()
# abstract: print list nice and clean
#
def pretty_print(info):
    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")
    for word in sorted(info, key=info.get, reverse=True):
        print(f"{word:12s}{info[word]:-5d}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
