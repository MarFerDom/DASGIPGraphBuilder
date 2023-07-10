from typing import List, Optional, Union
from src import conf, os_ops, protocols
from src import DASGIP_loader, graph_maker

logger = conf.logging.getLogger(__name__)

class Handler():
    def __init__ (self,
                  content_source: Union[str, protocols.DATA_TYPE], *,
                  filename: Optional[str] = None,
                  loader: protocols.handler_loader = DASGIP_loader,
                  graph_maker: protocols.handler_gmaker = graph_maker) -> None:
        '''
           Initializes handler with content from source and filename.

           If content_source is a dict:
            - it is assumed to be a content dictionary.
            - If filename is not None, it is used as file without file type.

           else:
            - it is assumed to be a file path and used to get filename.

           
        '''
        
        super(Handler, self).__init__()
        # Keep loader module.
        self.loader = loader
        # Keep graph maker module.
        self.graph_maker = graph_maker
        # Create graph options mapping
        self.options = {}

        # Check content type for str or DATA_TYPE.
        if type(content_source) is str:
            # Get proper file name.
            self.filename = os_ops.std_name(str(content_source))
            # File loader deals with bad filenames.
            self.content: protocols.DATA_TYPE = loader.file_loader(content_source)
        else:
            # Get proper file name or None.
            self.filename = filename and os_ops.std_name(filename)
            self.content: protocols.DATA_TYPE = content_source
            
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
           Returns headers except first column for source or
           'Bad source' if ```source``` not found.
        '''

        # If wrong source return empty
        if source not in self.sources: return ["Invalid source."]
        return list(
            self.loader.header_loader(self.content[source]).values())[1:]
   
    def filter_cols(self, source: str,
                    cols: List[str]=[]) -> protocols.DATA_TYPE:
        '''
           Return header_mapping with selected header from cols.

           Always keeps the fist column as 'time'.
           If cols is empty, returns complete mapping.
        '''

        # If wrong source return empty
        if source not in self.sources: return {"Error": "Invalid source."}
        # Get header mapping
        header_mapping = self.loader.header_loader(self.content[source])
        # Uses first column as time
        time = next(iter(header_mapping.values()))
        # Return filtered mapping
        if cols == []: return header_mapping
        return {k:v for k,v in header_mapping.items() if v in {time, *cols}}

    ##################
    # axis font size #
    ##################
    @property
    def axis_fontsize(self) -> float:
        return self.options.get('axis_fontsize', 0.)
    
    @axis_fontsize.setter
    def axis_fontsize(self, value) -> None:
        self.options.update({'axis_fontsize':float(value)})

    @axis_fontsize.deleter
    def axis_fontsize(self) -> None:
        self.options.pop('axis_fontsize', None)

    ####################
    # legend font size #
    ####################
    @property
    def legend_fontsize(self) -> float:
        return self.options.get('legend_fontsize', 0.)
    
    @legend_fontsize.setter
    def legend_fontsize(self, value) -> None:
        self.options.update({'legend_fontsize':float(value)})

    @legend_fontsize.deleter
    def legend_fontsize(self) -> None:
        self.options.pop('legend_fontsize', None)

    ####################
    # Title Parameters #
    ####################
    @property
    def title_params(self) -> protocols.DATA_TYPE:
        return self.options.get('title_params', {})
    
    ###################
    # title font size #
    ###################
    @property
    def title_fontsize(self) -> float:
        return self.title_params.get('title_fontsize', 0.)
    
    @title_fontsize.setter
    def title_fontsize(self, value) -> None:
        self.title_params.update({'fontsize':float(value)})

    @title_fontsize.deleter
    def title_fontsize(self) -> None:
        self.title_params.pop('title_fontsize', None)

    def add_option(self, key: str = None, value: str = None,
                   data: protocols.DATA_TYPE = {}) -> None:
        '''
           Add key, value pair to dictionary of graph options,
           later used to make graph.
        '''
        
        if key is not None:
            self.options.update({key:value})
        self.options.update(data)

    def remove_option(self, key: str) -> None:
        self.options.pop(key, None)

    def make_graph(self, source: str,
                   headers_map: protocols.DATA_TYPE = {}) -> str:
        '''
           Make graph from source with selected headers and options.
        '''

        # If wrong source return empty
        if source not in self.sources: return "Invalid source."
        # Set title as source
        self.options.update({'title':source})
        # Get units mapping. Graph maker deals with bad header map.
        units_mapping = self.graph_maker.get_units(headers_map)
        # Get dataframe. Loader deals with bad input.
        df = self.loader.dataframe_loader(self.content[source], headers_map)
        # Make graph. Graph maker deals with bad input.
        return self.graph_maker.make_graph(df,
                                           units_mapping,
                                           **self.options,
                                           filename=self.filename)
    

if __name__ == '__main__':
    handler = Handler(DASGIP_loader._mock_content_)
    srcs = handler.sources
    print(srcs, '\n')
    vars = handler.get_variables(srcs[0])
    print(vars, '\n')
    mapping = handler.filter_cols(srcs[0], vars)
    print(mapping, '\n')
    print(handler.make_graph(srcs[0],mapping))