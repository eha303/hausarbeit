class InvalidDataFileError(Exception):
    def __init__(self):
        self.error_message = 'The specified data file was not found or does not contain valid data.'
