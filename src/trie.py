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

    def build_phrases( self, words, scrambled, length=0 ):
        phrases = []
        temp = []
        full_phrase = False
        
        for word in words:
            rem_letters = scrambled
            flag = True

            for letter in word:
                if letter in rem_letters:
                    rem_letters = rem_letters.replace( letter, "", 1 )
                else:
                    flag = False
                    break
            
            if flag and length < 5:
                rem_words = self.build_words_from_list( rem_letters, words[ words.index( word ): ] )
                if len( rem_letters ) > 0 and len( rem_words ) > 0:
                    p, full = self.build_phrases( rem_words, rem_letters, length+1 )
                    
                    if full:
                        phrases.append( word )
                        phrases.append( p )
                        full_phrase = True
                elif len( rem_letters ) == 0:
                    full_phrase = True
                    phrases.append( word ) 
   
        return phrases, full_phrase

    def build_words( self, scrambled, cur ):
        words = []
        cur_word = ""

        if cur.data is not None:
            if cur.data in scrambled:
                scrambled = scrambled.replace( cur.data, "", 1 )
                cur_word += cur.data
            else:
                return words
        
        for next in cur.next:
            words.extend( [ cur_word + str for str in self.build_words( scrambled, cur.next[next] ) ] )

        if cur.eow:
            words.append( cur.data )

        return words

    def build_words_from_list( self, scrambled, words ):
        rem_words = []

        for word in words:
            rem_letters = scrambled
            flag = True
            for letter in word:
                if letter in rem_letters:
                    rem_letters.replace( letter, "", 1 )
                else:
                    flag = False
            if flag:
                rem_words.append( word )
        return rem_words

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

        






