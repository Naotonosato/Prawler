from kivy.event import EventDispatcher
from kivy.properties import ListProperty,ObjectProperty
from kivy.logger import Logger
from uix.relationtreeview import RelationNode
import utils


class RelationManager(utils.Subject,EventDispatcher):

    treeview = ObjectProperty(None)
    old_treeview = ObjectProperty(None,allownone=True)
    dragging_widget = ObjectProperty(None,allownone=True)

    def __init__(self,field,**kwargs):

        super(RelationManager,self).__init__(**kwargs)
        self.field = field
        self.field.add_observer(self)

    def update_from_field(self,field):
        
        new_widget = field.get_latest_widget()
        new_widget_name = new_widget.__class__.__name__
        node = RelationNode(
            text=new_widget_name,
            widget=new_widget,
            relation_manager=self.treeview.relation_manager)
        self.treeview.add_node(node)

    def notify(self):

        for observer in self.observers:
            observer.update_from_relation(self)

    def flatten_node(self,node):

        for i in node.nodes:
            
            for j in self.flatten_node(i):
                yield j
            else:
                yield i
            
    def register_dragging_widget(self,widget):
        
        if self.dragging_widget is None:
            self.dragging_widget = widget
        
    def release(self,touch):
            
        if self.dragging_widget is not None:
            from_node = self.dragging_widget
            to_node = self.treeview.get_node_at_pos(touch.pos)
            all_nodes = self.flatten_node(self.dragging_widget)
            if not to_node in all_nodes and to_node != from_node:
                        
                if to_node is not None:
                    self.treeview.remove_node(from_node)
                    self.treeview.add_node(from_node,to_node)
                else:
                    self.treeview.remove_node(from_node)
                    self.treeview.add_node(from_node)

                if hasattr(from_node,'widget'):
                    from_owned = from_node.widget.owned_widget
                    
                    if from_owned.parent is not None:
                        from_owned.parent.remove_widget(from_owned)

                    if hasattr(to_node,'widget'):
                        to_owned = to_node.widget.owned_widget
                        to_owned.add_widget(from_owned)

                self.notify()

        self.dragging_widget = None

    def get_relation(self):

        relation = [
        node for node in self.treeview.iterate_all_nodes()
        ]

        return relation

  