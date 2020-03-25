# NCAA March Madness Query

An SQL/Python project that uses Google Cloud's NCAA March Madness database to analyze the relationship between a team's 
success and how far away its players are from home.

## Resources
### [Google Cloud - NCAA Basketball BigQuery Dataset](https://console.cloud.google.com/marketplace/details/ncaa-bb-public/ncaa-basketball)
This is the database where I queried the data about the NCAA Basketball Players. You can view my query in [this sql file](query_player_locations_and_stat_totals.sql)
and even run the query in [Google's BigQuery Console](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=ncaa_basketball&page=dataset)

### [Kaggle - Country Codes](https://www.kaggle.com/koki25ando/country-code)
Google's country data was structured as 3-digit codes (USA, CAN, MEX, etc.), but the Python GeoPy API requires fully-spelled
country names to find the longitude and latitude of an address. I downloaded [the csv file](country_codes.csv) of country codes from this
page and joined it with my Google query output. You can see how I performed the join in [my python code](basketball_players.py).

### [GeoPy Documentation](https://geopy.readthedocs.io/en/stable/)
I used this Python Library to find the longitude and latitude of every college town and player birthplace in my dataset.
I proceeded to take those coordinates can calculate the distance between those points with another GeoPy function. You
can see how I implemented those onto my dataset with the help of pandas in [my python code](basketball_players.py).