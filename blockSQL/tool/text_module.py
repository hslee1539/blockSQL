class Text(str):
    def __init__(self, bytes_or_buffer : str, encoding = None, errors = None):
        str.__init__(self, "'" + bytes_or_buffer + "'", encoding, errors)
