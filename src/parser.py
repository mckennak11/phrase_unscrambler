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
        ### Identify the possible types of phrases
        if type == None:
            ##########################################
            # Phrase may be:
            #    Noun Phrase
            ##########################################
            if 'N' in tokens[ 0 ]:
                return self.parse_tokens( tokens, 'NP' )

            ##########################################
            # Phrase may be:
            #    Descriptive Phrase
            #    Descriptive Verb Phrase
            ##########################################
            elif 'A' in tokens[ 0 ]:
                if self.parse_tokens( tokens, 'DP' ):
                    return True
                else:
                    return self.parse_tokens( tokens, 'VP' )

            ##########################################
            # Phrase may be:
            #    Present Verb Phrase
            #    Past Verb Phrase
            #    Past Participle Verb Phrase
            #    Present Participle Verb Phrase
            ##########################################
            elif 'v' in tokens[ 0 ] or 'V' in tokens[ 0 ] or 'R' in tokens[ 0 ] or 's' in tokens[ 0 ] or \
                    't' in tokens[ 0 ] or 'T' in tokens[ 0 ]:
                if self.parse_tokens( tokens, 'VVP' ):
                    return True
                elif self.parse_tokens( tokens, 'PVP' ):
                    return True
                elif self.parse_tokens( tokens, 'PPVP' ):
                    return True
                else:
                    return self.parse_tokens( tokens, 'VPVP' ) 

            ##########################################
            # Phrase may be:
            #    Interjection Phrase
            ##########################################
            elif '!' in tokens[ 0 ]:
                return self.parse_tokens( tokens[0:] )

        ##############################################
        # Noun Phrase
        #    N+
        ##############################################
        elif type == 'NP':
            for tok in tokens:
                if 'N' not in tok:
                    return False
            return True

        ##############################################
        # Descriptive Phrase
        #    A+ NP
        ##############################################
        elif type == 'DP':
            for tok in tokens:
                if 'A' not in tok:
                    return self.parse_tokens( tokens, 'NP' )
            return False

        ##############################################
        # Descriptive Verb Phrase
        #    A+ (V|R)
        ##############################################
        elif type == 'DVP':
            len = 0
            for tok in tokens:
                len+=1
                if 'A' not in tok:
                    if len( tokens ) == len and ( 'V' in tok or 'R' in tok ):
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
                len = 1
                for tok in tokens[0:]:
                    if 'V' in tok or 'R' in tok:
                        len+=1
                    ### if followed by an adverb, must have only been one verb
                    elif 'v' in tok:
                        if len == 1 and len( tokens ) == len+1:
                            return True
                        return False
                    else:
                        return False
                return True
            ### Zero adverbs at beginning
            elif 'V' in tokens[ 0 ] or 'R' in tokens[ 0 ]:
                ### followed by zero or more simple verbs and zero or one adverb at the end
                    len = 1
                    for tok in tokens[0:]:
                        if 'V' in tok or 'R' in tok:
                            len += 1
                        elif 'v' in tok and len( tokens ) == len+1:
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
                ### Followed by zero or more adverbs
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

        return False



