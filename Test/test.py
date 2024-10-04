import math 
from tletools import TLE
import Data.Planet_Data.planetary_data as  pd 

import numpy as np
import skyfield

#source(5)
def ecc_anomaly(arr):
  ta,e = arr
  return 2*math.atan(math.sqrt((1-e)/(1+e))*math.tan(ta/2.0))

#Source(5)
def true_anomaly(arr):
  E,e = arr
  return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2.0))


Iridium_deb = TLE.from_lines(*open('Data/TLE data/Iridium 33 deb.txt').readlines())

orbital_period = (24.0 * 3600.0) / Iridium_deb.rev_num

semi_major_axis = (orbital_period**2)*pd.earth['mu']/(4 * (math.pi **2))**(1/3)

eccentric_anomaly = ecc_anomaly([Iridium_deb.M,Iridium_deb.ecc])

true_anomaly_value = true_anomaly([eccentric_anomaly,Iridium_deb.ecc])

print(eccentric_anomaly)
print(true_anomaly_value)
