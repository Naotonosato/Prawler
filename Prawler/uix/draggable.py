import traceback
from kivy.app import App
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.graphics import (
    Rectangle,Color,texture,Fbo,ClearColor,ClearBuffers,
    Scale,Translate,Rotate,PushMatrix,PopMatrix
    )
from kivy.uix.image import Image
from kivy.uix.splitter import Splitter
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.animation import Animation
from kivy.properties import StringProperty,ListProperty,DictProperty,ObjectProperty,NumericProperty,BooleanProperty
from uix.errorwidget import ErrorWidget
from classes import classes
import utils


class Draggable(DragBehavior):

    '''
    Item of toolbox must inherit this class.
    '''

    _old_pos = ListProperty([])
    owned_widget = ObjectProperty(None)
    '''
    owned_widget is instance of owned_class.
    this instance is generated by function
    'on_owned_class' dynamically.
    '''

    owned_class = DictProperty({})
    '''
    owned_class is class of widget that
    should be owned by item of toolbox.
    this dictionaly has keys 'class'
    and 'kwargs'.
    Key 'kwargs' is a key of dictionaly of
    owned_class's args.
    '''

    owned_widget_texture = ObjectProperty(None)
    '''
    owned_widet_texture is texture of
    owned_widget.
    item of toolbox displays this texture.
    this texture is got by function
    '_get_fbo'.
    '''

    def __init__(self,**kwargs):
        '''initialize.
        
        when function '__init__' called by it,
        App.get_running_app().root is None.
        so we have to use App.root widget later.
        by calling function '_initialize'
        '''
        super(Draggable,self).__init__(**kwargs)
        self.cancel = False
        self.updated = False
        self.drag_distance = 0
        app = App.get_running_app()
        self.toolbox = app.toolbox
        self.drag_manager = app.drag_manager
        self.field = app.field
        utils.do_later(self._initialize)

    def _initialize(self):
        '''initialize later.
        '''
        app = App.get_running_app()
        self.drag_rectangle = (0,0,app.root.width,app.root.height)
        app.root.bind(size=lambda _,size: setattr(self,'drag_rectangle',(0,0,*size)))
        self._index = self.parent.children.index(self)
        self._old_pos = self.pos
        self.updating = Clock.schedule_interval(self._update,1/60)
        
    def _update(self,dt):
        '''update.
        if self is out of toolbox,
        remove self from toolbox.

        Args: 
            dt (float): interval of clock event.
        '''
        if (not self.updated) and self.y + self.height < self._old_pos[1]:
            
            utils.do_later(self.toolbox.update_toolbox,self,self._index)
            self.updated = True
            self.updating.cancel()

    def get_texture(self,widget):
        '''
        get texture.

        Args:
            widget: subclass of kivy.uix.widget.

        Returns:
            kivy.graphics.texture.Texture: texture of widget.
        '''
        fbo = self._get_fbo(widget)
        
        fbo.add(widget.canvas)
        fbo.draw()
        texture = fbo.texture
        fbo.remove(widget.canvas)

        with fbo:
            PopMatrix()

        return texture

    def _get_fbo(self,widget):
        '''get frame buffer object of widget.
        Args:
            widget: subclass of kivy.uix.widget.
        Returns:
            kivy.graphics.fbo
        '''
        if widget.parent is not None:
            canvas_parent_index = widget.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                widget.parent.canvas.remove(widget.canvas)

        fbo = Fbo(size=widget.size, with_stencilbuffer=True)

        with fbo:
            PushMatrix()
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-widget.x, -widget.y - widget.height, 0)
            Rotate(origin=widget.center,
                axis=(widget.center_x,0,0),
                angle=-180)

        return fbo

    def attach_texture(self):
        '''attach texture.

        attaches texture of widget that
        owned by self.
        '''
        texture = self.get_texture(self.owned_widget)
        texture_size = texture.size

        if isinstance(self.owned_widget,Image):
            texture_size = self.owned_widget.get_norm_image_size()
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            self.owned_widget_texture = Rectangle(
                pos = self.pos,
                size = texture_size,
                texture = texture
                )
        
        self.owned_widget.bind(
            pos = lambda _,pos: setattr(self.owned_widget_texture,'pos',pos),
            size = lambda _,size: setattr(self.owned_widget_texture,'size',size)
            )
        
    def append_widget(self):
        '''append self to Field object.
        '''
        if not self.field.is_appended(self) and self.updated:
            self.field.append(
                self,'size','size_hint','pos','pos_hint'
                )
            self.owned_widget.size_hint = (None,None)      

    def on_owned_widget(self,_,widget):
        '''bind size and pos.
        '''
        self.bind(size=widget.setter('size'))
        self.bind(pos=widget.setter('pos'))
        widget.bind(size=self.setter('size'))
        widget.bind(pos=self.setter('pos'))

    def on_owned_class(self,_,dict_):
        '''generate widget.

        generate widget dynamically.

        Args:
            dict_ (dict):dictionaly of class and args of the class.
        
        Raises:
            Any exception: if failed to generate.
        '''
        try:
            class_ = dict_['class']
            kwargs = dict_.get('kwargs')
            if type(class_) == str:
                class_ = classes[class_]
            if kwargs:
                self.owned_widget = class_(**kwargs)
            else:
                self.owned_widget = class_()
        except:
            traceback.print_exc()
            self.owned_widget = ErrorWidget()

    def on_touch_move(self,touch):
        '''set self._old_pos.
        '''
        if not self.cancel:
            self._old_pos = self.pos
        self.cancel = True
        return super(Draggable,self).on_touch_move(touch)
                
    def on_touch_down(self,touch):
        '''callback that called when touch down.
        '''
        if self.collide_point(*touch.pos):
            if hasattr(touch,'button') and touch.button == 'right':
                pass
        return super(Draggable,self).on_touch_down(touch)

    def on_touch_up(self,touch):
        '''callback of touch up.

        append self to Field object.
        arange position in close widget.
        '''
        self.append_widget()
        self.scaling = False

        if self.collide_point(*touch.pos):
            self.drag_manager.guide(self)
            if self.owned_widget_texture is None and self.updated:
                self.text = ''
                utils.do_later(self.attach_texture)
            if not self.updated:
                self.pos = self._old_pos

        return super(Draggable,self).on_touch_up(touch)


Factory.register('Draggable',cls=Draggable)
#Factory.register('DraggableItem',cls=DraggableItem)