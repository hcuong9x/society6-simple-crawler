import configparser


class Config:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_config(self, section, option):
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.file_path)
        
        value = ''
        if config.has_section(section):
            value = config.get(section, option)
            
        return value
