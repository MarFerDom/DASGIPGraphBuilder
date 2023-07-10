import matplotlib
import numpy as np
import pandas as pd
from typing import Optional
from src import conf, protocols, os_ops

# Set non-GUI backend for matplotlib.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# Set style for matplotlib.
plt.style.use(conf._PLOT_STYLE_)

logger = conf.logging.getLogger(__name__)

_TEST_FILENAME_ = "dummy.png"
_TIME_FORMAT_ = "%Y_%m_%d(%a)-%I_%M%p_"

def _build_color_map(units_mapping: protocols.DATA_TYPE,
                   color_map: Optional[protocols.DATA_TYPE] = None
                   ) -> protocols.DATA_TYPE:
    '''
       Build color map compatible with units map.

       Adds black to missing values in color map.
       Adds '' to missing values in units map.
    '''
    
    logger.info('Building color mapping.')
    # Get variables from units_mapping excluding the abscissa.
    variables = list(units_mapping.keys())[1:]
    # If color_map is None, use empty map.
    color_map = (color_map and color_map.copy()) or {}
    # If mappings have mismatching list of variable.
    if set(variables) ^ set(color_map.keys()) != set():
        logger.info('Sorting incompatible mappings. ' + \
                     'Additional plots will be black without unit.')
        # If color map is missing a variable, set it to black.
        color_map.update({var: 'black' for var in variables \
                          if var not in color_map})
        # If units map is missing a variable, set it to ''.
        units_mapping.update({var: '' for var in color_map \
                              if var not in units_mapping})

    logger.info(f'{color_map = }')
    return color_map

def get_fig_size(number_of_graphs: int) -> tuple:
    '''
       Get figure size ajusted to number of plots given a max height.

       Returns number of plots horizontally and vertically, and figure size.
    '''
    
    # Adjust fig size for number of plots given a max height.
    w,h = conf._GRID_ASPECT_

    # Adjust fig size for number of plots given a max height.
    W,H = divmod(number_of_graphs,conf._MAX_H_)
    W, H = (1, number_of_graphs) if W == 0 else (W+(H!=0), conf._MAX_H_) 
    return (W, H, w*W, h*H)

def make_graph(df: pd.DataFrame,
               units_mapping: protocols.DATA_TYPE,
               min_map: protocols.DATA_TYPE = {},
               max_map: protocols.DATA_TYPE = {},
               color_map: Optional[protocols.DATA_TYPE] = None,
               title: str = conf._DEFAULT_GRAPH_TITLE_,
               plot_params = conf._DEFAULT_PLOT_PARAMS_,
               axis_fontsize: float = 23.,
               title_params: protocols.DATA_TYPE = conf._DEFAULT_TITLE_PARAMS_,
               legend_fontsize: float = 20.,
               xticks_width: int = conf._XTICKS_WIDTH_,
               filename: Optional[str] = None) -> str:
    '''
       Makes graph from dataframe with each variable in a cell on a grid.

       Uses a units, color, min and max maps to set graphs limits, color and
       displayed units. Creates xticks from xticks width value.
    '''

    # Build xticks with specific width.
    num_ticks = int(np.ceil(df[df.columns[0]].max()/xticks_width))
    xticks = np.linspace(0,
                        num_ticks*xticks_width,
                        num=num_ticks+1,
                        dtype=np.int8)

    # Build color_map if not provided.
    color_map = _build_color_map(units_mapping, color_map)
    # Guarantee that color_map does not have the abscissa as a key.
    color_map.pop(df.columns[0], None)
    # Get list of variables to plot.
    plot_list = list(color_map.keys())

    # Dropped plots to fit in image.
    if len(plot_list) > conf._MAX_VARS_:
        plot_list = plot_list[:conf._MAX_VARS_]
        logger.info("Dropped plots to fit in image.")
    # Get number of graphs and figure size.
    num_graphs = len(plot_list)
    W, H, *plot_params['figsize'] = get_fig_size(num_graphs)
    
    fig = plt.figure()
    # Set title
    fig.suptitle(title, **title_params)
    # Set layout
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)


    for var in plot_list:
        i = plot_list.index(var)+1
        # Create subplot
        ax = plt.subplot(H*100+W*10+i)
        # Show progress in terminal.
        print(
            'Building image [' + \
            i*'=' + (num_graphs-i)*' ' + \
            f']({i}/{num_graphs})', end='\r')
        
        # Plot graphs with column 0 as abscissa and var as ordinate.
        df.plot(kind=conf._GRAPH_KIND_, x=df.columns[0], y=var,
                ax=ax, **plot_params, color=color_map[var], xticks=xticks)
        # Set x and y labels, title, y limits and legend for the graph.
        ax.set_ylabel(
            units_mapping[var],
            fontsize=axis_fontsize)
        ax.set_xlabel(
            f'Time ({units_mapping[df.columns[0]]})',
            fontsize=axis_fontsize)
        ax.set_ylim(bottom=min_map.get(var, None), top=max_map.get(var, None))
        ax.legend(fontsize=legend_fontsize)
    
    # Show progress in terminal.
    print('Building graphs [' + \
            num_graphs*'=' + \
            f']({num_graphs}/{num_graphs})')

    # Add to filename the title and variables.
    # If variables names make filename too long, use number of variables.
    if len('_'.join(plot_list))>conf._MAX_FILENAME_VAR_SIZE_:
        plot_list = [f'{len(plot_list)}_variables']
    # Build filename from current datetime, title and variables.
    filename = (filename or os_ops.get_time()) + \
                '_'.join([title] + plot_list) + '.png'
    # Save image in images directory and close plot to free resources.
    plt.savefig(conf.__IMG_DIR__ + filename, dpi=conf._DPI_, bbox_inches='tight')
    logger.info(f'Graphs image saved as {filename}')
    plt.close()

    return filename


if __name__ == '__main__':
    from src import DASGIP_loader
    
    header_mapping = {
        'GARBAGE_TEXT.Time [s]':'Time',
        'GARBAGE_TEXT.DO1 [mg/L]':'DO1',
        'GARBAGE_TEXT.DO2 [mg/L]':'DO2',
        'GARBAGE_TEXT.DO3 [mg/L]':'DO3',
        'GARBAGE_TEXT.DO4 [mg/L]':'DO4',
        'GARBAGE_TEXT.DO5 [mg/L]':'DO5',
        'GARBAGE_TEXT.DO6 [mg/L]':'DO6',
        'GARBAGE_TEXT.DO7 [mg/L]':'DO7'
    }
    print(DASGIP_loader.get_units(header_mapping))
    
    color_map = {head:color for head,color in \
                 zip(header_mapping.values(), ['mediumseagreen','aquamarine'] + ['black']*6)}
    time = np.arange(0,60,1)

    img_name = make_graph(
        pd.DataFrame(
            np.array([time]+[50*(np.sin(time)+1)]*(len(color_map)-1)).T,
            columns=header_mapping.values()),
            DASGIP_loader.get_units(header_mapping),
            color_map=color_map,
            filename=_TEST_FILENAME_
            )
    
    print(img_name)