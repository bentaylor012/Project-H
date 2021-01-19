#kivy app
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

#import backend
#mport project_hBack as backend


#main app UI
class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class TypeScreenEntry(Screen):
    pass

class TypeScreenPatient(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass
presentation = Builder.load_file("startmain.kv")

class StartMainApp(App):
    def build(self): 
        return presentation

    def on_button_press(self):
        print("do something crazy")
        self.get_running_app().stop()
    
    def entry_voice(self):
        print("start new entry")

    def entry_man(self):
        print("type new entry")
    
    def lookup_patient_voice(self):
        print("who to look up")
    
    def lookup_patient_man(self):
        print("type who to look up")


        #Microphone(device_index: Union[int,None] = None, sample_rate: int = 16000,
        #chunk_size: int = 1024) -> Microphone

if __name__ == '__main__':
    #database setup
    app = StartMainApp()
    app.run()
