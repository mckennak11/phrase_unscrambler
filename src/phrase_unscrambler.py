from trie import Trie
from lexer import Lexer
from parser import Parser
from itertools import permutations
import getopt, os, sys


####################################################
# iterate_phrases
#
# Iterate the list of phrases and tokenize.
# Phrases are formatted in the following way:
#   [ A, B, [ C, D ], C, [ E ], D, [ F, [ G ], H ] ]
#   which represents the following phrases:
#       A
#       B C
#       B D
#       C E
#       D F G
#       D H
#   empty lists indicate the end of a phrase
####################################################

def iterate_phrases( phrases, lexer, parser, output=None, cur=[] ):
    grammatical = []
    for word in phrases:
        if isinstance( word, basestring ):
            cur.append( word )
        ### next word of the phrase
        elif len( word ) > 0:
            next = cur[:]
            g = iterate_phrases( word, lexer, parser, output, next )
            if _test and len(g) > 0 :
                for p_list in g:
                    grammatical.append( [ tup for tup in p_list ] )
            del cur[ -1 ]
        ### phrase is finished
        else:
            ### Tokenize phrase
            tokens = lexer.scan_phrases( cur )
            if _debug > 0 and not _test: print tokens
            elif _test: output.write( str(tokens) )

            ### Find all permutations of the phrase
            all_tokens = list( permutations( tokens ) )
            all_phrases = list( permutations( cur ) )
            for i, tokens in enumerate( all_tokens ):
                ### Parse tokens, print phrase if grammatical
                if parser.parse_tokens( tokens ):
                    if not _test: print all_phrases[ i ]
                    else:
                        grammatical.append( all_phrases[ i ] )
            del cur[ -1 ]
    if _test: 
        return grammatical


###################################################
# read_dict
#
# Read dictionary and build trie 
#    (alt12dicts by default)
###################################################

def read_dict( file, trie ):
    for line in file:
        #these words are uncommon (see README-infl)
        if line[ 0 ].isalpha():
            #split on whitespace
            line = line.split()
            if len( line[ 0 ] ) < 13:
	        if line[1][0] == 'A' and line[0].endswith( 'ly' ):
		    trie.add_word( line[0].lower(), 'v' )
                else:
                    trie.add_word( line[0].lower(), line[1][0] )
            
            for word in line[ 2: ]:
                #throw out non-alpha words (see README-infl)
                if word.isalpha() and len( word ) < 13:
                    if line[1][0] == 'V':
                        #simple present
                        if word.endswith('s'):
                            trie.add_word( word, 'R' )
                        #simple past
                        elif word.endswith('id') or word.endswith('ed'):
                            trie.add_word( word, 's' )
                        #present participle
                        elif word.endswith('ing'):
                            trie.add_word( word, 'T' )
                        #past participle
                        elif word.endswith('en'):
                            trie.add_word( word, 't' )
                        else:
                            print word
                    elif line[1][0] == 'N':
                        #plural
                        trie.add_word( word, 'p' )
                    elif line[1][0] == 'A':
                        trie.add_word( word, 'A' )


###################################################
# run_tests
# 
# Run automated tests, verify output, and
#    generate results.
# By default, uses alt12 dictionary.
###################################################

def run_tests( trie ):
    try:
        os.remove( '../test/output.txt' )
        os.remove( '../test/results.txt' )
    except OSError:
        pass

    f = open( '../alt12dicts/2of12id.txt', 'r' )
    output = open( '../test/output.txt', 'w' )
    results = open( '../test/results.txt', 'w' )
    read_dict( f, trie )
    lexer = Lexer( trie )
    parser = Parser()
    test_case = False
    verify = False

    tests = open( '../test/tests.txt' )
    for line in tests:
        line = line.rstrip()
        if( len( line ) == 0 or line[ 0 ] == '#' ):
            continue
        elif( line[ 0 ] == ':' ):
            ### a test follows
            verify=False
            test_case=True
        elif( test_case ):
            test_case=False
            ### expected results follow
            verify=True
            output.write( '\n\n\n\tTEST CASE: '+line+'\n' )
            results.write( '\n'+line )
            
            ### Build list of possible words
            words = trie.build_words( line, trie.root )
            output.write( 'GENERATED WORDS:\n' )
            output.write( str(words).strip('[]') )

            ### Build list of possible phrases
            phrases,c = trie.build_phrases( words, line ) 
            output.write( '\n\nGENERATED PHRASES:\n')
            output.write( str(phrases) )

            ### Tokenize and parse phrases
            output.write( '\n\nGENERATED TOKENS:\n')
            grammatical = iterate_phrases( phrases, lexer, parser, output )
            output.write( '\n\nGRAMMATICAL PHRASES:\n' )
            output.write( str(grammatical) )
        elif( verify ):
            phrases = []
            for tup in grammatical:
                p = ' '.join( [ i for i in tup] )
                phrases.append( p )
            results.write( '\n\t' + line )
            if line in phrases:
                results.write( '\n\tPASS' )
            else:
                results.write( '\n\tFAIL' )


###################################################
# help
#
# Print instructions for use, plus all possible
#    command-line arguments
# Also available in ../readme.txt
###################################################

def help():
    print '\n\nStandard Usage: Run phrase_unscrambler.py with no arguments,\nenter scrambled phrase when prompted\n'
    print '-h, --help \t\t Help'
    print '-d, --debug [level] \t Level must be an int, see readme.txt for details'
    print '-t, --test \t\t Run automated tests. See ../test/results.txt for results'
    print '\n\n'


###################################################
# main
#
# Parse command-line arguments and perform
#    corresponding behavior (see ../readme.txt).
#
# 1.Prompt user for scrambled phrase from stdin.
# 2.Identify possible words
# 3.Identify possible phrases
# 4.Tokenize phrases
# 5.Parse tokens and print grammatical phrases.
###################################################

def main( argv ):
    trie = Trie()
    global _debug 
    _debug = 0
    global _test
    _test = False

    try:
        opts, args = getopt.getopt( argv, 'hd:t', ['help', 'debug=', 'test'] )
    except getopt.GetoptError:
        print 'Invalid Option, see ../readme.txt'
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ('-d', '--debug'):
            arg = int(arg)
            if arg >= 0 and arg <= 3:
                _debug = arg
            else:
                print 'Currently support debug levels 0-3!'
        elif opt in ('-t', '--test'):
            _test = True
            run_tests( trie )
            sys.exit()
            
    ### Populate trie
    #f = open( '../mpos/mopypos.txt', 'r' )
    f = open( '../alt12dicts/2of12id.txt', 'r' )
    read_dict( f, trie )

    ### Read in scrambled phrase
    inp = raw_input( 'Enter scrambed charactes: ')
    inp = inp.lower()

    ### Build list of words
    words = trie.build_words( inp, trie.root )
    if _debug > 1: print words

    ### Build list of phrases
    phrases,f = trie.build_phrases( words, inp )
    if _debug > 2: print phrases + '\n'
    
    lexer = Lexer( trie )
    parser = Parser()
    ### Tokenize and parse phrases
    iterate_phrases( phrases, lexer, parser )


if __name__ == "__main__":
    main(sys.argv[1:])



