from trie import Trie


trie = Trie()

#populate trie
f = open( '../mpos/mobypos.txt', 'r' )

for line in f:
    if len( line ) < 13: 
        line = line.rstrip()
        word = line[ : line.index('\\') ]
        trie.add_word( word.lower(), line[ line.index('\\') + 1 : ] )


#sanity check
print trie.contains_word( 'active' ) 

