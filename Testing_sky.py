from skyfield.api import load, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt

# Load the TLE data
tle_lines = [
    "ISS (ZARYA)",
    "1 25544U 98067A   22327.57358602  .00001764  00000+0  44026-4 0  9993",
    "2 25544  51.6426 274.6222 0006982  17.3130  58.2278 15.50162985376689"
]

# Create a satellite object using the TLE
satellite = EarthSatellite(tle_lines[1], tle_lines[2], tle_lines[0])

# Load a time scale to compute positions
ts = load.timescale()

# Choose a time span for the simulation
time_range = ts.utc(2024, 9, range(0, 24))  # 24 hours at one-hour intervals

# Calculate positions of the satellite over time
positions = [satellite.at(t).position.km for t in time_range]

# Convert to a numpy array for easier plotting
positions = np.array(positions)

# Plot the satellite's X, Y, Z positions
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label='ISS Orbit')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.legend()
plt.show()
