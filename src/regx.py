import re

class Regx:
    ''' contains all reges def '''


    #--------MATCHES NAME CASRS ---------------


     #CASE ONE: All names in single line
     #re.findall(r'Before\n*\r*\n*\s+\w*.(?s)*?(?=\s+Circuit Judge)',
     #op_df.plain_text[1594][:2000])

     #CASE TWO:  Each name on seperate lines
     #re.findall(r'Before\n*\r*\n*\s+\w*.(?s)*(?=Judge[,/.](?=\n{1,}|\r{1,}))',
     # op_df.plain_text[1616][:2000])


     #CASE THREE:  There are two name connected with an 'and' string
     # r'Before\n*\r*\n*\s+\w*.(?s)*(?=Judges?[,/.](?=\n{1,}|\r{1,}))'


     #interestingly the finalcase covers all cases! Which is a great
     #example of specializing then finding a general solution.


    #I can just compile all regexs in one loop. Both this is more readable.
        
    opinion_split = re.compile(r'''
      \n*?\s+?                        #match the space before CAPS
      (?=[A-Z]+,\s.*?Judge\.|[A-Z]+,\s.*?Justice\.) #look Ahead for NAME,
                                                        #anything Judge|Justice
      |\r*\n*\s*                      #otherwise, match new-line or spaces
      (?=[Pp][Ee][Rr]\s+?[Cc][Uu][Rr][Ii][Aa][Mm]) #split on above if 'Per Curiam' cld be matched.
              ''', re.VERBOSE)

          author_regx = re.compile(r'''
      ([A-Z]+ ,                       #match Judge name in all CAPS then a ' ,'
      (?=.*?[Judge|Justice|Magistrate] #..only if any of these alternatives are seen
      \.\s+))                           # and those alernatives are followed by '.' and
                                       # one or more of spaces
        ''',re.VERBOSE)

          judge_regx = re.compile(r'''
      Before\n*\r*\n*\s+\w*.(?s)*  # matches str 'Before' and all spaces until a word
      (?=Judges?[,/.]|Justice[,/.]\*     # look-ahead for Judge(s) comma | period
      (?=\n{1,}|\r{1,}))           # look-ahead for new-line.
      ''', re.VERBOSE)

          clean_names_regx = re.compile(r'''
      Before\r*?\n*|   # replace 'Before' followed by some new-line char
      \*|                    # replace special character *
      Circuit|District|Judges?|Chief|Senior|Justice|Magistrate| # Any of these
      Associate|              # ...And this
      \s+|                    # any space
      \n*|                    # new-line
      |r*|'
      |[A-Z]$              # carriage -return
      ''', re.VERBOSE)
