import ast
import traceback
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeViewNode
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    AliasProperty,BooleanProperty,ListProperty,ReferenceListProperty,ObjectProperty,StringProperty,NumericProperty
    )
from .scalablelabel import ScalableLabel
from .scalablebutton import ScalableButton
import utils


class PropertyForm_(BoxLayout):
    
    _data = ListProperty([])
    _index = NumericProperty(0)
    default = ObjectProperty(None,allownone=True)
    property_object = ObjectProperty(None)
    text = StringProperty('')
    widget = ObjectProperty(None)
    name_label = ObjectProperty(None)
    value_label = ObjectProperty(None)
    
    def __init__(self,**kwargs):

        super(PropertyForm,self).__init__(**kwargs)
        self.name_label = ScalableLabel()
        self.value_label = ScalableLabel()
        self.add_widget(self.name_label)
        self.add_widget(self.value_label)

    def on_property_object(self,_,prop):

        if prop is not None:
            utils.do_later(self._on_property_object,_,prop,dt=1)

    def _on_property_object(self,_,prop):

        if self.widget is None:
            return
        self.name_label.text = prop.name + ': '
        self.value_label.text = str(prop.get(self.widget))
        

class PropertyView_(RecycleView):
    
    '''Properties View.
    '''
    target_widget = ObjectProperty(None,allownone=True)

    def __init__(self,**kwargs):

        super(PropertyView,self).__init__(**kwargs)
        app = App.get_running_app()
        app.drag_manager.bind(
            selected_widget=lambda _,w:setattr(
                self,'target_widget',w.owned_widget if w is not None else None)
            )

    def on_target_widget(self,_,widget):

        if widget is None:
            return
        properties = widget.properties()
        
        for name in properties:
            prop = properties[name]
            
            self.data.append(
                {
                'default':prop.get(widget),
                'property_object':prop,
                'widget':widget,
                })
        

class PropertyForm(BoxLayout):

    default = ObjectProperty(None,allownone=True)
    property_object = ObjectProperty(None)
    name_view = ObjectProperty(None)
    value_view = ObjectProperty(None)
    textinput = ObjectProperty(None)
    widget = ObjectProperty(None)
    
    def __init__(self,**kwargs):

        super(PropertyForm,self).__init__(**kwargs)
        self._disabled_on_text = False
        self.field = App.get_running_app().field
        self.size_hint_y = None
        self.name_view = ScalableLabel()
        self.value_view = ScalableButton()
        self.value_view.fbind('on_press',self._on_press)
        self.textinput = TextInput()
        self.textinput.fbind('text',self._on_text)
        self.textinput.fbind('focus',self._on_focus)
        self.add_widget(self.name_view)
        self.add_widget(self.value_view)

    def _on_press(self,_):

        self.remove_widget(self.value_view)
        self.add_widget(self.textinput)
        self.field.add_property(self.widget,self.property_object.name)

    def on_property_object(self,_,prop):

        if prop is None:
            return
        prop_name = self.property_object.name
        self.name_view.text = prop_name
        self.value_view.text = str(prop.get(self.widget.owned_widget))
        self.widget.owned_widget.fbind(
            prop_name,lambda _,value: setattr(self.value_view,'text',str(value))
            )

    def _on_text(self,_,text):

        if text != str(self.default):
            result = self.exec(text)
            if result[1] == 'success':
                try:
                    self.field.add_property(self.widget,self.property_object.name)
                    setattr(
                        self.widget.owned_widget,
                        self.property_object.name,
                        result[0]
                        )
                    self.widget.attach_texture()
                except:
                    pass
            else:
                pass
            utils.do_later(self.widget.attach_texture,dt=1)
    
    def _on_focus(self,_,focus):

        if not focus:
            self.remove_widget(self.textinput)
            self.add_widget(self.value_view)

    def exec(self,text):

        try:
            return eval(text,{},{}),'success'
        except:    
            #traceback.print_exc()
            return None,'failed'
        


class PropertyView(BoxLayout):

    target_widget = ObjectProperty(None,allownone=True)

    def __init__(self,**kwargs):

        super(PropertyView,self).__init__(**kwargs)
        app = App.get_running_app()
        app.drag_manager.bind(
                selected_widget=self.setter('target_widget')
                )

    def on_target_widget(self,_,widget):

        self.clear_widgets()
        if widget is None:
            return
        properties = widget.owned_widget.properties()
        for prop_name,prop_obj in properties.items():
            prop_form = PropertyForm()
            prop_form.widget = widget
            prop_form.default = prop_obj.get(widget.owned_widget)
            prop_form.property_object = prop_obj
            self.add_widget(prop_form)