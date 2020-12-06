from kivy.uix.anchorlayout import AnchorLayout
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from MapWidget.LocationMark import LocationMark


class MapWidget(AnchorLayout):
    '''' This class represent of map widget heritage from anchor Layout that contains
     mapview-Mapview is a Kivy widget for displaying interactive map
           '''

    def __init__(self, **kwargs):
        # marks -> the locations recommends
        self.marks = kwargs.pop("marks", None)
        # start location coordinates
        self.start_location_lat = float(kwargs.pop("start_location_lat", None))
        self.start_location_lon = float(kwargs.pop("start_location_lon", None))
        super(MapWidget, self).__init__(**kwargs)
        self.anchor_x = 'right'
        self.anchor_y = 'top'
        map_view = MapView(zoom=14, lat=self.start_location_lat, lon=self.start_location_lon)
        self.add_widget(map_view)
        start_location_mark = MapMarkerPopup(source="MapWidget/icons/pin.png", lon=self.start_location_lon,
                                             lat=self.start_location_lat)
        map_view.add_widget(start_location_mark)
        # Add marks on the map
        for index, row in self.marks.iterrows():
            map_mark = LocationMark(name=row['EndStationName'], source="MapWidget/icons/bicycle.png",
                                    lon=row['EndStationLongitude'], lat=row['EndStationLatitude'])
            map_view.add_widget(map_mark)







