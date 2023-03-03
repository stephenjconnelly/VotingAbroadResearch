#
#Author: Stephen James Connelly
#Code for cleaning and merging Manifesto, VParty, and GPS datasets into Origin Party database for
#voting abroad project with Chiara Superti and Beatrice Bonini.
#
#
import random

import numpy as np
# from random

import pandas as pd



#READING DATAFRAMES FROM CSVs ------------------------------------------------------
dfVParty = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/V-Dem-CPD-Party-V2.csv')
#reads database into pandas dataframe

dfManifesto = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/MPDataset_MPDS2022a.csv')
#reads database into pandas dataframe

dfGPS = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Global Party Survey by Party CSV V1 10_Feb_2020.csv')
#reads database into pandas dataframe

dfpartyOrigin = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Coding_List_Party_Origin.csv')
#reads google drive database into pandas dataframe

dfManifestoSA = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/MPDataset_MPDSSA2022a.csv')

#------------------------------------------------------------------------------------------


#SELECT MANIFESTOSA COLUMNS TO KEEP------------------------------------------------------
dfManifestoSA = dfManifestoSA[['countryname', 'party', 'edate', 'per607_1', 'per608_1',
                               'per601_2', 'per602_2', 'per607_2','per608_2']]
dfManifesto = dfManifesto[['countryname', 'party', 'edate', 'per607', 'per608',
                           'per7052', 'per601_2', 'per602_2', 'per607_2','per608_2', 'per7062']]

#------------------------------------------------------------------------------------------




# data = [['Karan',23],['Rohit',22],['Sahil',21],['Aryan',24]]
# df = pd.Dataframe(data,columns=['Name','Age'])
#
# data2 = [['Joe',23],['Joe2',23],['Joe3',21],['Joe4',24]]
# df2 = pd.Dataframe(data2,columns=['Name','Age'])
#
# df = pd.merge(df,df2[['Name','Age']], on=['Age'], how="inner")
#
#
# print(df)

# #CONVERTS IDENTIFER COLUMN TO STR. Error: Int64 and String conversion-----
# dfManifesto["ID_Manifesto"] = dfManifesto["ID_Manifesto"].astype(str)
# dfpartyOrigin["ID_Manifesto"] = dfpartyOrigin["ID_Manifesto"].astype(str)
# #-------------------------------------------------------------------------

#DATA CLEANING STEP------------------------------------------------------
#convertes identifer column to str. Error: Int64 and String conversion-----
# dfpartyOrigin = dfpartyOrigin[['ID_Manifesto', 'Party']]

#converts Manifesto's 'edate' column to simply the electon year
dfManifestoSA['edate'] = pd.to_datetime(dfManifestoSA['edate'])
dfManifestoSA['edate'] = dfManifestoSA['edate'].dt.strftime('%Y')
dfManifesto['edate'] = pd.to_datetime(dfManifesto['edate'])
dfManifesto['edate'] = dfManifesto['edate'].dt.strftime('%Y')

#renames manifesto's Party identifer column into "ID_Manifesto" and date into Manifesto_Year
dfManifestoSA = dfManifestoSA.rename(columns={"party":"ID_Manifesto"})
dfManifestoSA = dfManifestoSA.rename(columns={"edate":"Manifesto_year"})
dfManifesto = dfManifesto.rename(columns={"party":"ID_Manifesto"})
dfManifesto = dfManifesto.rename(columns={"edate":"Manifesto_year"})

dfpartyOrigin['ID_Manifesto'] = dfpartyOrigin['ID_Manifesto'].apply(lambda l: l if not pd.isna(l) else random.random() * 1000 )

dfManifestoSA["ID_Manifesto"] = dfManifestoSA["ID_Manifesto"].astype(str)
dfManifesto["ID_Manifesto"] = dfManifesto["ID_Manifesto"].astype(str)

dfpartyOrigin["ID_Manifesto"] = dfpartyOrigin["ID_Manifesto"].astype(str)

#removes rows 0 and 1, these cause errors.
dfpartyOrigin = dfpartyOrigin.drop(index=[0])
#-------------------------------------------------------------------------


#MERGING MANIFESTO INTO PARTYORIGIN------------------------------------------------------
dfpartyOrigin = pd.merge(dfpartyOrigin,dfManifestoSA, on=['Manifesto_year', 'ID_Manifesto' ], how="left")
dfpartyOrigin = pd.merge(dfpartyOrigin,dfManifesto, on=['Manifesto_year', 'ID_Manifesto'], how="left")

#------------------------------------------------------------------------------------------


#EXPORTS DATAFRAME TO CSV----------------------------
dfpartyOrigin.to_csv('partyorigin.csv', index=False)
#----------------------------------------------------


# Print the merged dataset
# dfpartyOrigin = dfpartyOrigin[['Manifesto_year', 'ID_Manifesto']]
print(dfpartyOrigin['ID_Manifesto'])






#- multiculturalism : positive  -> per607
#- multiculturalism : negative  -> per608
#- Minorities Abroad: Positive -> per 7052
#- National Way of Life: Immigration: Negative -> per601_2
#- National Way of Life: Immigration: Positive -> per602_2
#- Multiculturalism: Immigrants Diversity -> per607_2
#- Multiculturalism: Immigrants Assimilation -> per608_2
#- Underprivileged Minority Groups -> per705
#- Refugees: Positive -> per7062
