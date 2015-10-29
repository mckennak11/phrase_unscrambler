class Parser:

    def parse_tokens( self, tokens ):
        #phrases of length 1
        if len( tokens ) == 1:
            # N - 'fireman'
            if 'N' in tokens[ 0 ]:
                return True
   
            # V or r - 'run'
            elif 'V' in tokens[ 0 ] or 'R' in tokens[ 0 ]:
                return True

        #phrases of length 2
        elif len( tokens ) == 2:
            if 'A' in tokens[ 0 ]:
                # A,N - 'good dog'
                if 'N' in tokens[ 1 ]:
                    return True

                # A,V or A,r - 'good run'
                elif 'V' in tokens[ 1 ] or 'R' in tokens[ 1 ]:
                    return True

            elif 'v' in tokens[ 0 ]:
                # v,V or a,r - 'quickly run'
                if 'V' in tokens[ 1 ] or 'R' in tokens[ 1 ]:
                    return True

                # v,s - 'quickly ran'
                elif 's' in tokens[ 1 ]:
                    return True

                # v,t - 'quickly spoken'
                #elif 't' in tokens[ 1 ]:
                    #return True

            

        return False






