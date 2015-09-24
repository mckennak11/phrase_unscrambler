class Node:

    def __init__( self, data=None ):
        self.data = data
        self.next = {}
        self.pos = []
        self.eow = False



class Trie:

    def __init__( self ):
        self.root = Node()


    def add_word( self, word, pos ):
        cur = self.root

        for letter in word:
            if letter in cur.next and cur.next[ letter ] is not None:
                cur = cur.next[ letter ]
            else:
                temp = Node( letter )
                cur.next[ letter ] = temp
                cur = temp
        
        cur.eow = True
        for letter in pos:
            if letter not in cur.pos:
                cur.pos.append( letter )

    def build_phrases( self, scrambled ):
        words = self.build_words( scrambled, self.root )

    def build_words( self, scrambled, cur ):
        words = []
        cur_word = ""

        if cur.data is not None:
            if cur.data in scrambled:
                scrambled = scrambled.replace( cur.data, "" )
                cur_word += cur.data
            else:
                return words
        
        for next in cur.next:
            words.extend( [ cur_word + str for str in self.build_words( scrambled, cur.next[next] ) ] )

        if cur.eow:
            words.append( cur.data )

        return words

    def contains_word( self, word ):
        cur = self.root

        for letter in word:
            if letter in cur.next and cur.next[ letter ] is not None:
                cur = cur.next[ letter ]
            else:
                return False

        if cur.eow:
            return True, cur.pos

        return False
    
