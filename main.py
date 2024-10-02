from matplotlib.animation import FuncAnimation

from satellite import satellite
from datetime import datetime, timezone

#this will be used to plot out our orbits
import matplotlib.pyplot as plt

import numpy as np

import simulation

import requests

def main():
  

  #sample if you want to manually put in data
  url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
  Iridium_deb_file = 'Data/TLE data/Iridium 33 deb.txt'

  url2 = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=900&FORMAT=tle' 
  Cosmos_deb_file ='Data/TLE data/Cosmos 2251 deb.txt'

  Sat_174E_file = 'Data\TLE data\Sat-174E.txt'

  CALSPHERE_1_file = 'Data\TLE data\CALSPHERE 1.txt'

  Iridium_deb = satellite(Iridium_deb_file,is_file=True,track_time=True) #Set the track_time for the first Sat in the list to be true

  Cosmos_deb = satellite(Cosmos_deb_file,is_file=True,track_time=False) 

  Sat_174E = satellite(Sat_174E_file,is_file=True,track_time=False) 
  
  CALSPHERE_1= satellite(CALSPHERE_1_file,is_file=True,track_time=False) 

  satellites = [Iridium_deb,Cosmos_deb,Sat_174E,CALSPHERE_1]

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,10,0] #this will get coordinates every 3 mins

  playback_speed = 2 #each frame will update every 5 ms

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2024
  end_month = 10
  end_day = 1

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  tolerance = 30
  repeat = False

  sim  = simulation.simulation(satellites,tolerance,start_date,end_date,steps,playback_speed,repeat)

  #sim.start_simulation_no_plot()
  
  #print(f'Result: Closest distance was {sim.get_closest_distance_value()}km, and it happened on {sim.get_closest_distance_time()}UTC')

  sim.start_simulation_plot()
  '''
  
  #sample on how sim from a url with many satellites
  
  #link to active satellites
  url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2024
  end_month = 10
  end_day = 10

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,3,0] #this will get coordinates every 3 mins
  tolerance = 30 #Warning message if two satellites are closer than this value(km)
  playback_speed = 5 #frames will update every 5 ms
  repeat = False #repeat the simulation when completed
  sim = simulation.simulation(satellites=[],tolerance=tolerance,start_date=start_date,end_date=end_date,steps=steps,playback_speed=playback_speed,repeat=repeat)

  sim.populate_satellites(url,50) # this will grab


  sim.start_simulation_no_plot()

  #if i want the values for methods, I need first run start_simulation_no_plot()
  print(f'Result: Closest distance was {sim.get_closest_distance_value()}km, and it happened on {sim.get_closest_distance_time()}UTC')

  
  

  #sim.start_simulation_plot()
  '''
  
  
  
  

  

  

  
  




  

if __name__ == "__main__":
  main()

