import pandas as pd
from functools import partial
import warnings
import requests as r

#warnings.filterwarnings("error")w
#csvPippaNorris =

    #"./Global Party Survey by Party CSV V1 10_Feb_2020.csv"

dfVParty = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/V-Dem-CPD-Party-V2.csv')
#reads database into pandas dataframe

dfManifesto = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/MPDataset_MPDS2022a.csv')
#reads database into pandas dataframe

dfGPS = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Global Party Survey by Party CSV V1 10_Feb_2020.csv')
#reads database into pandas dataframe

dfpartyOrigin = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Coding_List_Party_Origin.csv')
#reads google drive database into pandas dataframe



#MERGING MANIFESTO INTO PARTYORIGIN
dfManifesto = dfManifesto[['countryname', 'party', 'per607', 'per608',
                           'per7052', 'per601_2', 'per602_2', 'per607_2','per608_2', 'per7062']]

# dfpartyOrigin = dfpartyOrigin[['ID_Manifesto', 'Party']]

# dfManifesto = dfManifesto[['countryname', 'party', 'per607', 'per608']];

dfManifesto = dfManifesto.rename(columns={"party":"ID_Manifesto"})

dfpartyOrigin = dfpartyOrigin.drop(index=[0,1])

dfManifesto["ID_Manifesto"] = dfManifesto["ID_Manifesto"].astype(str)


#dfpartyOrigin['ID_Manifesto'] = pd.to_numeric(dfpartyOrigin['ID_Manifesto'], errors='coerce')

#dfpartyOrigin = dfpartyOrigin.fillna(0)

# dfManifesto = dfManifesto.replace([np.inf, -np.inf], 0)


dfpartyOrigin["ID_Manifesto"] = dfpartyOrigin["ID_Manifesto"].astype(str)

dfpartyOrigin = dfpartyOrigin.reindex(columns=['Name in DATA', 'Country', 'ID_Manifesto'])



dfpartyOrigin = pd.merge(dfpartyOrigin,dfManifesto[["ID_Manifesto", "per607",
                    "per608", "per7052", "per601_2", "per602_2", "per607_2",
                      "per608_2", "per7062"]], on= 'ID_Manifesto', how="inner")

dfpartyOrigin.to_csv('partyorigin.csv', index=False)

# dfpartyOrigin = dfpartyOrigin[["ID_Manifesto", "Party"]]


# Print the merged dataset
print(dfpartyOrigin)






#- multiculturalism : positive  -> per607
#- multiculturalism : negative  -> per608
#- Minorities Abroad: Positive -> per 7052
#- National Way of Life: Immigration: Negative -> per601_2
#- National Way of Life: Immigration: Positive -> per602_2
#- Multiculturalism: Immigrants Diversity -> per607_2
#- Multiculturalism: Immigrants Assimilation -> per608_2
#- Underprivileged Minority Groups -> per705
#- Refugees: Positive -> per7062
