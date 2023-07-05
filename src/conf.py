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