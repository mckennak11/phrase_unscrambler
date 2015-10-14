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
            all_tokens = list( permutations( tokens ) )
            all_phrases = list( permutations( cur ) )
            for i, tokens in enumerate( all_tokens ):
                if parser.parse_tokens( tokens ):
                    print all_phrases[ i ]
            del cur[ -1 ]



trie = Trie()
#populate trie
f = open( '../mpos/mobypos.txt', 'r' )

for line in f:
    if len( line ) < 13: 
        line = line.rstrip()
        word = line[ : line.index('\\') ]
        trie.add_word( word.lower(), line[ line.index('\\') + 1 : ] )

#inp = raw_input( "Enter scrambled characters: " )
#inp = inp.lower()


words = trie.build_words( 'fearthegoat', trie.root )
#words = trie.build_words( 'dgdgooo', trie.root )
print words
print "\n\n\n"


phrases,f = trie.build_phrases( words, 'fearthegoat' )
#phrases,f = trie.build_phrases( words, 'dgdgooo' )
print phrases
print "\n\n\n"

lexer = Lexer( trie )
parser = Parser()
iterate_phrases( phrases, lexer, parser )
print "\n\n\n"



