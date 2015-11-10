from trie import Trie
from lexer import Lexer
from parser import Parser
from itertools import permutations


def iterate_phrases( phrases, lexer, parser, cur=[] ):
    for word in phrases:
        if isinstance( word, basestring ):
            cur.append( word )
        #next word of the phrase
        elif len( word ) > 0:
            next = cur[:]
            iterate_phrases( word, lexer, parser, next )
            del cur[ -1 ]
        #phrase is finished
        else:
            tokens = lexer.scan_phrases( cur )
            print tokens
            all_tokens = list( permutations( tokens ) )
            all_phrases = list( permutations( cur ) )
            for i, tokens in enumerate( all_tokens ):
                if parser.parse_tokens( tokens ):
                    print all_phrases[ i ]
            del cur[ -1 ]

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


trie = Trie()
#populate trie
#f = open( '../mpos/mobypos.txt', 'r' )
f = open( '../alt12dicts/2of12id.txt', 'r' )

read_dict( f, trie )

#for line in f:
    #if line[ 0 ] != '-':
        #line = line.rstrip()
        #word = line[ : line.index('\\') ]
        #word = line[ : line.index(' ') ]
        #if len( word ) < 13:
            #print word
            #trie.add_word( word.lower(), line[ line.index('\\') + 1 : ] )
            #trie.add_word( word.lower(), line[ line.index(' ') + 1 ] )

#inp = raw_input( "Enter scrambled characters: " )
#inp = inp.lower()


#words = trie.build_words( 'fearthegoat', trie.root )
words = trie.build_words( 'dgdgooo', trie.root )
print words
print "\n\n\n"


#phrases,f = trie.build_phrases( words, 'fearthegoat' )
phrases,f = trie.build_phrases( words, 'dgdgooo' )
print phrases
print "\n\n\n"

lexer = Lexer( trie )
parser = Parser()
iterate_phrases( phrases, lexer, parser )
print "\n\n\n"



