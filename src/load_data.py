
import numpy as np
import pandas as pd
from cleaner import Cleaner



def collect_all_data(cls, df):

    judges = df.copy()
    #
    for plaintext in judges.plain_text:

       top_split, bottom_split =  Cleaner.splitter(plaintext)
       bad_names = Cleaner._unclean_names(top_split)
       good_names = Cleaner._clean_names(bad_names)
       author = Cleaner._clean_author(bottom_split)

       yield list(good_names), author


def build_judges(cls, df):
    #build placeholder datframe
    jd = pd.DataFrame(index = range(len(df)),
                      columns=['Judge 1', 'Judge 2', 'Judge 3', 'Author'])
    #collect all names
    names = cls.collect_all_data(df)
    namer =[]
    auths = []
    for _names, auth  in  names:
         namer.append(_names)
         auths.append(auth)
    #pack placeholder with real data dataframe
    for i, name in enumerate(namer):
        try: #try upacking name s
            j1, j2, j3 = name
        except ValueError:
            j1, j2, j3 = [np.nan]*3
        finally:
            jd.loc[i] = j1, j2, j3, i
    jd['Author'] = auths; jd.index = df.index
    #join Dataframes
    return  df.join(jd)




def import_json(files):

    date_filed = []
    docket_number = []
    idx = []

    for f in files:
        with open(str(f)) as j:
            op = json.load(j)
            yield { 'date_filed' : op['date_filed'],
              'docket_number' : op['docket'],
              'id' : op['id'],
              'judges' : op['judges'],
              'plain_text' : op['plain_text'],
              'precedential_status' : op['precedential_status']}



if __name__ == '__main__':

	party = pd.read_csv('./jb.txt')
	df = import_json()


	party_aff = [col_name for col_name in party.keys() if 'Party' in col_name]
	party_col = party.loc[:, party_aff]
	party_col.isnull().apply(sum)
	plt.plot(party_col.isnull().apply(sum))

	party[party['Party Affiliation of President'].notnull() &
	party['Party Affiliation of President (2)'].notnull()]\
	[['Judge Last Name', 'Judge First Name', 'Birth Year']]

	df = df[df.plain_text != u'']
	opinions = build_judges(df)
	opinions = opinions.dropna(subset = ['Judge 1'])
	opinions.loc[0:, ['Judge 3']]  = [re.sub(r',' ,'', x) for x in opinions['Judge 3']]
	opinions.Author = list(Cleaner.a_c(opinions))

	opinions.loc[0:, ['Author']]  = [re.sub(r',' ,'', x) for x in opinions['Author']]

	Cleaner.docket_cleaner(opinions)

	party.loc[0:,['Party Affiliation of President', 'Birth year']] \
	[party['Judge Last Name'] == 'Burns'] # Notice the years are in decendicng order though.

	sub_opinion= party.loc[0:, ['Judge Last Name', 'Party Affiliation of President']]
	sub_opinion.drop_duplicates(subset = 'Judge Last Name', inplace = True)
	sub_opinion.index = list(sub_opinion['Judge Last Name'])

	for x, y in zip(['party_1', 'party_2', 'party_3'], ['Judge 1', 'Judge 2', 'Judge 3']):
	    opinions[x] = np.where(sub_opinion.loc[opinions[y]]\
	    ['Party Affiliation of President'] == 'Republican',1, 0)

	g =  opinions.loc[0:,['party_1', 'party_2', 'party_3']].sum(1).tolist()
	f = {'1' : 3, '2': 2, '3' : 1, '0' : 4}
	panels = map(lambda x: f[str(x)], g)
	opinions['panel_type'] = panels 