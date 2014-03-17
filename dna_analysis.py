#!/usr/bin/python

"""dna_analysis.py: Analyzes DNA files."""

__author__ = "Jackie Goordial and Luis de Bethencourt"
__copyright__ = "Copyright 2014"
__credits__ = ["Jackie Goordial", "Luis de Bethencourt"]
__license__ = "MIT"
__email__ = "luis@debethencourt.com"


from optparse import OptionParser
from sys import argv, exit


def search_terms(words_path, genome_path):
    '''Search for terms in a genome file.'''

    print "words file: %s" % (words_path)
    print "genome file: %s\n" % (genome_path)

    # Open the file in words_path as wf
    with open(words_path) as wf:
        # Loop over each line of the file.
        # word contains the line (which is a word)
        for word in wf:
            word_count = 0
            word = word.strip('\n')[:-1]      # Strip line formatting data.

            variations = []    # Store a list of variations of the word we want
            if " " in word:    # to search.
                variations.append(word.replace(" ", "-"))
                variations.append(word.replace(" ", "_"))
            if "-" in word:
                variations.append(word.replace("-", " "))

            # Loops over genome file. Not optimal but it works. Fix if
            with open(genome_path) as gf:      # performance becomes an issue.
                for genome in gf:
                    if genome[0] == ">":        # Only compare header lines
                        if word in genome:      # Look for word in header line.
                            # print genome
                            word_count += 1
                        else:
                            for var in variations:     # If word isn't in line,
                                if var in genome:      # check variations.
                                    # print genome
                                    word_count += 1

            print "%s, %d" % (word, word_count)


if __name__ == "__main__":
    parser = OptionParser(usage='''
Positional arguments:
    search-terms [words file] [genome file]
'''.strip('\n') % globals())
    (options, args) = parser.parse_args(argv[1:])

    # Over engineered parameter handling, but flexible for future growth.
    commands = ('search-terms')
    if not args or args[0] not in commands:
        parser.print_usage()
        if args:
            exit('no such command: %s' % args[0])

        exit()

    # Check the sub-command is valid.
    command = args[0]
    if command == "search-terms":
        # Check the two files are passed to the command.
        if len(args) > 2:
            words_path = args[1]
            genome_path = args[2]
            # If all is good, run search-terms with the files.
            search_terms(words_path, genome_path)
        else:
            print "missing data files"
            print "usage: search-terms [words file] [genome file]"
