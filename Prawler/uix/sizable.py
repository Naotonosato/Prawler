from kivy.properties import NumericProperty,ListProperty,ReferenceListProperty
from kivy.factory import Factory
import utils


class Sizable(object):

    disable_size_hint_x = NumericProperty(.8,allownone=True)
    disable_size_hint_y = NumericProperty(.8,allownone=True)
    disable_size_hint = ListProperty(
        [disable_size_hint_x,disable_size_hint_y]
        )
    disable_width = NumericProperty(0)
    disable_height = NumericProperty(0)
    disable_size = ListProperty(
        [disable_width,disable_height]
        )
    disable_pos_x = NumericProperty(None,allownone=True)
    disable_pos_y = NumericProperty(None,allownone=True)
    disable_pos = ListProperty(
        [disable_pos_x,disable_pos_y]
        )
    
    def on_disable_size_hint(self,_,hint):

        if hint[0] is not None:
            self.disable_width = self.width * hint[0]
        if hint[1] is not None:
            self.disable_height = self.height * hint[1]

    def on_disable_pos(self,_,pos):

        if pos[0] is None:
            self.disable_pos_x = self.x + (self.width - self.disable_width) / 2
        if pos[1] is None:
            self.disable_pos_y = self.y + (self.height - self.disable_height) / 2

    def on_touch_move(self,touch):

        x,y = touch.pos
        direction = 'd'
        dx,dy = touch.dx,touch.dy
        if self.collide_point(x,y):
            if x <= self.disable_pos_x:
                direction = to_left
            elif x >= self.disable_width + self.disable_pos_x:
                direction = 'to_right'
            elif y <= self.disable_pos_y:
                direction = 'to_bottom'
            elif y >= self.disable_height + self.disable_pos_y:
                direction = 'to_top'
        print(direction)
        return super(Sizable,self).on_touch_move(touch)

        
Factory.register('Sizable',Sizable)