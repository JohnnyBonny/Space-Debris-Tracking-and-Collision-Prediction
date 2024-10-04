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

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,3,0] #this will get coordinates every 3 mins in the simulation

  playback_speed = 2 #each frame will update every 5 ms

  start_year = 2024
  start_month = 9
  start_day = 30

  end_year = 2025
  end_month = 10
  end_day = 1

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  tolerance_zone = 30
  repeat = False
  collision_zone = 5

  sim  = simulation.simulation(satellites,tolerance_zone,collision_zone,start_date,end_date,steps,playback_speed,repeat)

  sim.start_simulation_no_plot()
  
  print(f'Result: Closest distance was {sim.get_closest_distance_value()}km, and it happened on {sim.get_closest_distance_time()}UTC')

  print(f'{sim.get_sat1_name()} Coordinates: {sim.get_sat1_coordinates()}')
  print(f'{sim.get_sat2_name()} Coordinates: {sim.get_sat2_coordinates()}')
  print("\n\"Note that the SGP4 propagator returns raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame. raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame.\"")
  print("Source: https://pypi.org/project/sgp4/")
  
  

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
  end_day = 10

  start_date = datetime(start_year,start_month,start_day, tzinfo=timezone.utc)
  end_date = datetime(end_year,end_month,end_day, tzinfo=timezone.utc)

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,3,0] #this will get coordinates every 3 mins
  playback_speed = 5 #frames will update every 5 ms
  repeat = False #repeat the simulation when completed
  tolerance_zone = 30  #Warning message if two satellites are closer than this value(km)
  collision_zone = 5 #Collision message if two satellites are closer than this value(km)
  repeat = False

  #initializing the simulation
  sim  = simulation.simulation([],tolerance_zone,collision_zone,start_date,end_date,steps,playback_speed,repeat)

  sim.populate_satellites(url,50) # this will grab

  sim.start_simulation_no_plot()

  #if i want the values for methods, I need first run start_simulation_no_plot()
  print(f'Result: Closest distance was {sim.get_closest_distance_value()}km, and it happened on {sim.get_closest_distance_time()}UTC')

  print(f'{sim.get_sat1_name()} Coordinates: {sim.get_sat1_coordinates()}')
  print(f'{sim.get_sat2_name()} Coordinates: {sim.get_sat2_coordinates()}')
  print("\n\"Note that the SGP4 propagator returns raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame. raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame.\"")
  print("Source: https://pypi.org/project/sgp4/")


  sim.start_simulation_plot()

#sample of what happens if satellites collides
def example3():
  Cosmos_sat_file = 'Data\TLE data\Cosmos 2251 sat.txt'
  Iridium_sat_file = 'Data\TLE data\Iridium 33 sat.txt'
  Cosmos_sat = satellite(source=Cosmos_sat_file,is_file=True,track_time=True)
  Iridium_sat = satellite(source=Iridium_sat_file,is_file=True,track_time=False)

  satellites = [Cosmos_sat,Iridium_sat]

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,1,1,2,0] #this will get coordinates every 28 sec in the simulation

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
  sim  = simulation.simulation(satellites,tolerance_zone,collision_zone,start_date,end_date,steps,playback_speed,repeat)
  
  
  sim.start_simulation_no_plot()
  
  print(f'Result: Closest distance was {sim.get_closest_distance_value()}km, and it happened on {sim.get_closest_distance_time()}UTC')

  print(f'{sim.get_sat1_name()} Coordinates: {sim.get_sat1_coordinates()}')
  print(f'{sim.get_sat2_name()} Coordinates: {sim.get_sat2_coordinates()}')
  print("\n\"Note that the SGP4 propagator returns raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame. raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame that’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame.\"")
  print("Source: https://pypi.org/project/sgp4/")
  if len(sim.get_collision_dates()) > 0:
    print("Collision information:")
    print(f" the coordinates are: {sim.get_collision_coordinates()}")
    print(f"the dates are: {sim.get_collision_dates()}")
    print(f"the names of the satellites are:{sim.get_collision_sates_names()}")
  
  sim.start_simulation_plot()

def main():
  example2()
  

if __name__ == "__main__":
  main()

