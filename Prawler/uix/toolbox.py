from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.treeview import TreeView,TreeViewNode
from kivy.properties import ListProperty,ObjectProperty
from utils import prop_to_dict

class ToolBox(BoxLayout):

    old_children = ListProperty([])
    sandbox = ObjectProperty(None)
    
    def __init__(self,**kwargs):

        super(ToolBox,self).__init__(**kwargs)
        app = App.get_running_app()
        app.toolbox = self
        self.relation_manager = app.relation_manager
        self.relation_manager.add_observer(self)
        self.generator = app.generator

    def on_children(self,_,children):

        if len(children) > len(self.old_children):
            new_widget = tuple(set(children) - set(self.old_children))[0]

        self.old_children = children

    def update_from_relation(self,relation):

        relation = relation.get_relation()
        root = relation[0]
        self.generator.set_relation(relation,root)

    def update_toolbox(self,widget_instance,index):

        widget_class = type(widget_instance)
        self.remove_widget(widget_instance)
        self.sandbox.add_widget(widget_instance)

        self.add_widget(widget_class(
            size_hint_x=None,
            size_hint_y=None,
            size=widget_instance.size,
            pos=widget_instance._old_pos,
            text=widget_instance.text,
            owned_class=widget_instance.owned_class
            ),index)

    def change_relation(self,widget):
        
        pass
