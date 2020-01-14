from regex import Regx

class Cleaner():
    ''' A wrapper class that holds the Cleaners '''

    @classmethod
    def splitter(cls, plaintext):

        ''' Splits opinions into substring before The actual opinion begins'
            which is where the authoring judge name is written or it is a
            per Curiam / PER CURIAM. 

            input: opinion as string

            output: two strings

            # some opinons are just errata, corrections, pdf converter error
            # reports or otherwise not containing data that helps the analysis
            # I get rid of those and replace them with a placeholder. So that
            # when I place opinions back to the dataframe they go in the
            # correct location
        '''
        try:
            split = re.split(Regx.opinion_split, plaintext)
            first_split = split[0]
            second_split = split[1:] 

        except IndexError:
            pass #errata produce this error since there is no where to split
                 # ..so the entire string is returned
        finally:
            return first_split, second_split



     # Believe it or not this single function is the of everything I've gottten to 
     # do! one line.       
    @classmethod
    def _unclean_names(cls, opinion):
        return re.findall(Regx.judge_regx, opinion)

    @classmethod
    def _clean_names(cls, unclean):
        ''' return a list of three Judge names from a list containing a single
        string
        input: a list containing a single string to be parsed for Judge names
        output: a list containing three names. '''

        #for name in unclean:
        try:
            unclean_split = re.split(r',\*?\s|and', unclean[0])
            name_w_unicode = [re.sub(Regx.clean_names_regx,'', name)
                            for name in unclean_split]
            #sanitize
            for namer in name_w_unicode:
               if (namer == u'' or namer == u',' or '.' in namer) :
                   continue
               else:
                   yield namer
        except IndexError:
           yield np.nan

    @classmethod
    def _clean_author(cls, unclean):
        ''' return an author name from list of strings'''
        try:
            if unclean[0]:
                return re.match(Regx.author_regx, unclean[0]).groups(1)

        except IndexError:
            return 'Errata' #errata produce this error
        except (AttributeError, TypeError):
            return 'Per Curiam' # Per Curiam produces this error




    @classmethod
    def empty_opinions(cls,op_df):
        '''
        #remove all rows without opinions
        '''
        op_df = op_df[op_df.plain_text != u'']

    @classmethod
    def docket_cleaner(cls, op_df):
        #Lets also clean to docket number

        #Below gets the the docket numbers from the ugly string they're in.

        dok = [(re.findall(r'[^\/a-z][0-9]+', docket))
            for docket in op_df.docket_number]
        print  '....cleaning docket numbers'
        op_df['docket_number'] = [docket for sublist in dok
                                  for docket in sublist]
        print 'Run the head() function on your DataFrame, should be cleaned!'