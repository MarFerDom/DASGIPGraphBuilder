from src import conf, handler

logger = conf.logging.getLogger(__name__)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description = 'Example use of {}\n'.format(__file__.split("\\")[-1]))
    parser.add_argument('filename',
                        help='File to load from [.csv]\n')
    parser.add_argument('-s', '--SOURCE', type=int, metavar='vessel_number',
                        required=True, help='Numbering of vessel\'s from which to read data from')
    parser.add_argument('-d','--DATA', nargs='+', metavar='variable',
                        help=f'List of variables to build graphs on.\n'+\
                            f'Not selecting variables means choosing all.\n')
    
    args = parser.parse_args()

    if '.csv' not in args.filename:
        parser.error('File not csv')

    handler = handler.Handler(args.filename)
    # Check for correct loading.
    if conf._ERROR_HEADER_ in handler.content:
        parser.error(f'{handler.content[conf._ERROR_HEADER_]}')
    print(f'File {args.filename} loaded\n')

    # Check for valid source selection.
    if args.SOURCE not in range(1,len(handler.sources)+1):
        parser.error(f'Invalid source!\nSelect from options: {handler.sources}')
    print(f'Option {handler.sources[args.SOURCE-1]} chosen\n')

    # Check for valid variables selection.
    data = args.DATA or []
    src_var = handler.get_variables(handler.sources[args.SOURCE-1])
    for d in data:
        if d not in src_var:
            parser.error(f'Invalid variable!\nSelect from options: {src_var}')
    
    # Print selected variables.
    if data == []:
        print('All variables selected for graphing\n')
    else:
        print(f'Selected {", ".join(data)} variables to graph\n')

    # Filtered selected variables.
    mapping = handler.filter_cols(handler.sources[args.SOURCE-1], data)
    # Make graph and return image filename.
    print(f'Graph generated as {handler.make_graph(handler.sources[args.SOURCE-1], mapping)}')