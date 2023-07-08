import logging
import logging.handlers

logging.getLogger('').setLevel(logging.NOTSET)
rotatingHandler = logging.handlers.RotatingFileHandler(
    filename='.LOG.log', maxBytes=10_000, backupCount=5)
rotatingHandler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotatingHandler.setFormatter(formatter)
logging.getLogger('').addHandler(rotatingHandler)

_FILE_ = "./CSV/CTPCLI308268.Manager 584248e0.Control.csv"
_TOKEN_ = '"[TrackData{}]"\n'
_END_TOKEN_ = '\n\n'

__DB_FILE__ = "./DB/prog_data.json"
__IMG_DIR__ = "./IMG/"

_TIME_FORMAT_ = '%Y-%m-%d'
_TIME_KEEP_DATA_ = 2 # days
_TIME_KEEP_IMAG_ = 0 # days