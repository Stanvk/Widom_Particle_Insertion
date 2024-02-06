import json
import os
from datetime import datetime

class Container:
    """
    Container class to save and load configurations quickly.
    """

    def __init__(self, basepath, relative_output_path):
        """
        Initiate a new Container object.

        @params: basepath (string)
        @returns: (self)
        """
        self._container = {}
        self.basepath = basepath
        self.output_path = self.basepath + relative_output_path
        
        self.generate_timestamp()

        if not os.path.exists(self.output_path):
            # raise FileNotFoundError("Directory not found! Please make sure that the directory exists before running the script.")
            os.mkdir(self.output_path)

    def generate_timestamp(self):
        """
        Generate a timestamp.

        @params:
        @return: (self)
        """
        self.set('timestamp', datetime.now().strftime("%d_%m_%Y_%H%M%S"))

        return self

    def get_timestamp(self):
        """
        Returns generate timestamp.

        @params:
        @returns timestamp (str)
        """
        return self.get('timestamp')

    def set_array(self, array: dict):
        """
        Add an array of key, value pairs in the container.

        @params: array (dict)
        #returns: (self)
        """
        for k,v in array.items():
            self.set(k,v)

        return self

    def set(self, key, value):
        """
        Set a key and corresponding value in the container.

        @params: key (mixed), value (mixed)
        @returns: (self)
        """
        self._container[key] = value

        return self

    def get(self, key):
        """
        Get a value from the container corresponding to its identifier key.

        @params: key (mixed)
        @returns: value (mixed)
        @raises: ValueError
        """
        if key not in self._container:
            raise KeyError("Key does not exist in container!")

        return self._container[key]

    def save(self, path = None, extension='txt', filename=None):
        """
        Saves complete container to a json file.

        @params: path (mixed)
        @returns: (self)
        """
        if path is None:
            path = self.output_path

        if filename is None:
            filename = 'config_'+self.get_timestamp()
        
        with open(path+filename+'.'+extension, 'w') as file:
            file.write(json.dumps(self._container)) # use `json.loads` to do the reverse

        return self

    def load(self, path = None, extension='txt', filename='config'):
        """
        Load new container into current instance.

        @params: path (mixed)
        @returns: (self)
        """
        if path is None:
            path = self.output_path

        with open(path+filename + '.' + extension, 'r') as file:
            self._container = json.load(file)

        return self