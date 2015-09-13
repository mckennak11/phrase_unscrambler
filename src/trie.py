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
    
