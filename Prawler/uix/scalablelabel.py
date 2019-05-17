from kivy.properties import DictProperty,ObjectProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import FocusBehavior

class ScalableLabel(Label):
    
    def __init__(self, **kwargs):

        super(ScalableLabel, self).__init__(**kwargs)
        self.fbind(
            'size',
            lambda _,size: setattr(self,'text_size',[size[0],None])
            )
        self.fbind(
            'texture_size',
            lambda _,size: setattr(self,'height',size[1])
            )     
    