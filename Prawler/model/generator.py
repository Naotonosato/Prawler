class Generator(object):

    def __init__(self,field):

        self.field = field
        super(Generator,self).__init__()

    def set_relation(self,relation,root):

        appointed = {}
        get_nodes = lambda x: x.nodes
        get_children = lambda x: x.children

        self.kv = 'FloatLayout:\n'

        appointed,kv = self.generate_tree(root, appointed,'')
        
        self.generate_from_relation(appointed['Root'])
        self.save_kv()

    def generate_tree(self,node,dict_,kv,nest=1):
        
        widget = 'Root'
        if hasattr(node,'widget'):
            widget = node.widget.owned_widget.__class__.__name__ 

        if not dict_.get(widget):
            dict_[widget] = []
    
        for child_node in node.nodes:
                
            c_widget = child_node.widget
            c_owned_widget = c_widget.owned_widget
            c_name = c_owned_widget.__class__.__name__
            c_prop = self.field.get_widget_properties(c_widget)
            to_add_dict = {c_name:[],'properties':c_prop,'nest':nest} 
             
            #if to_add_dict not in dict_[widget]:
            dict_[widget].append(to_add_dict)

            if child_node.nodes:
                    #if to_add_dict not in dict_[widget]:
                    #dict_[widget].append(to_add_dict)
                index = dict_[widget].index(to_add_dict)                    
                self.generate_tree(child_node,dict_[widget][index],kv,nest+1)
                    
        return dict_,kv

    def generate_from_relation(self,relation):          

        for i in relation:
            widget_name = tuple(set(i.keys()) - {'nest','properties'})[0]
            properties = i['properties']
            nest = i['nest']
            self.kv += ('    ' * nest)
            self.kv += (widget_name + ':\n')
            
            for prop in properties:
                value = properties[prop]
                self.kv += '    ' * (nest+1) + prop + ': ' + str(value) + '\n'
            
            self.generate_from_relation(i[widget_name])

    def _generate(self,result_dict,kv=r''):

        for widget in result_dict:
            properties = result_dict[widget]['properties']
            nest = result_dict[widget]['nest']
            kv += '\n' + '    ' * nest + widget + ':'
            
            for prop in properties:
                defaultvalue = str(prop.defaultvalue)
                prop_name = prop.name
                value = properties[prop]
                if type(value) == str:
                    value = "'" + value + "'"
                if str(value) == defaultvalue:
                    continue
                kv += '\n' + '    '*(nest+1) + prop_name + ': ' + str(value) 

    def save_kv(self):

        with open('test1.kv','wt') as f:
            f.write(self.kv)