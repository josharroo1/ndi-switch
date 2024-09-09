import configparser

def update_config_file():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'Settings' not in config:
        config['Settings'] = {'last_decoder': '0'}
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        self.config.read(self.config_file)

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        if section not in self.config:
            self.config.add_section(section)
        self.config[section][key] = str(value)

    def get_decoders(self):
        decoders = []
        for section in self.config.sections():
            if section.startswith('NDIDecoder'):
                decoder = {
                    'ip': self.config[section].get('ip', ''),
                    'username': self.config[section].get('username', ''),
                    'password': self.config[section].get('password', ''),
                    'name': self.config[section].get('name', f"Decoder {len(decoders) + 1}")
                }
                decoders.append(decoder)
        return decoders

    def update_decoders(self, decoders):
        for i, decoder in enumerate(decoders, 1):
            section = f'NDIDecoder{i}'
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config[section]['ip'] = decoder['ip']
            self.config[section]['username'] = decoder['username']
            self.config[section]['password'] = decoder['password']
            self.config[section]['name'] = decoder['name']
        
        # Remove any excess decoder sections
        sections_to_remove = []
        for section in self.config.sections():
            if section.startswith('NDIDecoder'):
                try:
                    decoder_number = int(section[10:])
                    if decoder_number > len(decoders):
                        sections_to_remove.append(section)
                except ValueError:
                    sections_to_remove.append(section)
        
        for section in sections_to_remove:
            self.config.remove_section(section)
        
        self.save_config()

    def get_sources(self):
        return [value for key, value in self.config['NDI_Sources'].items() if key.startswith('source')]

    def get_user_friendly_names(self):
        return [value for key, value in self.config['User_Friendly_Names'].items() if key.startswith('source')]

    def update_sources(self, sources):
        self.config['NDI_Sources'] = {f'source{i+1}': source for i, source in enumerate(sources)}
        self.save_config()

    def update_user_friendly_names(self, names):
        self.config['User_Friendly_Names'] = {f'source{i+1}': name for i, name in enumerate(names)}
        self.save_config()