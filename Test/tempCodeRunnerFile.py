
#this will be used to parse the data
from sgp4.api import Satrec

#this will be used to format the julian date
from sgp4.api import jday
import matplotlib.pyplot as plt
import requests

url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
response = requests.get(url)

if response.status_code == 200:
  tle_data = response.text.strip().splitlines()

    # Example: Parse the first satellite (ISS) TLE
  satellite_name = tle_data[0]
  Iridium_TLE_line1 = tle_data[1]
  Iridium_TLE_line2 = tle_data[2]

  satellite = Satrec.twoline2rv(Iridium_TLE_line1, Iridium_TLE_line2)

  jd,fr = jday(2024,12,9,20,42,0)

  e, r, v = satellite.sgp4(jd, fr)

  print(e) #e will be non-zero if there was an error
  print(r) #the positional vector in respect to time(represented as kilometers)
  print(v) #the velocity vector in respect to time(represented as km/sec)


  #now plotting this data

  ax = plt.axes(projection = "3d")
  ax.scatter(r[0],r[1],r[2])
else:
  print(f"the request was not able to be made. Error code : {response.status_code}")
