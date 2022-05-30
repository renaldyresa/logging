class TypeLogError(Exception):

    def __init__(self):
        super().__init__("Type Log Invalid")


class LocalLogDirectoryError(Exception):

    def __init__(self):
        super().__init__("Type Log Local, must be have app name. (os['APP_NAME'])")
