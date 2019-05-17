from kivy.uix.label import Label


class ErrorWidget(Label):

    def __init__(self,**kwargs):

        super(ErrorWidget,self).__init__(**kwargs)
        self.text = ' ! Error'