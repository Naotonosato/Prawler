from functools import partial
from kivy.clock import Clock
from kivy.uix.widget import Widget
def do_later(func,*args,dt=0):
    '''call function later.
    
    Args:
        func: function that you want tp call later.
        dt(float): interval of calling the function.
    '''
    func = partial(func,*args)

    def dumb(dt=0):
        func()

    Clock.schedule_once(dumb,dt)


def flatten(iteratable):
    '''flatten a nested iteratable object.
    Args:
        iteratable: iteratable object.
    '''
    for i in iteratable:
        if hasattr(i,'__iter__') and not isinstance(i,str):
            for j in flatten(i):
                yield j
        else:
            yield i


def prop_to_dict(widget):

    properties = widget.properties()
    return {prop:properties[prop].get(widget) for prop in properties}


def check_property(widget,prop_obj):
    
    from kivy.properties import ObjectProperty
    value = prop_obj.get(widget)
    if isinstance(prop_obj,ObjectProperty):
        return False
    
    if hasattr(value,'__iter__') and not isinstance(value,str):
        if any((
            True if isinstance(i,Widget) else False 
            for i in flatten(value))):
            return False

    return True


class Subject(object):
    '''Subject class.

    If you want to implemente subject,
    you can inherit this class.

    Attributes:
        observers (list): list of observers.
    '''

    def __init__(self):

        self.observers = []

    def add_observer(self,observer):

        self.observers.append(observer)

    def notify(self):

        raise NotImplementedError


class Singleton(type):
    '''Singleton.

    If you want to implemente singleton,
    you can use this class as a metaclass. 
    '''
    
    __instance = {}

    def __call__(cls,*args,**kwargs):

        if cls.__instance.get(cls) is None:
            cls.__instance[cls] = super(Config,cls).__call__(*args,**kwargs)

        return cls.__instance[cls]