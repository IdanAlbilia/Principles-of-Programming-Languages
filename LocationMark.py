from kivy_garden.mapview import MapMarkerPopup
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class LocationMark(MapMarkerPopup):

    def __init__(self, **kwargs):
        self.location_name = kwargs.pop("name", "")
        super(MapMarkerPopup, self).__init__(**kwargs)
        self.popup=None

    def on_press(self):
        if not self.popup:
            self.popup = Popup(title='Details', content=Label(text=self.location_name), size_hint=(None, None), size=(150, 100))
        self.popup.open()
