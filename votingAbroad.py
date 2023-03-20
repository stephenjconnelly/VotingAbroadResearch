#
#Author: Stephen James Connelly
#Code for cleaning and merging Manifesto, VParty, and GPS datasets into Origin Party database for
#voting abroad project with Chiara Superti and Beatrice Bonini.
#
#
import pandas as pd
import numpy as np



#READING DATAFRAMES FROM CSVs ------------------------------------------------------
#reads database into pandas dataframe
dfVParty = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/V-Dem-CPD-Party-V2.csv')

#reads Manifesto database into pandas dataframe
dfManifesto = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/MPDataset_MPDS2022a.csv')
dfManifestoSA = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/MPDataset_MPDSSA2022a.csv')

#reads GPS database into pandas dataframe
dfGPS = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Global Party Survey by Party CSV V1 10_Feb_2020.csv')

#reads google drive database into pandas dataframe
dfpartyOrigin = pd.read_csv('/Users/danielaconnelly/Desktop/votingAbroad/Coding_List_Party_Origin - Sheet1.csv')
#------------------------------------------------------------------------------------------

#SELECT MANIFESTO COLUMNS TO KEEP------------------------------------------------------
dfManifestoSA = dfManifestoSA[['party', 'edate', 'per607_1', 'per608_1',
                               'per601_2', 'per602_2', 'per607_2','per608_2', 'rile',
                               'per705']]
dfManifesto = dfManifesto[['party', 'edate', 'per607', 'per608',
                           'per7052', 'per601_2', 'per602_2', 'per607_2','per608_2',
                           'per7062', 'rile']]
#------------------------------------------------------------------------------------------

#SELECT VPARTY COLUMNS TO KEEP------------------------------------------------------
dfVParty = dfVParty[['v2paimmig_ord', 'pf_party_id', 'year', 'v2pariglef_ord']]
#-----------------------------------------------------------------------------------

#SELECT GPS COLUMNS TO KEEP------------------------------------------------------
dfGPS = dfGPS[['ID_GPS', 'Elec_year', 'V10', 'V4_Ord']]
#--------------------------------------------------------------------------------

#converts Manifesto's 'edate' column, MM/DD/YYYY, to simply YYYY---------
dfManifestoSA['edate'] = pd.to_datetime(dfManifestoSA['edate'])
dfManifestoSA['edate'] = dfManifestoSA['edate'].dt.strftime('%Y')
dfManifesto['edate'] = pd.to_datetime(dfManifesto['edate'])
dfManifesto['edate'] = dfManifesto['edate'].dt.strftime('%Y')
#-------------------------------------------------------------------------

#renames manifesto unique identifer column into "ID_Manifesto" and date into Manifesto_Year
dfManifestoSA = dfManifestoSA.rename(columns={"party":"ID_Manifesto"})
dfManifestoSA = dfManifestoSA.rename(columns={"edate":"Manifesto_year"})
dfManifesto = dfManifesto.rename(columns={"party":"ID_Manifesto"})
dfManifesto = dfManifesto.rename(columns={"edate":"Manifesto_year"})
#-------------------------------------------------------------------------------------------

#renames V2Party unique identifer column and date column into 'V_party_year' and 'ID_V_party'
dfVParty = dfVParty.rename(columns={"pf_party_id":"ID_V_party"})
dfVParty = dfVParty.rename(columns={"year":"V_party_year"})
#--------------------------------------------------------------------------------------------

#renames GPS unique identifer column and date column into 'GPS_Elec_year' and 'ID_GPS'
dfGPS = dfGPS.rename(columns={"ID_GPS":"ID_GPS"})
dfGPS = dfGPS.rename(columns={"Elec_year":"GPS_Elec_year"})
#-------------------------------------------------------------------------

#removes row 0, this cause errors-----------------
dfpartyOrigin = dfpartyOrigin.drop(index=[0])
#-------------------------------------------------

#converts partyorigin, manifesto, VParty columns to int64 and converts bad values (ie. 'N/A') to NaN values ------------------
dfpartyOrigin[["ID_Manifesto", "Manifesto_year"]]= dfpartyOrigin[["ID_Manifesto", "Manifesto_year"]].replace('N/A ', np.nan)
dfpartyOrigin[["ID_Manifesto", "Manifesto_year"]]= dfpartyOrigin[["ID_Manifesto", "Manifesto_year"]].replace('1986-2017', np.nan)
dfManifestoSA[["ID_Manifesto", "Manifesto_year"]] = dfManifestoSA[["ID_Manifesto", "Manifesto_year"]].astype('Int64')
dfManifesto[["ID_Manifesto", "Manifesto_year"]] = dfManifesto[["ID_Manifesto", "Manifesto_year"]].astype('Int64')
dfpartyOrigin[["ID_Manifesto", "Manifesto_year", 'V_party_year', 'ID_V_party' ]] = dfpartyOrigin[["ID_Manifesto",
                                "Manifesto_year", 'V_party_year', 'ID_V_party']].astype('Int64')
dfVParty[['V_party_year', 'ID_V_party' ]] = dfVParty[['V_party_year', 'ID_V_party']].astype('Int64')
#-------------------------------------------------------------------------------------------------------------------------------

#MERGING MANIFESTO INTO PARTYORIGIN------------------------------------------------------
dfpartyOrigin = pd.merge(dfpartyOrigin,dfManifestoSA, on=['Manifesto_year', 'ID_Manifesto'], how="left")
dfpartyOrigin = pd.merge(dfpartyOrigin,dfManifesto, on=['Manifesto_year', 'ID_Manifesto'], how="left")
#------------------------------------------------------------------------------------------

#MERGING VPARTY INTO PARTYORIGIN----------------------------------------------------------
dfpartyOrigin = pd.merge(dfpartyOrigin,dfVParty, on=['V_party_year', 'ID_V_party'], how="left")
#------------------------------------------------------------------------------------------

#MERGING GPS INTO PARTYORIGIN-------------------------------------------------------------
dfpartyOrigin = pd.merge(dfpartyOrigin,dfGPS, on=['ID_GPS', 'GPS_Elec_year'], how="left")
#------------------------------------------------------------------------------------------

#EXPORTS DATAFRAME TO CSV----------------------------
dfpartyOrigin.to_csv('partyorigin.csv', index=False)
#----------------------------------------------------

# Print the merged dataset---------
print(dfpartyOrigin['ID_Manifesto'])
#----------------------------------

#Manifesto variables:
#- multiculturalism : positive  -> per607
#- multiculturalism : negative  -> per608
#- Minorities Abroad: Positive -> per 7052
#- National Way of Life: Immigration: Negative -> per601_2
#- National Way of Life: Immigration: Positive -> per602_2
#- Multiculturalism: Immigrants Diversity -> per607_2
#- Multiculturalism: Immigrants Assimilation -> per608_2
#- Underprivileged Minority Groups -> per705
#- Refugees: Positive -> per7062
#- Left-Right Index -> rile

#ManifestoSA variables:
#- National Way of Life: Immigration: Negative -> per601_2
#- National Way of Life: Immigration: Positive -> per602_2
#- Multiculturalism: Immigrants Diversity -> per607_2
#- Multiculturalism: Immigrants Assimilation -> per608_2
#- multiculturalism : positive  -> per607_1
#- multiculturalism : negative  -> per608_1
#- Left-Right index -> rile
#- Underprivileged Minority Groups -> per705

#VParty variables:
#-Immigration : v2paimming
#-Economic left-right scale: v2pariglef

#GPS variables:
#-Immigration: v10
#-Left-Right: V4_Ord

