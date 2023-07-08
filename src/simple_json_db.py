import json
import os
from datetime import datetime
from typing import Any, Dict
from src import conf

logger = conf.logging.getLogger(__name__)

def time_check(file_time: datetime, max_time: str):
    '''
       Check if file time is overdue
    '''

    return (datetime.today() - file_time).days >= max_time

class SimpleJSONDB():
    def __init__(self, filename: str = conf.__DB_FILE__):
        self.filename = filename
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
            logger.info('Loaded database from file')
            self._check_imag_del()
            self._check_data_del()
        else:
            self.data = {
                'files': {}, # mapping of filenames to content
                'config': {}, # configuration data
                'f_mng': {} # file management data
            }
            logger.info('Created new database')

    def _check_imag_del(self):
        # Get files form IMG folder and check for timestamp overdue
        for filename in os.listdir(conf.__IMG_DIR__):
            # Get timestamp from file
            file_time = datetime.fromtimestamp(
                os.stat(os.path.join(conf.__IMG_DIR__, filename)).st_mtime
                )
            if time_check(file_time, conf._TIME_KEEP_IMAG_):
                os.remove(os.path.join(conf.__IMG_DIR__, filename))

    def _check_data_del(self):
        for filename in self.data.get("files", ()).copy():
            file_time = datetime.strptime(self.data['f_mng'][filename], conf._TIME_FORMAT_)
            if time_check(file_time, conf._TIME_KEEP_DATA_):
                print(f'removing {filename}')
                self.data['files'].pop(filename, None)
                self.data['f_mng'].pop(filename, None)
                

    @property
    def config(self):
        return self.data['config']
    
    @config.setter
    def config(self, new_config: Dict[str,Any]):
        self.data['config'] = new_config

    @config.deleter
    def config(self):
        self.data['config'] = {}

    
    def get_files(self, *args, **kwargs) -> list:
        '''
           Get list of available files to read from
        '''
        
        return list(self.data['files'].keys())
    
    def update_content(self, filename: str, content: Dict[str, str] ={}, *args, **kwargs):
        '''
           Update content from a file to database.
           
           If content is empty, remove file from database.
        '''

        if content == {}:
            self.data['files'].pop(filename, None)
            self.data['f_mng'].pop(filename, None)
        else:
            self.data['files'][filename] = content
            self.data['f_mng'][filename] = datetime.today().strftime(conf._TIME_FORMAT_)
    
    def get_content(self, filename: str, *args, **kwargs) -> str:
        '''
           Get content of a file from database.
           
           If file does not exist, return empty dictionary.
        '''

        return self.data['files'].get(filename, {})
    
    def get_imgs(self, *args, **kwargs):
        '''
           Get file names from images directory
        '''
        return [f for f in os.listdir(conf.__IMG_DIR__) if \
                all([
                    os.path.isfile(os.path.join(conf.__IMG_DIR__, f)),
                    f.endswith(('.jpg', '.png', '.jpeg', '.gif'))
                ])
            ]
    
    def commit(self):
        '''
           Save data changes to file
        '''
        
        with open(self.filename, 'w') as f:
            #write json to text file
            json.dump(self.data, f)


class mockDB():
    def __init__(self):
        self.files = {}

    # get list of available files
    def get_files(self, *args, **kwargs) -> list:
        return list(self.files.keys())
    
    # update file content dictionary [mock method implement - read from database]
    def update_file(self, filename: str, content: str ='', *args, **kwargs):
        if content == '':
            self.files.pop(filename, None)
        else:
            self.files[filename] = content
    
    # get file content [mock method implement - read from database]
    def get_content(self, filename: str, *args, **kwargs) -> str:
        return self.files.get(filename, '')
    
    def get_img(self, *args, **kwargs):
        return ["test.png"]