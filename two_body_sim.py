
#this will be used to parse the data
from sgp4.api import Satrec

#this will be used to format the julian date
from sgp4.api import jday

#this will be used to plot out our orbits
import matplotlib.pyplot as plt

#this will be used to obtain information from a url
import requests

import numpy as np

#used to store many satellites into an array
from sgp4.api import SatrecArray

import datetime
'''


url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
response = requests.get(url)

url2 = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=61219&FORMAT=tle'
response2 = requests.get(url2)

if response.status_code == 200:

  #gets the data and divides them
  tle_data = response.text.strip().splitlines()

  # Example: Parse the TLE
  satellite_name = tle_data[0]
  Iridium_TLE_line1 = tle_data[1]
  Iridium_TLE_line2 = tle_data[2]

  satellite = Satrec.twoline2rv(Iridium_TLE_line1, Iridium_TLE_line2)

  tle_data = response2.text.strip().splitlines()

  # Example: Parse the TLE
  satellite_name2 = tle_data[0]
  STARLINK_32248_TLE_line1 = tle_data[1]
  STARLINK_32248_TLE_line2 = tle_data[2]

  satellite2 = Satrec.twoline2rv(STARLINK_32248_TLE_line1, STARLINK_32248_TLE_line2)

  # Define the time for which you want to propagate the orbit (current date and time)
  year, month, day, hour, minute, second = 2024, 9, 27, 0, 0, 0
  #jd, fr = jday(year, month, day, hour, minute, second)

  time_intervals = [i for i in range(0, 1440, 10)]  # Every 10 minutes for 24 hours (1440 minutes)
  # Arrays to store position data
  x , y, z = [], [], []
  x2, y2, z2 = [] , [] , []


  closest_distance_value = float('inf')
  closest_distance_time = datetime.datetime(year, month, day)
  for minutes in time_intervals:
      future_time = datetime.datetime(year, month, day) + datetime.timedelta(minutes=minutes)
      jd, fr = jday(future_time.year, future_time.month, future_time.day, 
                    future_time.hour, future_time.minute, future_time.second)
      e, r, v = satellite.sgp4(jd, fr)

      point_1 = np.array([r[0],r[1],r[2]])
      # Append position data
      x.append(r[0])
      y.append(r[1])
      z.append(r[2])
      e, r, v = satellite2.sgp4(jd, fr)

      point_2 = np.array([r[0],r[1],r[2]])
      x2.append(r[0])
      y2.append(r[1])
      z2.append(r[2])

      
      current_distance = np.linalg.norm(point_2 - point_1)
      #if the closest distance value is greater than the current distance
      if closest_distance_value > current_distance:
        #then update the closest distance value
        closest_distance_value = current_distance
        closest_distance_time = future_time


  #print(e) #e will be non-zero if there was an error
  #print(r) #the positional vector in respect to time(represented as kilometers)
  #print(v) #the velocity vector in respect to time(represented as km/sec)


  #now plotting this data
  ax = plt.axes(projection = "3d")
  ax.plot(x,y,z, color = 'red')
  ax.plot(x2,y2,z2, color = 'green')

  # Plot the Earth as a blue sphere
  earth_radius = 6371  # Earth's radius in km
  u = np.linspace(0, 2 * np.pi, 100)
  v = np.linspace(0, np.pi, 100)
  x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
  y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
  z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
  ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.6)

  # Show the updated plot with the Earth
  ax.set_xlabel('X Position (km)')
  ax.set_ylabel('Y Position (km)')
  ax.set_zlabel('Z Position (km)')

  print(f'The closest distance between the two objects is {closest_distance_value}km')
  print(f'This occured on {closest_distance_time}')
  plt.show()
else:
  print(f"the request was not able to be made. Error code : {response.status_code}")
'''