import re
import io
import pandas as pd
from typing import Optional
from src import conf, protocols

logger = conf.logging.getLogger(__name__)

_mock_content_ = {"Vessel 1":"Unit.InoculationX [];Unit.Y1.PV [kW]\n00:00:00;0.000"}

################################################################################
# File loader contains helper functions to load data from DASGIP generated csv #
# files to a pandas DataFrame. It uses a list of tags to select headers        #
# to be used as DataFrame columns.                                             #
################################################################################

def file_loader(filename: Optional[str] = None) -> protocols.DATA_TYPE:
    '''
       Load file content as data blocks.

       A data block is a dictionay with _TOKEN_
       as key and content as value.
    '''

    if filename is None:
        return _mock_content_

    try:
        with open(filename) as f:
            content = f.read()
    except:
        # Return error messege if unable to load file.
        logger.error(conf._ERROR_FILE_)
        return {conf._ERROR_HEADER_: conf._ERROR_FILE_}

    return data_block_loader(content)

def data_block_loader(content: Optional[str] = None) -> protocols.DATA_TYPE:
    '''
       Breaks a string content as blocks separated by special tokens.
    '''

    if content is None:
        return _mock_content_
    
    # Get all data blocks.
    data_blocks = {}
    i=1
    end_index = 0
    while(True):
        # Get index of TOKEN.
        start_index = content.find(conf._TOKEN_.format(i), end_index)
        # Break if not found.
        if start_index == -1:
            break
        # Get index after TOKEN.
        start_index += len(conf._TOKEN_.format(i))
        # Find end of data block.
        end_index = content.find(conf._END_TOKEN_, start_index)
        # Include block only if end token found.
        if end_index != -1:
            data_blocks[f'Vessel {i}'] = content[start_index:end_index]
        i += 1

    # Return error messege if no token found.
    if data_blocks == {}:
        logger.info(conf._ERROR_NO_TOKEN_)
        return {conf._ERROR_HEADER_: conf._ERROR_NO_TOKEN_}
    
    return data_blocks

def clean_header(header: str) -> str:
    '''
       Returns cleaner header.
    '''
    # Header part between first and second dot (or EOS),
    # without loose brackets and digits/white space at the end.
    return header.split('.')[1].replace('[]','')[:-1]

def header_filter(header: str) -> bool:
    '''
       Checks if header in choice criteria.
    '''
    
    return len(set(filter(lambda x: x in header, conf._HEADER_TAGS_)))

def header_loader(data_block: str) -> protocols.DATA_TYPE:
    '''
       Builds map of selected headers to cleaner versions.
    '''

    # Get first line as headers. Remove additional double quotes.
    headers = data_block[:data_block.find('\n')].replace('\"','').split(';')
    # Make pretty headers selected headers. 
    header_map = {head:clean_header(head) for head in headers \
                  if header_filter(head)}
    
    # Check for minimum headers.
    if len(header_map)<2:
        logger.error(conf._ERROR_LOAD_HEADER_)
        return {conf._ERROR_HEADER_, conf._ERROR_LOAD_HEADER_}

    return header_map

def get_units(header_mapping: protocols.DATA_TYPE) -> protocols.DATA_TYPE:
    '''
       Build mapping from clean headers to units based on
       'dirty' to 'clean' headers mapping.
    '''
    
    logger.info('Building units mapping.')
    units_mapping = {}
    for dirty, clean in header_mapping.items():
        # Finds units inside brackets in header or None.
        x = re.search(r"\[(.*?)\]", dirty) and \
            re.search(r"\[(.*?)\]", dirty).group(1)
        # Time headers have empty brackets or no brackets.
        units_mapping[clean] = 'h' if x in ('', None) else x
    logger.info(f'{units_mapping = }')
    return units_mapping

def dataframe_loader(data_block: str,
                     headers_map: Optional[protocols.DATA_TYPE] = None
                     ) -> pd.DataFrame:
    '''
       Load DataFrame from data block.

       Considers first column to be time.
    '''

    # Load data frame with selected columns or all if no mapping provided.
    cols = headers_map and headers_map.keys()
    df = pd.read_csv(io.StringIO(data_block), sep=';', usecols=cols)
    # Rename if mapping available.
    if headers_map is not None: df.rename(columns=headers_map, inplace=True)

    # With first columns as reference remove, lines prior to first valid value.
    df.drop(range(df[df.columns[0]].first_valid_index()), inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Convert time to hours transcurred. First column must be time.
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

    # Ignore remaining leading NaN.
    return df


if __name__ == '__main__':

    content = file_loader()
    print(*content.keys())

    header = header_loader(content[next(iter(content.keys()))])
    print(
        list(get_units(header).values())
        )

    for key in content:
         print(
             dataframe_loader(content[key], header).head()
             )
