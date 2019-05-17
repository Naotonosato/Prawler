from collections import OrderedDict
from kivy.event import EventDispatcher
from kivy.properties import DictProperty,ListProperty
import utils


class Field(EventDispatcher):

    widget_list = ListProperty()
    widget_properties = DictProperty({})    

    def __init__(self,**kwargs):

        super(Field,self).__init__(**kwargs)
        self.__observers = []

    def add_observer(self,observer):

        self.__observers.append(observer)

    def on_widget_list(self,_,_list):

        self.notify()
    
    def notify(self):

        for observer in self.__observers:
            observer.update_from_field(self)
    
    def get_widget_list(self):

        return self.widget_list

    def get_widget_properties(self,widget):

        print(self.widget_properties[widget])
        return self.widget_properties[widget]

    def get_latest_widget(self):

        return self.widget_list[-1]

    def add_property(self,widget,*prop_name):

        if self.widget_properties.get(widget) is None:
            self.append(widget,*prop_name)
            return
        for name in prop_name:
            prop = widget.owned_widget.property(name)
            if prop is not None:
                value = prop.get(widget.owned_widget)
                if not utils.check_property(widget.owned_widget, prop):
                    continue
                widget.owned_widget.fbind(name,self.update_property,widget,name)
                self.widget_properties[widget][name] = value

    def delete(self,widget,prop_name):

        for name in prop_name:
            prop = widget.property(name)
            if prop is not None:
                widget.funbind(name)
                self.widget_list.remove(widget)
                del self.widget_properties[widget]
        self.notify()

    def append(self,widget,*prop_name):

        self.widget_properties[widget] = {}
        for name in prop_name:
            prop = widget.owned_widget.property(name)
            if prop is not None:
                value = prop.get(widget.owned_widget)
                if not utils.check_property(widget.owned_widget, prop):
                    continue
                widget.owned_widget.fbind(name,self.update_property,widget,name)
                self.widget_properties[widget][name] = value

        self.widget_list.append(widget)

    def update_property(self,item,name,_,value):

        self.widget_properties[item][name] = value
        
    def remove(self,widget):

        self.widget_list.remove(widget)
        del self.widget_properties[widget]

    def is_appended(self,widget):

        return widget in self.widget_list