class Parser:

    def parse_tokens( self, tokens ):
        #phrases of length 2
        if len( tokens ) == 2:
            if 'A' in tokens[ 0 ]:
                # A,N
                if 'N' in tokens[ 1 ]:
                    return True

        return False






