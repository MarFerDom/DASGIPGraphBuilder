import json
from src import conf, os_ops, protocols

logger = conf.logging.getLogger(__name__)

class SimpleJSONDB():
    def __init__(self, filename: str = conf.__DB_FILE__):
        '''
           Simple JSON database.
           
           If file does not exist, create new database.
        '''
        
        self.filename = filename
        # Load data from file.
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
            logger.info('Loaded database from file')
            # Remove expired data and images.
            os_ops.check_imag_del()
            self._check_data_del()
        # Or create new database.
        except:
            self.data = {
                'files': {}, # mapping of filenames to content
                'config': {}, # configuration data
                'f_mng': {} # file management data
            }
            logger.info('Created new database')

    def _check_data_del(self):
        '''
           Checks for data overdue to delete.
        '''
        
        # Get files from database and check for timestamp expiration.
        for filename in self.data.get("files", ()).copy():
            # Remove files that expired.
            if os_ops.time_check(self.data['f_mng'][filename], conf._TIME_KEEP_DATA_):
                logger.info(f'removing {filename}')
                # Remove content.
                self.data['files'].pop(filename, None)
                # Remove timestamp.
                self.data['f_mng'].pop(filename, None)
                

    @property
    def config(self):
        return self.data['config']
    
    @config.setter
    def config(self, new_config: protocols.CONFIG_TYPE):
        self.data['config'] = new_config

    @config.deleter
    def config(self):
        self.data['config'] = {}

    def get_imgs(self, *args, **kwargs) -> list:
        '''
           Get file names from images directory
        '''
        
        return os_ops.get_imgs()
    
    def get_files(self, *args, **kwargs) -> list:
        '''
           Get list of available files to read from
        '''
        
        return list(self.data['files'].keys())
    
    def update_content(self,
                       filename: str,
                       content: protocols.DATA_TYPE = {},
                       *args, **kwargs) -> None:
        '''
           Update content from a file to database.
           
           If content is empty, remove file from database.
        '''

        if content == {}:
            self.data['files'].pop(filename, None)
            self.data['f_mng'].pop(filename, None)
        else:
            self.data['files'][filename] = content
            self.data['f_mng'][filename] = os_ops.get_time()
    
    def get_content(self,
                    filename: str,
                    *args, **kwargs) -> protocols.DATA_TYPE:
        '''
           Get content of a file from database.
           
           If file does not exist, return empty dictionary.
        '''

        return self.data['files'].get(filename, {conf._ERROR_HEADER_, conf._ERROR_FILE_})
    
    def commit(self):
        '''
           Save data changes to file
        '''
        
        with open(self.filename, 'w') as f:
            #write json to text file
            json.dump(self.data, f)


if __name__ == '__main__':
    db = SimpleJSONDB()
    
    if len(db.config): print("\nOpened existing database!")

    print(f'\nStored configuration:\n{db.config}')

    print(f'\nAvailable files:\n{db.get_files()}')
    
    print(f'\nAvailable images:\n{db.get_imgs()}')



# class mockDB():
#     def __init__(self):
#         self.files = {}

#     # get list of available files
#     def get_files(self, *args, **kwargs) -> list:
#         return list(self.files.keys())
    
#     # update file content dictionary [mock method implement - read from database]
#     def update_file(self, filename: str, content: str ='', *args, **kwargs):
#         if content == '':
#             self.files.pop(filename, None)
#         else:
#             self.files[filename] = content
    
#     # get file content [mock method implement - read from database]
#     def get_content(self, filename: str, *args, **kwargs) -> str:
#         return self.files.get(filename, '')
    
#     def get_img(self, *args, **kwargs):
#         return ["test.png"]