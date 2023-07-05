from typing import Dict, List
from src import conf
from src import graph_maker
from src import file_loader

logger = conf.logging.getLogger(__name__)

class Handler():
    def __init__ (self, filename, from_content=False):
        super(Handler, self).__init__()
        self.filename:str = filename
        self.options = {}
        if from_content:
            self.content: Dict[str,str] = file_loader.data_block_loader(filename)
        else:
            self.content: Dict[str,str] = file_loader.file_loader(filename)
            
        if 'Error' in self.content:
            logger.error(self.content['Error'])

    @property
    def sources(self) -> List[str]:
        '''
           Returns list of sources of data in the file.
        '''

        return list(self.content.keys())

    def get_variables(self, source: str) -> List[str]:
        '''
           Returns header for source or 'Bad source' if ```source``` not found.

           Used to prompt user for columns to use.
        '''

        # If wrong source return empty
        if source not in self.sources: return ["Invalid source."]
        return list(file_loader.header_loader(self.content[source]).values())[1:]
   
    def filter_cols(self, source: str, cols: List[str]=[]) -> Dict[str,str]:
        '''
           Return header_mapping with selected header to use.
        '''

        # If wrong source return empty
        if source not in self.sources: return {"Error": "Invalid source."}
        # Get header mapping
        header_mapping = file_loader.header_loader(self.content[source])
        time = next(iter(header_mapping.values()))
        # Return filtered mapping
        if cols == []: return header_mapping
        return {k:v for k,v in header_mapping.items() if v in [time]+cols}

    ##################
    # axis font size #
    ##################
    @property
    def axis_fontsize(self) -> float:
        return self.options.get('axis_fontsize', 0.)
    
    @axis_fontsize.setter
    def axis_fontsize(self, value):
        self.options.update({'axis_fontsize':float(value)})

    @axis_fontsize.deleter
    def axis_fontsize(self):
        self.options.pop('axis_fontsize', None)

    ####################
    # legend font size #
    ####################
    @property
    def legend_fontsize(self) -> float:
        return self.options.get('legend_fontsize', 0.)
    
    @legend_fontsize.setter
    def legend_fontsize(self, value):
        self.options.update({'legend_fontsize':float(value)})

    @legend_fontsize.deleter
    def legend_fontsize(self):
        self.options.pop('legend_fontsize', None)

    ####################
    # Title Parameters #
    ####################
    @property
    def title_params(self) -> Dict[str,str]:
        return self.options.get('title_params', {})
    
    ###################
    # title font size #
    ###################
    @property
    def title_fontsize(self) -> float:
        return self.title_params.get('title_fontsize', 0.)
    
    @title_fontsize.setter
    def title_fontsize(self, value):
        self.title_params.update({'fontsize':float(value)})

    @title_fontsize.deleter
    def title_fontsize(self):
        self.title_params.pop('title_fontsize', None)

    def add_option(self, key: str, value: str):
        self.options.update({key:value})

    def remove_option(self, key: str):
        self.options.pop(key, None)

    def make_graph(self, source: str, headers_map: Dict[str,str] = {}) -> str:
        '''
           Make graph from source with selected headers and options.
        '''

        # If wrong source return empty
        if source not in self.sources: return "Invalid source."

        self.options.update({'title':source})
        units_mapping = graph_maker.get_units(headers_map)
        df = file_loader.dataframe_loader(self.content[source], headers_map)
        return graph_maker.make_graph(df, units_mapping, **self.options)
    

if __name__ == '__main__':
    handler = Handler(file_loader._FILE_)
    srcs = handler.sources
    print(srcs, '\n')
    vars = handler.get_variables(srcs[0])
    print(vars, '\n')
    mapping = handler.filter_cols(srcs[0], vars[0:3])
    print(mapping, '\n')
    print(handler.make_graph(srcs[0],mapping))