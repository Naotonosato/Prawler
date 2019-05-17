from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import ListProperty,ObjectProperty
import utils

class DragManager(EventDispatcher):

    '''Manager class of items of toolbox.
    '''
    dragging_widget = ObjectProperty(None,allownone=True)
    guide_distance = ListProperty([10,10])
    selected_widget = ObjectProperty(None,allownone=True)

    def __init__(self,field,**kwargs):

        super(DragManager,self).__init__(**kwargs)
        self.field = field

    def select(self,node):

        self.selected_widget = node.widget
    
    def deselect(self,node):
            
        self.selected_widget = None

    def guide(self,dragging_widget):

        close_x,close_y,close_x_widget,close_y_widget = None,None,None,None
        
        for widget in self.field.get_widget_list():
            
            prop = self.field.get_widget_properties(widget)

            if widget == dragging_widget or widget in dragging_widget.children:
                continue
            pos = prop['pos']

            if close_x is None:
                close_x = pos[0]
            if close_y is None:
                close_y = pos[1]
            distance = dragging_widget.x - pos[0],dragging_widget.y - pos[1]
            if abs(distance[0]) < abs(close_x) and close_x is not None:
                close_x = distance[0]
                close_x_widget = widget
            if abs(distance[1]) < abs(close_y) and close_y is not None:
                close_y = distance[1]
                close_y_widget = widget

        if close_x is not None and abs(close_x) < self.guide_distance[0]:
            dragging_widget.x -= close_x
            #close_x_widget.draw_guide('x')
        if close_y is not None and abs(close_y) < self.guide_distance[1]:
            dragging_widget.y -= close_y
            #close_y_widget.draw_guide('y')