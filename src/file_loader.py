import io
import pandas as pd
from typing import Dict
from src import conf

logger = conf.logging.getLogger(__name__)

def file_loader(filename: str = conf._FILE_) -> Dict[str,str]:
    '''
       Load file content as data blocks.

       A data block is a dictionay with _TOKEN_
       as key and content as value.
    '''

    try:
        with open(filename) as f:
            content = f.read()
    except:
        logger.error("File not found")
        return {"Error": "File not found"}

    return data_block_loader(content)

def data_block_loader(content: str) -> Dict[str,str]:
    '''
       Load data blocks from content.
    '''

    # Get all data blocks
    data_blocks = {}
    i=1
    end_index = 0
    while(True):
        # Get index of TOKEN
        start_index = content.find(conf._TOKEN_.format(i), end_index)
        # Break if not found
        if start_index == -1:
            break
        # Get index after TOKEN
        start_index += len(conf._TOKEN_.format(i))
        # Find end of data block
        end_index = content.find(conf._END_TOKEN_, start_index)
        data_blocks[f'Vessel {i}'] = content[start_index:end_index]
        i += 1

    return data_blocks

def header_loader(content: str) -> Dict[str, str]:
    '''
       Reads .PV values and InoculationTime from content.
    '''

    headers = content[:content.find('\n')].replace('\"','').split(';')
    pretty_headers = [head.split('.')[1].replace(' []','')[:-1] for head in headers \
                      if '.PV' in head or 'Inoculation' in head]
    if len(headers)<2 or len(pretty_headers)<2:
        logger.error("Error loading headers")
        return {"Error", "Error loading headers"}

    # Get only InoculationTime and .PV headers.
    headers = [headers[2]] + [head for head in headers if '.PV' in head]
    return {a:b for a,b in zip(headers,pretty_headers)}

def dataframe_loader(content: str, headers_map: Dict[str,str]={}) -> pd.DataFrame:
    '''
       Load DataFrame from content.
    '''

    # Load data frame with columns selected or all if no mapping provided.
    cols = None if headers_map == {} else headers_map.keys()
    df = pd.read_csv(io.StringIO(content), sep=';', usecols=cols)
    # Rename if mapping available
    if headers_map is not None: df.rename(columns=headers_map, inplace=True)

    # Remove lines prior to inoculation.
    df.drop(range(df[df.columns[0]].first_valid_index()), inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Convert time to hours transcurred.
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: (x-df[df.columns[0]][0]).total_seconds()/3600)

    # Sets all NaN values on a Pandas DataFrame column
    # to the last previous valid value in the column.
    for column in df.columns:
        prev_value = None
        for i in range(len(df)):
            if pd.isna(df.at[i,column]):
                df.at[i,column] = prev_value
            else:
                prev_value = df.at[i,column]

    return df

if __name__ == '__main__':

    content = file_loader()
    print(content.keys())

    # for key in content:
    #     print(header_loader(content[key]))

    for key in content:
         print(dataframe_loader(content[key], header_loader(content[key])).head())
