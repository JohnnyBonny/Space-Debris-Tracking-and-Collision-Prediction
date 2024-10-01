import datetime
import random

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import satellite

import matplotlib.colors as mcolors
 


class simulation:
  def __init__(self,satellites,tolerance,start_date,end_date,steps,playback_speed):
    self.satellites = satellites
    self.tolerance = tolerance
    self.start_date = start_date
    self.end_date = end_date
    self.steps = steps
    self.playback_speed = playback_speed
    self.closest_distance_value= float('inf')
    self.clostest_distance_time = start_date

    self.start_simulation()

  def get_clostest_distance_value(self):
    return self.closest_distance_value

  def get_clostest_distance_time(self):
    return self.clostest_distance_time
  
  def validate_sim_date(self,start_date:datetime, end_date:datetime,steps:int):
    #insures that at least 1 simulation can be ran
    if (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4])) < end_date and start_date < end_date:
      return True
    else:
      return False
    
  #updates the frame of the animation to only show 4 points at a time
  def update_data(self,frames,lines):
    start_index = max(0,frames-3) # we want to make sure that we do not accidently go over the coordinates list
    end_index = frames + 1


    points = []
    for index,satellite in enumerate(self.satellites):
      x_positions = satellite.get_x_position()
      y_positions = satellite.get_y_position()
      z_positions = satellite.get_z_position()
      
      lines[index].set_data(x_positions[start_index:end_index],y_positions[start_index:end_index])
      lines[index].set_3d_properties(z_positions[start_index:end_index])  # Set the Z data for 3D
      points.append(np.array([x_positions[end_index], y_positions[end_index], z_positions[end_index]]))

    #calculate the closest two lines were to each other
    for x in range(len(points)):
      for y in range(x+1,len(points)):
        distance = abs(np.linalg.norm(points[y] - points[x])) #Source: (12)


        if distance < self.closest_distance_value:
          if distance < self.tolerance:
            print("WARNING! WITHIN TOLERANCE ZONE!")
          if distance <= 4:
            print(f"Oh no {self.satellites[x].get_name()} and {self.satellites[y].get_name()} collided!(most likely)")

          self.closest_distance_value = distance
          self.closest_distance_time = self.satellites[0].get_times()[end_index]

          print(f'The closest distance between the two objects is {self.closest_distance_value}km')
          print(f'This occured on {self.closest_distance_time}UTC between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')
    
    return lines,
    
  def start_simulation(self):
    fig = plt.figure()
    plt.style.use('dark_background')
    # add subplot with projection='3d'
    ax = fig.add_subplot(111, projection='3d')
    lines = []
    
    colors = list(mcolors._colors_full_map.keys())

    if self.validate_sim_date(self.start_date,self.end_date,self.steps):
      for satellite in self.satellites:
        satellite.get_coordinates(self.start_date,self.end_date,self.steps)
        plot, = ax.plot([],[],[],color = random.choice(colors))
        lines.append(plot)
      
      animation = FuncAnimation(fig=fig,func=self.update_data,frames=len(self.satellites[0].get_x_position()),interval=self.playback_speed,fargs=(lines,))
    
    
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
    else:
      print("The simulation dates are incorrect. Please try again")
     