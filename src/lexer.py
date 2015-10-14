class Lexer:

    def __init__( self, trie ):
        self.trie = trie


    def scan_phrases( self, phrases ):
        tokens = []
        cur_phrase = []

        for word in phrases:
            tokens.append( self.trie.get_pos( word ) ) 

        return tokens


