class Parser:

    ##################################################
    # parse_tokens function:
    #    Determines if a list of tokens builds a
    #    grammatical phrase
    #    
    #    params:
    #        tokens: list of tokens in the phrase/
    #            subphrase
    #        type (optional): determine if a phrase/
    #            subphrase is a particular type - 
    #            see grammar.txt for subphrase types
    #    returns:
    #        true/false if the phrase is/is not
    #            grammatical, resp
    ##################################################
    def parse_tokens( self, tokens, type=None ):
        ret = False

        ### Identify the possible types of phrases
        if type == None:
            ##########################################
            # Phrase may be:
            #    Noun Phrase
            ##########################################
            if 'N' in tokens[ 0 ]:
                ret |= self.parse_tokens( tokens, 'NP' )

            ##########################################
            # Phrase may be:
            #    Descriptive Phrase
            #    Descriptive Verb Phrase
            ##########################################
            if 'A' in tokens[ 0 ]:
                if self.parse_tokens( tokens, 'DP' ):
                    return True
                else:
                    ret |= self.parse_tokens( tokens, 'VP' )

            ##########################################
            # Phrase may be:
            #    Present Verb Phrase
            #    Past Verb Phrase
            #    Past Participle Verb Phrase
            #    Present Participle Verb Phrase
            ##########################################
            if 'v' in tokens[ 0 ] or 'V' in tokens[ 0 ] or 'R' in tokens[ 0 ] or 's' in tokens[ 0 ] or \
                    't' in tokens[ 0 ] or 'T' in tokens[ 0 ]:
                if self.parse_tokens( tokens, 'VVP' ):
                    return True
                elif self.parse_tokens( tokens, 'PVP' ):
                    return True
                elif self.parse_tokens( tokens, 'PPVP' ):
                    return True
                else:
                    ret |= self.parse_tokens( tokens, 'VPVP' ) 

            ##########################################
            # Phrase may be:
            #    Interjection Phrase
            ##########################################
            if '!' in tokens[ 0 ]:
                ret |= self.parse_tokens( tokens[1:] )

        ##############################################
        # Noun Phrase
        #    N N?
        ##############################################
        elif type == 'NP':
            if len( tokens ) > 2:
                return False
            for tok in tokens:
                if 'N' not in tok:
                    return False
            return True

        ##############################################
        # Descriptive Phrase
        #    A A? NP
        ##############################################
        elif type == 'DP':
            pos = 0
            for tok in tokens:
                if 'A' in tok:
                    pos += 1
                    if pos > 2:
                        return False
                else:
                    return self.parse_tokens( tokens[pos:], 'NP' )
            return False

        ##############################################
        # Descriptive Verb Phrase
        #    A A? (V|R)
        ##############################################
        elif type == 'DVP':
            length = 0
            for tok in tokens:
                length+=1
                if 'A' in tok and length > 1:
                    return False
                else:
                    if len( tokens ) == length and ( 'V' in tok or 'R' in tok ):
                        return True
                    return False
            return False

        ##############################################
        # Present Verb Phrase
        #    v? (V|R) v? |
        #    v? (V|R)+   |
        #    (V|R)+ v?
        ##############################################
        elif type == 'VVP':
            ### One adverb at beginning
            if 'v' in tokens[ 0 ]:
                ### followed by one or more simple verbs
                if len( tokens ) < 2:
                    return False
                length = 1
                for tok in tokens[1:]:
                    if 'V' in tok or 'R' in tok:
                        length+=1
                    ### if followed by an adverb, must have only been one verb
                    elif 'v' in tok:
                        if length == 2 and len( tokens ) == length+1:
                            return True
                        return False
                    else:
                        return False
                return True
            ### Zero adverbs at beginning
            elif 'V' in tokens[ 0 ] or 'R' in tokens[ 0 ]:
                ### followed by zero or more simple verbs and zero or one adverb at the end
                    length = 1
                    for tok in tokens[1:]:
                        if 'V' in tok or 'R' in tok:
                            length += 1
                        elif 'v' in tok and len( tokens ) == length+1:
                            return True
                        else:
                            return False
                    return True
            return False

        ##############################################
        # Past Verb Phrase:
        #    v? s v?
        ##############################################
        elif type == 'PVP':
            ### One adverb at beginning
            if 'v' in tokens[ 0 ]:
                ### Followed by exactly one past tense verb
                if len( tokens ) < 2 or 's' not in tokens[ 1 ]:
                    return False
                ### Followed by zero or one adverbs
                if len( tokens ) == 2:
                    return True
                if 'v' in tokens[ 2 ] and len( tokens ) == 3:
                    return True
            ### Zero adverbs at beginning
            elif 's' in tokens[ 0 ]:
                ### Followed by zero or one adverbs
                if len( tokens ) == 1:
                    return True
                if 'v' in tokens[ 1 ] and len( tokens ) == 2:
                    return True
            return False

        ##############################################
        # Past Participle Verb Phrase
        #    v? t |
        #    t v?
        ##############################################
        elif type == 'PPVP':
            ### One adverb at beginning
            if 'v' in tokens[ 0 ]:
                ### Followed by exactly one past participle verb
                if len( tokens ) == 2 and 't' in tokens[ 1 ]:
                    return True
            ### Zero adverbs at beginning
            elif 't' in tokens[ 0 ]:
                ### Followed by zero or more adverbs
                if len( tokens ) == 1:
                    return True
                if len( tokens ) == 2 and 'v' in tokens[ 1 ]:
                    return True
            return False

        ##############################################
        # Present Participle Verb Phrase
        #    v? T v?
        ##############################################
        elif type == 'VPVP':
            ### One adverb at beginning
            if 'v' in tokens[ 0 ]:
                ### Followed by exactly one present participle verb
                if len( tokens ) < 2 or 'T' not in tokens[ 1 ]:
                    return False
                ### Followed by zero or more adverbs
                if len( tokens ) == 2:
                    return True
                if 'v' in tokens[ 2 ] and len( tokens ) == 3:
                    return True
            ### Zero adverbs at beginning
            elif 'T' in tokens[ 0 ]:
                ### Followed by zero or one adverbs
                if len( tokens ) == 1:
                    return True
                if 'v' in tokens[ 1 ] and len( tokens ) == 2:
                    return True
            return False

        return ret



