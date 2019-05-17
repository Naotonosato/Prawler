from kivy.app import App
from kivy.event import EventDispatcher
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.treeview import TreeView,TreeViewNode,TreeViewLabel
from kivy.properties import ObjectProperty,BooleanProperty
import utils


class DraggableNode(TreeViewLabel):

    '''Draggable Node.
    '''
    
    relation_manager = ObjectProperty(None)
    drag_manager = ObjectProperty(None)

    def __init__(self,**kwargs):
        '''initialize.
        
        when function '__init__' called by it,
        App.get_running_app().root is None.
        so we have to use App.root widget later.
        by calling function '_initialize'
        '''
        super(DraggableNode,self).__init__(**kwargs)
        utils.do_later(self._initialize,dt=-1)

    def _initialize(self):

        app = App.get_running_app()
        self.drag_rectangle = (0,0,app.root.width,app.root.height)
        self.drag_manager = app.drag_manager

    def on_touch_move(self,touch):

        if self.collide_point(*touch.pos):
            self.relation_manager.register_dragging_widget(self)
            
        return super(DraggableNode,self).on_touch_move(touch)

    def on_touch_up(self,touch):

        if not self.collide_point(*touch.pos):
            self.relation_manager.release(touch)
        
        return super(DraggableNode,self).on_touch_up(touch)


class RelationTreeView(TreeView):
    
    '''TreeView that displays relation of widgets.
    '''
    relation_manager = ObjectProperty(None)

    def __init__(self,**kwargs):

        super(RelationTreeView,self).__init__(**kwargs)
        app = App.get_running_app()
        app.relation_manager.treeview = self
        self.relation_manager = app.relation_manager

    def notify(self,dt):

        if self.relation_manager is not None:            
            self.relation_manager.notify()

    def add_node(self,node,parent=None):

        utils.do_later(self.notify,-1)
        return super(RelationTreeView,self).add_node(node,parent)

    def remove_node(self,node):

        if self.relation_manager:
            self.relation_manager.notify()

        return super(RelationTreeView,self).remove_node(node)
        

class RelationNode(DraggableNode):

    '''Node of RelationTreeView.

    Node of RelationTreeView must inherit
    this class.
    '''
    widget = ObjectProperty(None)
    is_drawed = BooleanProperty(False)

    def on_widget(self,_,widget):

        self.text = widget.owned_widget.__class__.__name__

    def on_touch_up(self,touch):

        if not self.is_drawed:
            self.drag_manager.select(self)
            self.is_drawed = True
        else:
            self.drag_manager.deselect(self)
            self.is_drawed = False

        super(RelationNode,self).on_touch_up(touch)

        
Factory.register('RelationTreeView',RelationTreeView)


if __name__ == '__main__':
    from kivy.uix.boxlayout import BoxLayout
    

    class TestApp(App):

        def build(self):
            box = BoxLayout()
            tree = DroppableTreeView()
            tree.add_node(DraggableNode(text='node1',relation_manager=tree.relation_manager))
            tree.add_node(DraggableNode(text='node2',relation_manager=tree.relation_manager))
            tree.add_node(DraggableNode(text='node3',relation_manager=tree.relation_manager))
            tree.add_node(DraggableNode(text='node4',relation_manager=tree.relation_manager))
            box.add_widget(tree)
            tree2 = TreeView()
            node = TreeViewLabel(text='node1')
            tree2.add_node(node)
            tree2.add_node(TreeViewLabel(text='node2'),node)
            tree2.add_node(TreeViewLabel(text='node3'))
            tree2.add_node(TreeViewLabel(text='node4'))
            box.add_widget(tree2)
            return box


    TestApp().run()