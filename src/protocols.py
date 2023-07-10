from typing import Any, Dict, Protocol, Optional
from pandas import DataFrame

DATA_TYPE = Dict[str,str]
CONFIG_TYPE = Dict[str,Any]

class handler_loader(Protocol):
    '''
        Protocol module containing file_loader, header_loader
        and dataframe_loader methods.
    '''
    
    def file_loader(filename: Optional[str] = None) -> DATA_TYPE:
        ...
    def header_loader(data_block: str) -> DATA_TYPE:
        ...
    def dataframe_loader(data_block: str,
                         headers_map: Optional[DATA_TYPE] = None) -> DataFrame:
        ...
    
class handler_gmaker(Protocol):
    '''
        Protocol module containing get_units and make_graph methods.
    '''
    
    def get_units(header_map: DATA_TYPE) -> DATA_TYPE:
        ...
    def make_graph(df: DataFrame, unit_map: DATA_TYPE, **kwargs) -> str:
        ...
