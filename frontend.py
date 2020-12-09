from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from mybackend import Database
from MapWidget.MapWidget import MapWidget


class MainWindow(GridLayout):
    """A class that basically runs the Gui."""
    db = Database()
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    places = ObjectProperty(None)

    def recommend(self):
        """ Recommend function, takes input from user (such as SelfLocation, How long does the user want to travel, How
        many recommendations he wants to get) then sends those inputs to the backend in order to get a recommendation."""

        if not self.location.text.strip() or not self.time.text.strip() or not self.places.text.strip():
            self.popup(Label(text='You must enter current location, time to travel and number of recommendations  '),
                       'Error')
            return
        # The .title() method capitalize first letter of each word
        start_point = self.location.text.strip().title()
        trip_duration = self.time.text
        recommendations_number = self.places.text
        lon, lat = Database.get_location_lat_lon(self.db, start_point)
        if lon is None:
            self.popup(Label(text='The start location does not exist'), 'Error')
            return
        try:
            results = Database.get_recommendation(self.db, start_point, trip_duration, recommendations_number)
            self.popup(MapWidget(marks=results, start_location_lat=lat, start_location_lon=lon),
                       'Recommended Locations', (600, 600))
        except ValueError:
            self.popup(Label(text='Please enter positive numbers for Trip duration and Number of Recommendations'), 'Error')
        # clean the text input
        self.location.text = ""
        self.time.text = ""
        self.places.text = ""

    def popup(self, content, title, size=(600, 300)):
        """ function in order to create a popup window, content in the popup, title -> title of the popup"""
        popup = Popup(title=title, content=content, size_hint=(None, None), size=size)
        popup.open()


# run the main window of the app
class MyApp(App):
    def build(self):
        return MainWindow()


# run app
if __name__ == '__main__':
    MyApp().run()
