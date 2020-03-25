import pandas as pd
import numpy as np
from geopy.distance import distance
from geopy.geocoders import OpenMapQuest
from geopy.extra.rate_limiter import RateLimiter
from pandarallel import pandarallel

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def calculate_per(row):
    '''Calculate the Player Efficiency Rating of a player based on the input data. The formula was taken from
    https://bleacherreport.com/articles/113144-cracking-the-code-how-to-calculate-hollingers-per-without-all-the-mess'''

    per = (row.FGM * 85.910
           + row.Steals * 53.897
           + row.Three_PTM * 51.757
           + row.FTM * 46.845
           + row.Blocks * 39.190
           + row.Offensive_Reb * 39.190
           + row.Assists * 34.677
           + row.Defensive_Reb * 14.707
           - row.Fouls * 17.174
           - row.FT_Miss * 20.091
           - row.FG_Miss * 39.190
           - row.Turnovers * 53.897) * (1 / row.Minutes)

    return per


def get_distance_between(row):
    '''
    A lambda function that calculates the distance (in miles) between two addresses in a DataFrame row
    :param row: A row inside a DataFrame that has the following series names: school_city, birthplace_city, Country_name
    :return: An Integer representing the distance in miles
    '''

    # Get latitude and longitude of the player's school
    school_geo = geocode(row.school_city)
    school_lat = school_geo.latitude
    school_long = school_geo.longitude

    try:

        # Get the latitude and longitude of the player's hometown
        if type(row.birthplace_state) == float and np.isnan(row.birthplace_state):
            birth_geo = geocode(str(row.birthplace_city + ", " + row.Country_name))
        else:
            birth_geo = geocode(str(row.birthplace_city + ", " + row.birthplace_state + ", " + row.Country_name))

        birth_lat = birth_geo.latitude
        birth_long = birth_geo.longitude

        # Calculate the distance in miles between the two coordinates
        distance_num = distance((school_lat, school_long), (birth_lat, birth_long)).miles

        return distance_num

    except:
        print("There was an error with the following city: {},  player: {} {}".format(row.birthplace_city, row.first_name, row.last_name))
        pass


if __name__ == '__main__':

    stats_df = pd.read_csv('player_locations_and_stat_totals.csv')
    stats_df['birthplace_country'] = stats_df['birthplace_country'].str.strip()

    country_codes_df = pd.read_csv('country_codes.csv', index_col=0)

    stats_df = stats_df.merge(country_codes_df, how='left', left_on='birthplace_country', right_on='code_3digit')

    # Instantiate Geopy Nominatim
    geolocator = OpenMapQuest(api_key='XqxsOEvVxEWTifxzkzeh1rWC9sJMZg0x')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=.4)

    # print(geocode('Hightstown, NJ, United States of America'))

    stats_df['PER'] = stats_df.apply(calculate_per, axis=1)

    pandarallel.initialize(progress_bar=True)
    stats_df['miles_between_school_and_home'] = stats_df.parallel_apply(get_distance_between, axis=1)

    stats_df = stats_df.sort_values(by='PER', ascending=False).reset_index(drop=True)

    stats_df.to_csv('output_showing_miles_between.csv')

    print(stats_df.head(100))