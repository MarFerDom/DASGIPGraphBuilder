import os
from datetime import datetime
from typing import Union
from src import conf

def std_name(filename: str) -> str:
    '''
       Returns filename without path or file type,
       with limited number of characters.
    '''
    
    return os.path.splitext(os.path.basename(filename))[0][:42]

def get_time() -> str:
     '''
        Get current datetime in right format as string.
     '''
     
     return datetime.today().strftime(conf._TIME_FORMAT_)

def time_check(file_time: Union[str, datetime], max_time: str) -> bool:
    '''
       Check if file time is overdue
    '''

    if type(file_time) == str: datetime.strptime(file_time, conf._TIME_FORMAT_)
    return (datetime.today() - file_time).days >= max_time

def get_imgs() -> list:
    '''
        Get file names from images directory
    '''
    
    return [f for f in os.listdir(conf.__IMG_DIR__) if \
            all([
                os.path.isfile(os.path.join(conf.__IMG_DIR__, f)),
                f.endswith(('.jpg', '.png', '.jpeg', '.gif'))
            ])
        ]

def check_imag_del() -> None:
    '''
        Checks for images overdue to delete.
    '''
    
    # Get files form IMG folder and check for timestamp expiration.
    for filename in get_imgs():
        # Get timestamp from file
        file_time = datetime.fromtimestamp(
            os.stat(os.path.join(conf.__IMG_DIR__, filename)).st_mtime
            )
        # Remove files that expired.
        if time_check(file_time, conf._TIME_KEEP_IMAG_):
            os.remove(os.path.join(conf.__IMG_DIR__, filename))