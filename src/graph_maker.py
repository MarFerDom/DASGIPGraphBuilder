import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from typing import Dict, Optional
from src import conf


logger = conf.logging.getLogger(__name__)

plt.style.use('ggplot')

_XTICKS_WIDTH_ = 6
_MAX_H_ = 3
_MAX_FILENAME_VAR_SIZE_ = 40
_FILENAME_ = "graph.png"
_GRAPH_TITLE_ = "Title"
_TIME_FORMAT_ = "%Y_%m_%d(%a)-%I_%M%p_"
_DEFAULT_TITLE_PARAMS_ = {'fontsize':23, 'fontweight':'bold',
                         'style':'italic', 'family':'monospace'}
_DEFAULT_PLOT_PARAMS_ = {'grid':True, 'fontsize':20.,
                         'legend':True, 'linewidth':5.5}

def get_units(header_mapping: Dict[str,str]) -> Dict[str,str]:
    '''
       Build mapping from headers to units.
    '''
    
    logger.info('Building units mapping.')
    units_mapping = {}
    for header, new_header in header_mapping.items():
        x = re.search(r"\[(.*?)\]", header).group(1)
        units_mapping[new_header] = 'h' if x == '' else x
    return units_mapping

def _build_color_map(units_mapping: Dict[str,str],
                   color_map: Optional[Dict[str,str]] = None):

    # Get variables from units_mapping excluding the abscissa.
    variables = list(units_mapping.keys())[1:]
    # If color_map is None, then use black for all variables.
    if color_map is None:
        logger.info('Building color mapping.')
        color_map = {var: 'black' for var in variables}
    # If color_map missing a variable, then use black for that variable.
    if set(variables) ^ set(color_map.keys()) != set():
        logger.info('Sorting incompatible mappings' + \
                     'Additional plots will be black without unit.')
        color_map.update({var: 'black' for var in variables if var not in color_map})
        units_mapping.update({var: '' for var in color_map if var not in units_mapping})

    return color_map
    
def make_graph(df: pd.DataFrame, units_mapping: Dict[str,str],
               min_map: Dict[str,str] = {}, max_map: Dict[str,str] = {},
               color_map: Optional[Dict[str,str]] = None,
               title: str = _GRAPH_TITLE_,
               plot_params = _DEFAULT_PLOT_PARAMS_, axis_fontsize: float = 23.,
               legend_fontsize: float = 20., DO_ylim = (-10, 110),
               title_params: Dict[str,str] = _DEFAULT_TITLE_PARAMS_,
               xticks_width: int = _XTICKS_WIDTH_,
               filename: Optional[str] = None) -> str:
    '''
       Makes graph from dataframe.
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

    # Adjust fig size for number of plots.
    w,h = (18,5)
    if len(plot_list) > 2*_MAX_H_:
        plot_list = plot_list[:2*_MAX_H_]
        logger.info("Dropped plots to fit in image.")
    num_graphs = len(plot_list)
    W,H = divmod(num_graphs,_MAX_H_)
    W, H = (1, num_graphs) if W == 0 else (W+(H!=0), _MAX_H_) 
    plot_params['figsize'] = (w*W,h*H)
    dpi = 300

    #fig, axs = plt.subplots(H, W)
    fig = plt.figure()
    #if type(axs) != np.ndarray: axs = np.array([axs])
    #axs = axs.reshape((-1,)).tolist()
    fig.suptitle(title, **title_params)
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    #for ax, var in zip(axs, plot_list):
    for var in plot_list:
        i = plot_list.index(var)+1
        ax = plt.subplot(H*100+W*10+i)
        print(
            'Building image [' + \
            i*'=' + (num_graphs-i)*' ' + \
            f']({i}/{num_graphs})', end='\r')
        
        df.plot(kind='line', x=df.columns[0], y=var,
        ax=ax, **plot_params, color=color_map[var], xticks=xticks)
        ax.set_ylabel(units_mapping[var], fontsize=axis_fontsize)
        ax.set_xlabel(f'Time ({units_mapping[df.columns[0]]})', fontsize=axis_fontsize)
        
        # IMPROVE THIS PLEASE!!
        ax.set_ylim(bottom=min_map.get(var, None), top=max_map.get(var, None))
        #if "DO" in var : ax.set_ylim(*DO_ylim)
        #if "FAir" in var: ax.set_ylim(0,110)
        #if "N" == var: ax.set_ylim(0,1500)
        ax.legend(fontsize=legend_fontsize)
    print('Building graphs [' + num_graphs*'=' + f']({num_graphs}/{num_graphs})')

    if filename is None:
        if len('_'.join(plot_list))>_MAX_FILENAME_VAR_SIZE_: plot_list = [f'{len(plot_list)}_variables']
        filename = datetime.now().strftime(_TIME_FORMAT_) + '_'.join([title]+plot_list) + '.png'
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    logger.info(f'Graphs image saved as {filename}')
    plt.close()

    return filename


if __name__ == '__main__':

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
    print(get_units(header_mapping))
    
    color_map = {head:color for head,color in \
                 zip(header_mapping.values(), ['mediumseagreen','aquamarine'] + ['black']*6)}
    time = np.arange(0,60,1)

    make_graph(pd.DataFrame(np.array([time]+[50*(np.sin(time)+1)]*(len(color_map)-1)).T, columns=header_mapping.values()),
               get_units(header_mapping), color_map=color_map, filename=_FILENAME_)