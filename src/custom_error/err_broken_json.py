class BrokenJsonStructureException(Exception):

    def __init__(self, msg: str):
        self.__msg: str = msg
        super().__init__(self.__msg)