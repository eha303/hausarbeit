class InvalidDataFileError(Exception):
    def __init__(self):
        self.error_message = 'The specified data file was not found or does not contain valid data.'

class InvalidFunctionDataError(Exception):
    def __init__(self):
        self.error_message = 'Invalid Function Data. This does not seem to be an expected list of Y-Coordinates.'

class InvalidDataFrameError(Exception):
    def __init__(self):
        self.error_message = 'Invalid DataFrame. This does not seem to be a dataframe.'