from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from LocationMark import LocationMark
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class RootWidget(AnchorLayout):
    # New-York latitude and longitude coordinates are:  40.730610, -73.935242



    def __init__(self, **kwargs):
        self.marks = kwargs.pop("marks",None)
        self.start_location_lat = float(kwargs.pop("start_location_lat",None))
        self.start_location_lon = float(kwargs.pop("start_location_lon",None))
        super(RootWidget, self).__init__(**kwargs)
        self.anchor_x = 'right'
        self.anchor_y = 'top'
        mapview = MapView(zoom=14, lat=self.start_location_lat, lon=self.start_location_lon)
        self.add_widget(mapview)
        start_location_mark = MapMarkerPopup(source="icons/pin.png",lon=self.start_location_lon,
                                                 lat=self.start_location_lat)
        mapview.add_widget(start_location_mark)
        for index, row in self.marks.iterrows():
            map_mark = LocationMark(name=row['EndStationName'], source="icons/bicycle.png",lon=row['EndStationLongitude'], lat=row['EndStationLatitude'])

            print(row['EndStationName'])
            # map_mark.bind(on_press=self.show_name)
            # map_mark.bind(on_press = lambda row['EndStationName']: self.show_name)
            mapview.add_widget(map_mark)

    def show_name(self,instance):
        print(instance.location_name)





