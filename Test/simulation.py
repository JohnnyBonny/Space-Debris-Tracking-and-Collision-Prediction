#used to parse the TLE file
from tletools import TLE

Iridium_deb = TLE.from_lines(*open('Data/TLE data/Iridium 33 deb.txt').readlines())
Cosmos_deb = TLE.from_lines(*open('Data/TLE data/Cosmos 2251 deb.txt').readlines())
Sat_2024_174E = TLE.from_lines(*open('Data/TLE data/2024-174E.txt').readlines())
Starlink = TLE.from_lines(*open('Data/TLE data/Starlink-32248.txt').readlines())

print(Iridium_deb.name)

print(Cosmos_deb.name)

print(Sat_2024_174E.name)

print(Starlink.name)