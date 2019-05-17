import utils


class Config(metaclass=utils.Singleton):

    __initialized = False

    def __init__(self,*args,**kwargs):
        
        if not self.__initialized:
            
            pass