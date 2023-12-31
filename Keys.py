# (E)TL: Data extraction
FINANCIAL_MODELING_PREP_KEY = ""        # <- insert you financial modeling prep key between the quotation marks
AZURE_STORE_CONNECTION_STRING = ""      # <- insert your azure data store connection key from access keys here


# E(T)L: Cleaning and transformation

#  How-To: read csv from Azure blob Storage and store in a DataFrame:
#  Refer to: https://stackoverflow.com/a/68620427

constituents_SAS_url = ""       # <- insert your Azure Blob constituents.csv SAS url here
sectors_SAS_url = ""            # <- insert your Azure Blob sector.csv SAS url here
ratios_SAS_url = ""             # <- insert your Azure Blob ratios.csv SAS url here
stockperformance_SAS_url = ""   # <- insert your Azure Blob stockPerformance.csv SAS url here

# ET(L): Loading to Azure Data Lake

# process of finding Data Lake connection string similar to finding Azure Blob connection string
# Refer to: https://stackoverflow.com/a/68620427
AZURE_STORE_CONNECTION_STRING_DATA_LAKE = ""    # <- insert your azure data lake connection key from access keys here

