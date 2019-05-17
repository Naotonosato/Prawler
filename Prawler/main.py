import os
import sys
sys.path.append(os.pardir)
from uix.propertyview import PropertyView, PropertyForm
from uix.multi_language_textinput import MultiLanguageTextInput
from manager.dragmanager import DragManager
from manager.relationmanager import RelationManager
from model.generator import Generator
from model.field import Field
from kivy.uix.dropdown import DropDown
from kivy.factory import Factory
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.modules import keybinding

Factory.register('MultiLanguageTextInput', MultiLanguageTextInput)
Factory.register('PropertyView', PropertyView)
Factory.register('PropertyForm', PropertyForm)

Window.clearcolor = (.4, .4, .4, .8)
#Config.write()
#app name candidates:
'''
+ KivyLadder/ /RAD --> RADer --> Ladder
+ MilletRadical/ /kivy --> kibi --> millet,RAD --> rad --> radical
+ Prawler/ /RAD-RADer --> Ladder-HASHIGO --> "p"ub "crawl"ing --> Prawler
'''


class Prawler(App):

    def __init__(self, **kwargs):

        super(Prawler, self).__init__(**kwargs)

        self.toolbox = None
        self.field = Field()
        self.generator = Generator(field=self.field)
        self.relation_manager = RelationManager(field=self.field)
        self.drag_manager = DragManager(field=self.field)


class Test1(App):

    pass


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            Test1().run()
    else:
        Prawler().run()
