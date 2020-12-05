import sqlite3
import pandas as pd


class Database:

    def __init__(self):
        """ init a new database and call prepare data func"""
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.prepare_data()

    def prepare_data(self):
        """ Read the given csv file, create a data frame and create a new table in the DB"""
        data = pd.read_csv(r'BikeShare.csv')
        df = pd.DataFrame(data, columns=['TripDuration', 'StartTime', 'StopTime', 'StartStationID', 'StartStationName',
                                         'StartStationLatitude', 'StartStationLongitude', 'EndStationID',
                                         'EndStationName',
                                         'EndStationLatitude', 'EndStationLongitude', 'BikeID', 'UserType', 'BirthYear',
                                         'Gender', 'TripDurationinmin'])
        try:
            df.to_sql(name='Trips', con=self.conn)
        except:
            print('Database already exists!')

        self.conn.commit()
        # conn.close()



    def get_start_location(self, start_location):
        """Get the rows with the same start location as our user's input"""
        query = "SELECT StartStationName, EndStationName, TripDurationinmin ,EndStationLatitude, EndStationLongitude " \
                " FROM Trips where StartStationName = '{0}'".format(start_location)
        df = pd.read_sql_query(query, self.conn)
        return df
    '''Get the latitude and longitude coordinates of start location'''
    def get_location_lat_lon(self, start_location):
        query = "SELECT  StartStationLongitude, StartStationLatitude " \
                " FROM Trips where StartStationName = '{0}'".format(start_location)
        df = pd.read_sql_query(query, self.conn)
        return df['StartStationLongitude'].iloc[0], df['StartStationLatitude'].iloc[0]

    def sort_by_time(self, trip_time, df):
        """Sort the data frame by trip time - take user's wished trip time in mind"""
        df.loc[:, "TripDurationinmin"] = df["TripDurationinmin"].apply(lambda x: abs(x - trip_time))
        results = df.sort_values(by='TripDurationinmin', ascending=True, )
        return results

    def recommend_me(self, num_of_places, df):
        """Return the number of recommendations the user wanted to receive (without duplicates)"""
        df = df.drop_duplicates('EndStationName')
        return df.head(num_of_places)

    def get_recommendation(self, start_location, trip_time, num_of_places):
        """A method that combines all of the 3 methods above, this method also interacts with the frontend."""
        df = self.get_start_location(start_location)
        df = self.sort_by_time(trip_time, df)
        df = self.recommend_me(num_of_places, df)
        if df.empty:
            print('The start location does not exist')
            return
        return df
#
# db = Database()
# res = db.get_recommendation('City Hall', 7, 7)
# print(res)
#
# res_dct = {i:res[i] for i in range(0, len(res))}
# print(res_dct)