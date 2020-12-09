import sqlite3
import pandas as pd
import math


class Database:

    def __init__(self, database_name="database.db"):
        """ init a new database and call prepare data func"""
        self.database_name = database_name
        if not self.check_if_table_exists():
            self.prepare_data()
        else:
            print("database already exists")

    def check_if_table_exists(self):
        """"check if tha database already exists"""
        query = "SELECT name FROM sqlite_master " \
                "WHERE type='table' AND name='Trips';"
        df = self.view(query)
        return not df.empty

    def prepare_data(self):
        """ Read the given csv file, create a data frame and create a new table in the DB"""
        data = pd.read_csv(r'BikeShare.csv')
        df = pd.DataFrame(data, columns=['TripDuration', 'StartTime', 'StopTime', 'StartStationID', 'StartStationName',
                                         'StartStationLatitude', 'StartStationLongitude', 'EndStationID',
                                         'EndStationName',
                                         'EndStationLatitude', 'EndStationLongitude', 'BikeID', 'UserType', 'BirthYear',
                                         'Gender', 'TripDurationinmin'])
        conn = sqlite3.connect(self.database_name)
        df.to_sql(name='Trips', con=conn)
        conn.commit()
        conn.close()

    def view(self, query):
        """This method view the database and return and the answer in dataframe  """
        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_start_location(self, start_location):
        """Get the rows with the same start location as our user's input"""
        query = "SELECT StartStationName, EndStationName, AVG (TripDurationinmin) as TripDurationinmin ," \
                " StartStationLatitude,StartStationLongitude, " \
                "EndStationLatitude, EndStationLongitude " \
                " FROM Trips where StartStationName = '{0}'" \
                "GROUP by StartStationName, EndStationName  ".format(start_location)
        df = self.view(query)
        return df

    '''Get the latitude and longitude coordinates of start location'''

    def get_location_lat_lon(self, start_location):
        query = "SELECT  StartStationLongitude, StartStationLatitude " \
                " FROM Trips where StartStationName = '{0}'".format(start_location)
        df = self.view(query)
        if df.empty:
            return None, None
        return df['StartStationLongitude'].iloc[0], df['StartStationLatitude'].iloc[0]

    @staticmethod
    def sort_by_time(trip_time, df):
        """Sort the data frame by trip time - take user's wished trip time in mind"""
        df['Distance'] = df.apply(lambda x: math.sqrt((x["StartStationLongitude"] - x['EndStationLongitude']) ** 2
                                                      + (x["StartStationLatitude"] - x['EndStationLatitude']) ** 2),
                                  axis=1)
        df.loc[:, "TripDurationinmin"] = df["TripDurationinmin"].apply(lambda x: str(abs(x - int(trip_time))))
        results = df.sort_values(by=['TripDurationinmin', 'Distance'], ascending=True, )
        return results

    @staticmethod
    def recommend_me(num_of_places, df):
        """Return the number of recommendations the user wanted to receive (without duplicates)"""
        df = df.drop_duplicates('EndStationName')
        return df.head(num_of_places)

    def get_recommendation(self, start_location, trip_time, num_of_places):
        """A method that combines all of the 3 methods above, this method also interacts with the frontend."""
        trip_time = int(trip_time)
        num_of_places = int(num_of_places)
        if trip_time < 0 or num_of_places < 0:
            raise ValueError
        df = self.get_start_location(start_location)
        df = self.sort_by_time(trip_time, df)
        df = self.recommend_me(num_of_places, df)
        return df
