from matplotlib.animation import FuncAnimation

from satellite import satellite
from datetime import datetime, timezone

#this will be used to plot out our orbits
import matplotlib.pyplot as plt

import numpy as np

import simulation

import requests

#sample if you want to use a file or use a url with only 1 tle data in it
def example1():  
  url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
  Iridium_deb_file = 'Data/TLE data/Iridium 33 deb.txt'

  url2 = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=900&FORMAT=tle' 
  Cosmos_deb_file ='Data/TLE data/Cosmos 2251 deb.txt'

  Sat_174E_file = 'Data\TLE data\Sat-174E.txt'

  CALSPHERE_1_file = 'Data\TLE data\CALSPHERE 1.txt'

  #a source can be a file or URL.
  Iridium_deb = satellite(source=Iridium_deb_file,is_file=True,track_time=True) #Set the track_time for the first Sat in the list to be true

  Cosmos_deb = satellite(source=Cosmos_deb_file,is_file=True,track_time=False) 

  Sat_174E = satellite(source=Sat_174E_file,is_file=True,track_time=False) 
  
  CALSPHERE_1= satellite(source=CALSPHERE_1_file,is_file=True,track_time=False) 

  satellites = [Iridium_deb,Cosmos_deb,Sat_174E,CALSPHERE_1]

  #increments =  [weeks, days, hours, minutes, seconds]
  increments = [0,0,0,3,0] #this will get coordinates every 3 mins in the simulation

  playback_speed = 2 #each frame will update every 5 ms

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2024
  end_month = 10
  end_day = 1

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  tolerance_zone = 100
  repeat = False
  collision_zone = 5

  sim  = simulation.simulation(satellites,tolerance_zone,collision_zone,start_date,end_date,increments,playback_speed,repeat)

  sim.start_simulation_no_plot()
  sim.print_info()
  sim.start_simulation_plot()

#sample on how sim from a url with many satellites
def example2():

  #link to active satellites
  url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2024
  end_month = 10
  end_day = 5

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  #increments =  [weeks, days, hours, minutes, seconds]
  increments = [0,0,0,3,0] #this will get coordinates every 3 mins
  playback_speed = 5 #frames will update every 5 ms
  repeat = False #repeat the simulation when completed
  tolerance_zone = 100  #Warning message if two satellites are closer than this value(km)
  collision_zone = 5 #Collision message if two satellites are closer than this value(km)
  repeat = False

  #initializing the simulation
  sim  = simulation.simulation([],tolerance_zone,collision_zone,start_date,end_date,increments,playback_speed,repeat)

  sim.populate_satellites(url,50) # this will grab 50 satellites from the url

  sim.start_simulation_no_plot()

  sim.print_info()
  sim.start_simulation_plot()

  sim.print_info()

#sample of what happens if satellites collides
def example3():
  Cosmos_sat_file = 'Data\TLE data\Cosmos 2251 sat.txt'
  Iridium_sat_file = 'Data\TLE data\Iridium 33 sat.txt'
  Cosmos_sat = satellite(source=Cosmos_sat_file,is_file=True,track_time=True)
  Iridium_sat = satellite(source=Iridium_sat_file,is_file=True,track_time=False)

  satellites = [Cosmos_sat,Iridium_sat]

  #increments =  [weeks, days, hours, minutes, seconds]
  increments = [0,1,1,2,0] #this will get coordinates every 28 sec in the simulation

  playback_speed = 0 #each frame will update every 2 ms

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2025
  end_month = 12
  end_day = 8

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  tolerance_zone = 100
  collision_zone = 91
  repeat = False

  #initializing the simulation
  sim  = simulation.simulation(satellites,tolerance_zone,collision_zone,start_date,end_date,increments,playback_speed,repeat)
  
  
  sim.start_simulation_no_plot()
  

  #sim.start_simulation_plot()

#for slides
def example4():
  Iridium_url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
  Iridium_deb_file = 'Data/TLE data/Iridium 33 deb.tx'

  Cosmos_url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=900&FORMAT=tle' 
  Cosmos_deb_file ='Data/TLE data/Cosmos 2251 deb.txt'

  #a source can be a file or URL.
  #Set the track_time for the first Sat in the list to be true
  Iridium_deb = satellite(source=Iridium_deb_file,is_file=True,track_time=True) 

  Cosmos_deb = satellite(source=Cosmos_deb_file,is_file=True,track_time=False)

  satellites = [Iridium_deb,Cosmos_deb]

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2024
  end_month = 10
  end_day = 1


  #make sure that the start date is before the end_date
  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)
  
  #increments =  [weeks, days, hours, minutes, seconds]
  #Ensure the increments do not exceed the total time difference
  increments = [0,0,0,3,0] #this will get coordinates every 3 mins in the simulation

  tolerance_zone = 100 # a "warning zone"(km)
  repeat = False #to repeat the simulation once it has finished
  collision_zone = 5 # how close two objects will have to be to classify as collision(in km)

  playback_speed = 2 #each frame will update every 2 ms


  sim  = simulation.simulation(satellites,tolerance_zone,collision_zone,start_date,end_date,increments,playback_speed,repeat)

  sim.start_simulation_no_plot() #will calculate all the values without the plots(faster)

  sim.start_simulation_plot() #will calculate all the values with the plots(3D animation, but slower at runtime)

  sim.print_info()#to print out information obtained front the simulation
  
  
  print(f'\nsim.get_closest_distance_time():{sim.get_closest_distance_time()}') #datetime of when two satellites were the closest to each other
  print(f'sim.get_closest_distance_value():{sim.get_closest_distance_value()}') #In km, how close the two satellites were
  print(f'sim.get_sat1_name():{sim.get_sat1_name()}') #Closest satellite 1 
  print(f'sim.get_sat1_coordinates():{sim.get_sat1_coordinates()}')
  print(f'sim.get_sat2_name():{sim.get_sat2_name()}') #Closest satellite 2
  print(f'sim.get_sat2_coordinates():{sim.get_sat2_coordinates()}\n')
  
  print(f'sim.get_collision_coordinates():{sim.get_collision_coordinates()}') #the coordinates of the two satellites colliding
  print(f'sim.get_collision_sates_names():{sim.get_collision_sates_names()}') # the names of the two satellites colliding
  print(f'sim.get_collision_dates():{sim.get_collision_dates()}\n') #datetime when collision occured

  print(f'sim.get_tolerance_coordinates():{sim.get_tolerance_coordinates()}') #the coordinates of the two satellites within the tolerance zone
  print(f'sim.get_tolerance_sat_dates():{sim.get_tolerance_sat_dates()}')#the datetime of the two satellites when they are within the tolerance zone
  print(f'sim.get_tolerance_sat_names():{sim.get_tolerance_sats_names()}')#the names of the two satellites when they arewithin the tolerance zone

def main():
  example4()


  

if __name__ == "__main__":
  main()

