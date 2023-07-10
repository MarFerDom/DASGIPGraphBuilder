import logging
import logging.handlers

    # LOGGER

logger = logging.getLogger('')
logger.setLevel(logging.NOTSET)

# Add rotating file handler
rotatingHandler = logging.handlers.RotatingFileHandler(
    filename='.LOG.log', maxBytes=10_000, backupCount=5)
rotatingHandler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotatingHandler.setFormatter(formatter)
logger.addHandler(rotatingHandler)

    # FILE LOADING

# Example file used in prototyping
_FILE_ = "./CSV/CTPCLI308268.Manager 584248e0.Control.csv"
# Token for separating data blocks
_TOKEN_ = '"[TrackData{}]"\n'
_END_TOKEN_ = '\n\n'
# Reads Inoculation and .PV headers from a data block.
_HEADER_TAGS_ = ('Inoculation', '.PV')

    # API

API_PORT = 5000
API_URL = f"http://127.0.0.1:{API_PORT}/"
API_CONFIG = "config"
API_UPLOAD = "upload"
API_LIST_FILES = "file"
API_IMGS = "img"
API_GRAPH = "graph_maker"

    # DATABASE

# Database file
__DB_DIR__ = "./DB/"
__DB_FILE__ = __DB_DIR__+"prog_data.json"
# Images directory
__IMG_DIR__ = "./IMG/"

_TIME_FORMAT_ = '%Y-%m-%d'
_TIME_KEEP_DATA_ = 2 # days to keep data
_TIME_KEEP_IMAG_ = 1 # days to keep images
_ERROR_DB_ = "Database error: "
_ERROR_IMG_ = "Image error: Invalid file type"


_ERROR_HEADER_ = "Error: "
_ERROR_FILE_ = "File not found"
_ERROR_NO_TOKEN_ = "No token found in content"
_ERROR_LOAD_HEADER_ = "Error loading headers"
_ERROR_FORMAT_ = "Format error"


    # GRAPH

_PLOT_STYLE_ = 'ggplot'
_XTICKS_WIDTH_ = 6 # hours

# Max number of subplots stacked vertically per plot
_MAX_H_ = 3
# Max number of variables per image.
_MAX_VARS_ = 2*_MAX_H_
# Max size of filename devoted to variables in saving images.
_MAX_FILENAME_VAR_SIZE_ = 42

_DEFAULT_GRAPH_TITLE_ = "Title"
_DEFAULT_TITLE_PARAMS_ = {'fontsize':23, 'fontweight':'bold',
                         'style':'italic', 'family':'monospace'}
_DEFAULT_PLOT_PARAMS_ = {'grid':True, 'fontsize':20.,
                         'legend':True, 'linewidth':5.5}
_GRAPH_KIND_ = 'line'
# Subplot size.
_GRID_ASPECT_ = (18,5)
# DPI for saving images.
_DPI_ = 300