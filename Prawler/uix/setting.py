from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from model.generator import Generator


class Setting(object):

    def check(self):

        pass

    def set_value(self):

        pass


class SettingField(TextInput):

    def on_text(self,_,text):

        pass


class Setting(RecycleView):

    def change_data(self,widget):

        app = App.get_running_app()