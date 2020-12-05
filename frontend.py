import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from mybackend import Database
from kivy.uix.image import AsyncImage, Image
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


# read the kv file in order to get app layout
kv = Builder.load_file("my.kv")


class MainWindow(GridLayout):
    """A class that basically runs the Gui."""
    db = Database()
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    places = ObjectProperty(None)

    def recommend(self):
        """ Recommend function, takes input from user (such as SelfLocation, How long does the user want to travel, How
        many recommendations he wants to get) then sends those inputs to the backend in order to get a recommendation."""
        # print("My location: ", self.location.text, ", How many minutes will you travel?: ", self.time.text,
        #       "Number of recommendations: ", self.places.text)
        start_point = self.location.text
        try:
            trip_duration = int(self.time.text)
            recommendations_number = int(self.places.text)
            try:
                results = Database.get_recommendation(self.db, start_point, trip_duration, recommendations_number)
                results = 'We recommend you to travel:\n' + '\n'.join(results)
                popup(results, 'Recommended Locations')
            except:
                popup('The start location does not exist', 'Error')
        except:
            popup('Please enter numbers only for Trip duration and Number of Recommendations', 'Error')

        self.location.text = ""
        self.time.text = ""
        self.places.text = ""


def popup(msg, title):
    """ function in order to create a popup window, msg -> msg in the popup, title -> title of the popup"""
    popup = Popup(title=title, content=Label(text=msg), size_hint=(None, None), size=(400, 400))
    popup.open()


# run the main window of the app
class MyApp(App):
    def build(self):
        return MainWindow()


# run app
if __name__ == '__main__':
    MyApp().run()
