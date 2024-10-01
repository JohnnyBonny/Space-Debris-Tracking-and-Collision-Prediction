from matplotlib.animation import FuncAnimation

from satellite import satellite
from datetime import datetime, timezone

#this will be used to plot out our orbits
import matplotlib.pyplot as plt

import numpy as np

import simulation


def main():
  url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
  Iridium_file = 'Data/TLE data/Iridium 33 deb.txt'

  url2 = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=61219&FORMAT=tle' 
  Cosmos_file ='Data/TLE data/Cosmos 2251 deb.txt'

  Sat_174E_file = 'Data\TLE data\Sat-174E.txt'

  CALSPHERE_1_file = 'Data\TLE data\CALSPHERE 1.txt'

  Iridium_deb = satellite(Iridium_file,is_file=True,track_time=True) #Set the track_time for the first Sat in the list to be true

  Cosmos_deb = satellite(Cosmos_file,is_file=True,track_time=False) 

  Sat_174E = satellite(Sat_174E_file,is_file=True,track_time=False) 
  
  CALSPHERE_1= satellite(CALSPHERE_1_file,is_file=True,track_time=False) 

  satellites = [Iridium_deb,Cosmos_deb,Sat_174E,CALSPHERE_1]

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,3,0] #this will get coordinates every 3 mins

  playback_speed = 5 #each frame will update every 5 ms

  start_year = 2024
  start_month = 1
  start_day = 1

  end_year = 2024
  end_month = 9
  end_day = 29

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  simulation.simulation(satellites,50,start_date,end_date,steps,playback_speed)
  

if __name__ == "__main__":
  main()



  '''
  #now plotting this data
  ax = plt.axes(projection = "3d")
  
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

  plt.show()
  i = 0 
  #draw the orbit in real time
  while i+2 < len(Iridium_deb.get_x_position())- 1:
    line = ax.plot(Iridium_deb.get_x_position()[i:i+3], Iridium_deb.get_y_position()[i:i+3], Iridium_deb.get_z_position()[i:i+3])

    plt.pause(.01)

    line.remove()

    plt.draw()
    i+=2

'''