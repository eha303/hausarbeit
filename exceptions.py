class InvalidDataFileError(Exception):
    """
    This Exception should be raised when a data file does not contain
    the data expected.
    """

    def __init__(self):
        self.error_message = 'The specified data file was not found or does not contain valid data.'


class InvalidFunctionDataError(Exception):
    """
    This Exception should be raised when a simple list of coordinates is expected
    but it is not a simple list of coordinates
    """
    def __init__(self):
        self.error_message = 'Invalid Function Data. This does not seem to be an expected list of Y-Coordinates.'


class InvalidDataFrameError(Exception):
    """
    This Exception should be raised when a DataFrame is expected
    but it is not a DataFrame
    """
    def __init__(self):
        self.error_message = 'Invalid DataFrame. This does not seem to be a dataframe.'
