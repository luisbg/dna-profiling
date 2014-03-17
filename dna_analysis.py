#!/usr/bin/python

"""dna_analysis.py: Analyzes DNA files."""

__author__ = "Jackie Goordial and Luis de Bethencourt"
__copyright__ = "Copyright 2014"
__credits__ = ["Jackie Goordial", "Luis de Bethencourt"]
__license__ = "MIT"
__email__ = "luis@debethencourt.com"


from optparse import OptionParser
from sys import argv, exit

_version = 0.1


def search_terms(words_path, genome_path, options):
    '''Search for terms in a genome file.'''

    if options.verbose:
        print "words file: %s" % (words_path)
        print "genome file: %s\n" % (genome_path)

    # Open the file in words_path as wf
    with open(words_path) as wf:
        # Loop over each line of the file.
        # word contains the line (which is a word)
        for word in wf:
            word_count = 0
            word = word.strip('\n')[:-1]      # Strip line formatting data.

            if options.verbose:
                print "Start search for: %s" % (word)

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
                        found = False           # Look for word in header line.

                        genome_l = genome.lower()
                        if word.lower() in genome_l:
                            found = True
                        else:
                            for var in variations:     # If word isn't in line,
                                if var.lower() in genome_l:      # check variations.
                                    found = True

                        if found:
                            word_count += 1
                            if options.verbose:
                                print genome

            print "%s, %d" % (word, word_count)


if __name__ == "__main__":
    version = _version
    parser = OptionParser(version='%%prog %s' % version,
                          usage='''
usage: %%prog [--version] [--verbose]

Command-line DNA Analysis

Positional arguments:
    search-terms [words file] [genome file]

Examples:
  %%prog --verbose search-terms searchwords.txt JG3.txt
'''.strip('\n') % globals())
    parser.add_option('-v', '--verbose', action='count', dest='verbose',
                      default=0, help='Print more info')
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
            search_terms(words_path, genome_path, options)
        else:
            print "missing data files"
            print "usage: search-terms [words file] [genome file]"
