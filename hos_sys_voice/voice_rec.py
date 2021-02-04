#kivy app
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput 

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

import project_hBack as backend


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
        backend.speech_option()
        #

    def entry_man(self):
        print("type new entry")
        #
    
    def lookup_patient_voice(self):
        print("who to look up")
        #

    def lookup_patient_man(self):
        print("type who to look up")
        #

    def process(self, entry):
        patient = entry
        print(patient)
        #query with entry return buttons
    
    def process2(self, pEntry, dEntry, tEntry):
        entry ={
            'patient': pEntry,
            'diagnosis': dEntry,
            'treatment': tEntry
        }
        print(entry)

        #reset the entries
        pEntry= ''
        dEntry=''
        tEntry=''
        
        #send the dictionary to backend

if __name__ == '__main__':
    #database setup
    backend.begin()
    app = StartMainApp()
    app.run()
