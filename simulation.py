import datetime
import random

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import requests
import satellite

import matplotlib.colors as mcolors
 


fig = plt.figure()

class simulation:
  def __init__(self,satellites:list[satellite.satellite],tolerance:int,start_date:datetime,end_date:datetime,steps:list[int],playback_speed:int,repeat:bool):
    self.satellites = satellites
    self.tolerance = tolerance
    self.start_date = start_date
    self.end_date = end_date
    self.steps = steps
    self.playback_speed = playback_speed
    self.closest_distance_value= float('inf')
    self.closest_distance_time = start_date
    self.sat1_coordinates = []
    self.sat2_coordinates = []
    self.repeat = repeat
    self.sim_ran = False

    #the text so show the current time
    self.current_time_text = fig.text(.36, 0.9, "", style = 'italic', fontsize = 14, color = "black") 

    #the text to show the closest distance two satellites 
    self.closest_dist_text = fig.text(.01, 0.8, "", style = 'italic', fontsize = 9, color = "black") 

    #the text to show the time it happened 
    self.closest_time_text = fig.text(.01, 0.76, "", style = 'italic', fontsize = 9, color = "black") 

    #the text to show the two satillites that were close to each other 
    self.closest_sats_text = fig.text(.01, 0.72, "", style = 'italic', fontsize = 9, color = "black") 

    #the text to show the coordinates of sat1
    self.sat1_coord_text = fig.text(.01, 0.68, "", style = 'italic', fontsize = 9, color = "black") 

    #the text to show the coordinates of sat2
    self.sat2_coord_text = fig.text(.01, 0.64, "", style = 'italic', fontsize = 9, color = "black") 

    #the text to show when an two satellites fell within the tolerance zone
    self.tolerance_text = fig.text(.75, 0.8, f"Tolerance Zone({self.tolerance}km) has not been met", style = 'italic', fontsize = 9, color = "green") 

    #the text to show when two satellites hit each other

    #the text at the bottom of the plot to show the start date

    #the text at the bottom of the plot to show the end date

    #the text at the bottom of the plot to show the tolerance

    #the text at the bottom of the plot to show the steps



    
    #if we used the populate sat function
    self.did_auto_populate =False


  def get_closest_distance_value(self):
    return self.closest_distance_value

  def get_closest_distance_time(self):
    return self.closest_distance_time
  
  def get_sat1_coordinates(self):
    return self.sat1_coordinates
  
  def get_sat2_coordinates(self):
    return self.sat2_coordinates
  
  def validate_sim_date(self,start_date:datetime, end_date:datetime,steps:int):
    #insures that at least 1 simulation can be ran
    if (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4])) < end_date and start_date < end_date:
      return True
    else:
      return False
    
  #updates the frame of the animation to only show 4 points at a time
  def update_data(self,frames,lines,ax):
    start_index = max(0,frames-3) #frames - 3 means we are only getting 4 points at a time
    end_index = frames + 1


    datetime_obj = self.satellites[0].get_times()[end_index]

    # Format it to show only month, day, year, hour, and minute
    formatted_time = datetime_obj.strftime('%m-%d-%Y %H:%M')
    self.current_time_text.set_text("current time: " + formatted_time + " UTC")  # Update the existing text object
    
    points = []
    for index,satellite in enumerate(self.satellites):
      x_positions = satellite.get_x_position()
      y_positions = satellite.get_y_position()
      z_positions = satellite.get_z_position()

      #we are only grabbing the end_index because we want the most recent data
      lines[index].set_data(x_positions[start_index:end_index],y_positions[start_index:end_index])
      lines[index].set_3d_properties(z_positions[start_index:end_index])  # Set the Z data for 3D
      points.append(np.array([x_positions[end_index], y_positions[end_index], z_positions[end_index]]))

    #calculate the closest two lines were to each other
    for x in range(len(points)):
      for y in range(x+1,len(points)):
        distance = abs(np.linalg.norm(points[y] - points[x])) #Source: (12)

        if distance < self.closest_distance_value:
          distance = float(f"{distance:.2f}")
          self.closest_distance_value = distance
          self.closest_distance_time = self.satellites[0].get_times()[end_index]
          if distance <= 4:
            print(f"Oh no {self.satellites[x].get_name()} and {self.satellites[y].get_name()} collided!(most likely)")
            print(f'The position of this collision is at x: {self.satellites[x].get_x_position()[end_index]:.2f} y: {self.satellites[x].get_y_position()[end_index]:.2f} z: {self.satellites[x].get_z_position()[end_index]:.2f}')
            print(f'This occured on {self.closest_distance_time}UTC between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')

          if distance < self.tolerance:
            print("WARNING! WITHIN TOLERANCE ZONE!")
            self.tolerance_text.set_text(f'WARNING! WITHIN TOLERANCE ZONE OF {self.tolerance}KM')
          

          print(f'The closest distance between the two objects is {self.closest_distance_value}km')
          print(f'This occured on {self.closest_distance_time}UTC between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')

          self.closest_dist_text.set_text(f'The closest distance between the two objects is {self.closest_distance_value}km')
          self.closest_time_text.set_text(f'This occured on {self.closest_distance_time}UTC')
          self.closest_sats_text.set_text(f'between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')

          self.sat1_coordinates = [self.satellites[x].get_x_position()[end_index], self.satellites[x].get_y_position()[end_index],self.satellites[x].get_z_position()[end_index]]

          self.sat2_coordinates = [self.satellites[y].get_x_position()[end_index], self.satellites[y].get_y_position()[end_index],self.satellites[y].get_z_position()[end_index]]


          self.sat1_coord_text.set_text(f'{self.satellites[x].get_name()}: ({self.satellites[x].get_x_position()[end_index]:.2f}, {self.satellites[x].get_y_position()[end_index]:.2f}, {self.satellites[x].get_z_position()[end_index]:.2f})')

          self.sat2_coord_text.set_text(f'{self.satellites[y].get_name()}: ({self.satellites[y].get_x_position()[end_index]:.2f}, {self.satellites[y].get_y_position()[end_index]:.2f}, {self.satellites[y].get_z_position()[end_index]:.2f})')

    #if we are on the very last frame
    if frames == len(self.satellites[0].get_x_position())-2:
      
      ax.scatter(self.sat1_coordinates[0],self.sat1_coordinates[1],self.sat1_coordinates[2],color='red')
      ax.scatter(self.sat2_coordinates[0],self.sat2_coordinates[1],self.sat2_coordinates[2],color='red')
    return lines,

  #only for when there are more than 1 in the url
  def populate_satellites(self,url, number_sats):
    response = requests.get(url)

    if response.status_code == 200:
      print("request successful")
    else:
      print(f'Error code {response.status_code}')
      return
    
    lines = response.text.strip().splitlines()

    #grab as many satellites from the url if the user input > the number of sats
    if len(lines) * 3 < number_sats:
      print(f"We can only grab at most {len(lines) / 3}")
      number_sats = len(lines) / 3

    #we are now going to grab 50 satellites 
    i=0
    while i < number_sats * 3:
      if i == 0:
        s1 = satellite.satellite("",False,True)
        s1.get_coordinates_auto(self.start_date,self.end_date,self.steps,lines,i)
        self.satellites.append(s1)
      else:
        s2 = satellite.satellite("",False,False)
        s2.get_coordinates_auto(self.start_date,self.end_date,self.steps,lines,i)
        self.satellites.append(s2)

      i+=3

      self.did_auto_populate = True


      
    
  def start_simulation_plot(self):

    if self.sim_ran == True:
      self.closest_distance_value= float('inf')
      self.closest_distance_time = self.start_date

    # add subplot with projection='3d'
    ax = fig.add_subplot(111, projection='3d')
    lines = []
    
    #colors = list(mcolors._colors_full_map.keys())

    if self.validate_sim_date(self.start_date,self.end_date,self.steps) == True:
      for satellite in self.satellites:
        #satellite.get_coordinates_man(self.start_date,self.end_date,self.steps)
        #plot, = ax.plot([],[],[],color = random.choice(colors))
        if self.did_auto_populate != True:
          satellite.get_coordinates_man(self.start_date,self.end_date,self.steps)
        plot, = ax.plot([],[],[],color = 'y')
        lines.append(plot)

      # Plot the Earth as a blue sphere
      earth_radius = 6371  # Earth's radius in km
      u = np.linspace(0, 2 * np.pi, 100)
      v = np.linspace(0, np.pi, 100)
      x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
      y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
      z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
      ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.6)
      
      animation = FuncAnimation(fig=fig,func=self.update_data,frames=len(self.satellites[0].get_x_position())-1,interval=self.playback_speed,fargs=(lines,ax,),repeat= self.repeat)

      
      # Show the updated plot with the Earth
      ax.set_xlabel('X Position (km)')
      ax.set_ylabel('Y Position (km)')
      ax.set_zlabel('Z Position (km)')

      plt.show()
    else:
      print("The simulation dates are incorrect. Please try again")

  def start_simulation_no_plot(self):
    self.sim_ran = True
    

    if self.validate_sim_date(self.start_date,self.end_date,self.steps) == True:

      #if the satellites were manual put in a list then get the coordinates
      if self.did_auto_populate != True:
        for satellite in self.satellites:
          satellite.get_coordinates_man(self.start_date,self.end_date,self.steps)
      
      
        #stores the array of all the satellites coordinates
      for step in range(0,len(self.satellites[0].get_x_position())):
        points = []
        for satellite in self.satellites:
          x_positions = satellite.get_x_position()
          y_positions = satellite.get_y_position()
          z_positions = satellite.get_z_position()
        
          points.append(np.array([x_positions[step], y_positions[step], z_positions[step]]))

        
        #calculate the closest two lines were to each other in 1 step
        for x in range(len(points)):
          for y in range(x+1,len(points)):
            distance = abs(np.linalg.norm(points[y] - points[x])) #Source: (12)

            if distance < self.closest_distance_value:
              distance = float(f"{distance:.2f}")
              self.closest_distance_value = distance
              self.closest_distance_time = self.satellites[0].get_times()[step] 
              if distance <= 4:
                print(f"Oh no {self.satellites[x].get_name()} and {self.satellites[y].get_name()} collided!(most likely)")
                print(f'The position of this collision is at x: {self.satellites[x].get_x_position()[step]:.2f} y: {self.satellites[x].get_y_position()[step]:.2f} z: {self.satellites[x].get_z_position()[step]:.2f}')
                print(f'This occured on {self.closest_distance_time}UTC between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')

              if distance < self.tolerance:
                print("WARNING! WITHIN TOLERANCE ZONE!")

              self.sat1_coordinates = [self.satellites[x].get_x_position()[step], self.satellites[x].get_y_position()[step],self.satellites[x].get_z_position()[step]]

              self.sat2_coordinates = [self.satellites[y].get_x_position()[step], self.satellites[y].get_y_position()[step],self.satellites[y].get_z_position()[step]]



        