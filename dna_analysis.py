#!/usr/bin/python

"""dna_analysis.py: Analyzes DNA files."""

__author__ = "Jackie Goordial and Luis de Bethencourt"
__copyright__ = "Copyright 2014"
__credits__ = ["Jackie Goordial", "Luis de Bethencourt"]
__license__ = "MIT"
__email__ = "luis@debethencourt.com"


from optparse import OptionParser
from sys import argv, exit, stdout

_version = 0.1


def search_terms(words_path, genome_paths, options):
    '''Search for terms in a genome file.'''

    if options.verbose:
        print "words file: %s" % (words_path)
        for gp in genome_paths:
            print "genome file: %s\n" % (gp)

    # Print header of the data table (blank cell, genome file 1, genome file N)
    stdout.write("%20s\t" % (" "))
    for gp in genome_paths:
        stdout.write("%s\t" % (gp))
    stdout.write("\n")

    # Open the file in words_path as wf
    with open(words_path) as wf:
        # Loop over each line of the file.
        # word contains the line (which is a word)
        for word in wf:
            word_counts = {}
            word = word.strip('\n')[:-1]      # Strip line formatting data.

            if options.verbose:
                print "\nStart search for: %s" % (word)

            variations = []    # Store a list of variations of the word we want
            if " " in word:    # to search.
                variations.append(word.replace(" ", "-"))
                variations.append(word.replace(" ", "_"))
            if "-" in word:
                variations.append(word.replace("-", " "))

            # Loops over genome files. Not optimal but it works. Fix if
            for gp in genome_paths:            # performance becomes an issue.
                word_counts[gp] = 0

                with open(gp) as gf:
                    for genome in gf:
                        if genome[0] == ">":    # Only compare header lines
                            found = False       # Look for word in header line.

                            genome_l = genome.lower()
                            if word.lower() in genome_l:
                                found = True
                            else:                      # If wors isn't in line,
                                for var in variations:     # check variations
                                    if var.lower() in genome_l:
                                        found = True

                            if found:
                                word_counts[gp] += 1
                                if options.verbose:
                                    print genome

            # Print data (search term, count in gnome file 1, count in file n)
            stdout.write("%20s\t" % (word))
            for gp in genome_paths:
                stdout.write("%5d\t" % (word_counts[gp]))
            stdout.write("\n")


if __name__ == "__main__":
    version = _version
    parser = OptionParser(version='%%prog %s' % version,
                          usage='''
usage: %%prog [--version] [--verbose]

Command-line DNA Analysis

Positional arguments:
    search-terms [words file] [genome file 1..2..N]

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
            genome_paths = []

            gfs = 2
            while gfs < len(args):
                genome_paths.append(args[gfs])
                gfs += 1

            # If all is good, run search-terms with the files.
            search_terms(words_path, genome_paths, options)
        else:
            print "missing data files"
            print "usage: search-terms [words file] [genome file]"
