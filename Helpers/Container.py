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

        Params
        basepath [string] - The path to save the configuration.

        Returns
        self [Container] - Return current instance
        """
        self._container = {}
        self.basepath = basepath
        self.output_path = self.basepath + relative_output_path
        
        self.generate_timestamp()

        if not os.path.exists(self.output_path):
            # raise FileNotFoundError("Directory not found! Please make sure that the directory exists before running the script.")
            os.mkdir(self.output_path)

    def generate_timestamp(self):

        self._timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")

        return self

    def get_timestamp(self):

        return self._timestamp

    def set_array(self, array: dict):
        """
        Add an array of key, value pairs in the container.

        Params
        array [dict] - Dictionary of key value pairs to set in container.

        Returns
        self [Container] - Return current instance
        """
        for k,v in array.items():
            self.set(k,v)

        return self

    def set(self, key, value):
        """
        Set a key and corresponding value in the container.

        Params
        key [mixed] - Identifier for container value
        value [mixed] - Value corresponding to key

        Returns
        self [Container] - Return current instance.
        """
        self._container[key] = value

        return self

    def get(self, key):
        """
        Get a value from the container corresponding to its identifier key.

        Params
        key [mixed] - Identifier for container value.

        Returns
        value [mixed] - Value found in the container

        Raises
        ValueError - if key does not exist.
        """
        if key not in self._container:
            raise KeyError("Key does not exist in container!")

        return self._container[key]

    def save(self, path = None, extension='txt', filename='config'):
        """
        Saves complete container to a json file.

        Params
        path [string/None] - Path to save config file to.

        Returns
        self [Container] - Returns current instance.
        """
        if path is None:
            path = self.output_path
        
        with open(path+filename+'.'+extension, 'w') as file:
            file.write(json.dumps(self._container)) # use `json.loads` to do the reverse

        return self

    def load(self, path = None, *, extension='txt'):
        """
        Load new container into current instance.

        Params
        path [string/None] - Path to load json from

        Returns
        self [Container] - Returns current instance with freshly loaded data.
        """
        if path is None:
            path = self.output_path

        with open(path+'config.' + extension, 'r') as file:
            self._container = json.load(file)

        return self