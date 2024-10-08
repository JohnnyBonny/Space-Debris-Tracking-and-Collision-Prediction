import datetime
#import random

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import requests
import satellite

#import matplotlib.colors as mcolors

#import math
 


fig = plt.figure()

class simulation:
  def __init__(self,satellites:list[satellite.satellite],tolerance_zone:int,collision_zone:int,start_date:datetime,end_date:datetime,increments:list[int],playback_speed:int,repeat:bool):
    self.satellites = satellites
    self.tolerance_zone = tolerance_zone
    self.start_date = start_date
    self.end_date = end_date
    self.increments = increments
    self.playback_speed = playback_speed
    self.repeat = repeat
    self.collision_zone = collision_zone

    #variables relating to when satellites are the closest to each
    #other in the simulation
    self.closest_distance_value= float('inf')
    self.closest_distance_time = start_date
    self.sat1_name = ""
    self.sat2_name = ""
    self.sat1_coordinates = []
    self.sat2_coordinates = []

    #a list of coordinates for the collision
    #example: [[sat1_coordinates,sat2_coordinates],]
    self.collision_coordinates = []
    
    self.collision_sats_names_set = set()

    #a list of a list of the two sats that collided
    #[[sat1,sat2],[sat1,sat3]..]
    self.collision_sats_names = []
    
    # example:[datetime,]
    self.collision_dates = [] 
    
    #a list of coordinates
    #example: [[sat1_coordinates,sat2_coordinates],]
    self.tolerance_coordinates = []
    
    #a list of a tuple two sats that are within the tolerance_zone
    self.tolerance_sats_names_set = set()

    self.tolerance_sat_dates = []
    self.tolerance_sats_names = []
    
    #used to check if we ran a simulation before
    self.sim_ran = False

    #if we got the coordinates already for all the satellites
    self.got_coordinates =False

    #--------------Text for 3D window---------------------------
    #the text so show the current time
    self.current_time_text = fig.text(.36, 0.9, "", style = 'italic', fontsize = 18, color = "black") 

    #the text to show the closest distance two satellites 
    self.closest_dist_text = fig.text(.01, 0.8, "", style = 'italic', fontsize = 13, color = "black") 

    #the text to show the time it happened 
    self.closest_time_text = fig.text(.01, 0.76, "", style = 'italic', fontsize = 13, color = "black") 

    #the text to show the two satillites that were close to each other 
    self.closest_sats_text = fig.text(.01, 0.72, "", style = 'italic', fontsize = 13, color = "black") 

    #the text to show the coordinates of sat1
    self.sat1_coord_text = fig.text(.01, 0.68, "", style = 'italic', fontsize = 13, color = "black") 

    #the text to show the coordinates of sat2
    self.sat2_coord_text = fig.text(.01, 0.64, "", style = 'italic', fontsize = 13, color = "black") 

    #the text to explain what the coordinates are a reference to
    self.info1_coord_text = fig.text(.01, 0.60, "Coordinate are in True Equator Mean Equinox” (TEME)", style = 'italic', fontsize = 13, color = "black") 

    #the text at the left of the plot to show the start date
    self.start_date_text = fig.text(.01, 0.50, f"Start date: {self.start_date}UTC", style = 'italic', fontsize = 13, color = "black") 
    
    #the text at the left of the plot to show the end date
    self.end_date_text = fig.text(.01, 0.46, f"End date: {self.end_date}UTC", style = 'italic', fontsize = 13, color = "black")

    self.increments_top_text = fig.text(.01, 0.42, f"Calulations will happen every", style = 'italic', fontsize = 13, color = "black")
    self.increments_bottom_text = fig.text(.01, 0.38, f"{self.increments[0]} weeks,{self.increments[1]} days,{self.increments[2]} hours,{self.increments[3]} minutes, {self.increments[4]} seconds", style = 'italic', fontsize = 13, color = "black")

    #the text to show when an two satellites fell within the tolerance zone
    self.tolerance_text = fig.text(.75, 0.8, f"Tolerance Zone({self.tolerance_zone}km) has not been met", style = 'italic', fontsize = 13, color = "green") 

    #the text to show when two satellites hit each other
    self.collision_status_text = fig.text(.75, 0.76, f"No Collision(within {self.collision_zone}km of each) has been detected", style = 'italic', fontsize = 13, color = "green") 

    #the text to show when two satellites hit each other
    self.collision_sat_text = fig.text(.75, 0.72, "", style = 'italic', fontsize = 13, color = "black")

    #the text to show when two satellites hit each other
    self.collision_time_text = fig.text(.75, 0.68, f"", style = 'italic', fontsize = 13, color = "black") 

    #the text to show when two satellites hit each other
    self.collision_coord_top_text = fig.text(.75, 0.64, f"", style = 'italic', fontsize = 13, color = "black") 
    self.collision_coord_bottom_text = fig.text(.75, 0.6, f"", style = 'italic', fontsize = 13, color = "black") 

    #--------------Text for 3D window---------------------------

  def get_closest_distance_value(self):
    return self.closest_distance_value

  def get_closest_distance_time(self):
    return self.closest_distance_time
  
  def get_sat1_name(self):
    return self.sat1_name
  
  def get_sat2_name(self):
    return self.sat2_name
  
  def get_sat1_coordinates(self):
    return self.sat1_coordinates
  
  def get_sat2_coordinates(self):
    return self.sat2_coordinates
   
  def get_collision_coordinates(self):
    return self.collision_coordinates
  
  def get_collision_sates_names(self):
    return self.collision_sats_names
  
  def get_collision_dates(self):
    return self.collision_dates
  

  def get_tolerance_coordinates(self):
    return self.tolerance_coordinates
  
  def get_tolerance_sats_names(self):
    return self.tolerance_sats_names
  
  def get_tolerance_sat_dates(self):
    return self.tolerance_sat_dates
  
  def validate_sim_date(self,start_date:datetime, end_date:datetime,increments:int):
    #insures that at least 1 simulation can be ran
    if (start_date + datetime.timedelta(weeks=increments[0], days=increments[1], hours=increments[2], minutes=increments[3], seconds=increments[4])) < end_date:
      return True
    else:
      return False
    
  #updates the frame of the animation to only show 4 points at a time(ONLY USED IN start_simulation_plot())
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
          self.closest_dist_text.set_text(f'The closest distance between the two objects is {self.closest_distance_value}km')
          self.closest_time_text.set_text(f'This occured on {self.closest_distance_time}UTC')
          self.closest_sats_text.set_text(f'between {self.satellites[x].get_name()} and {self.satellites[y].get_name()}')
          self.sat1_coordinates = [self.satellites[x].get_x_position()[end_index], self.satellites[x].get_y_position()[end_index],self.satellites[x].get_z_position()[end_index]]

          self.sat2_coordinates = [self.satellites[y].get_x_position()[end_index], self.satellites[y].get_y_position()[end_index],self.satellites[y].get_z_position()[end_index]]

          self.sat1_name = self.satellites[x].get_name()
          self.sat2_name = self.satellites[y].get_name()


          self.sat1_coord_text.set_text(f'{self.satellites[x].get_name()}: ({self.satellites[x].get_x_position()[end_index]:.2f}, {self.satellites[x].get_y_position()[end_index]:.2f}, {self.satellites[x].get_z_position()[end_index]:.2f})')

          self.sat2_coord_text.set_text(f'{self.satellites[y].get_name()}: ({self.satellites[y].get_x_position()[end_index]:.2f}, {self.satellites[y].get_y_position()[end_index]:.2f}, {self.satellites[y].get_z_position()[end_index]:.2f})')

        if distance <= self.collision_zone:
          #this is information we already know, so we can just skip it section and only update the text on the simulation
          if self.sim_ran == False:
            sat1_name = self.satellites[x].get_name()
            sat2_name = self.satellites[y].get_name()
            sats_name = (sat1_name,sat2_name)

            if sat_names not in self.collision_sats_names_set:
              self.collision_sats_names_set.add(sats_name)
              self.collision_coordinates.append([self.satellites[x].get_x_position()[end_index],self.satellites[x].get_y_position()[end_index],
              self.satellites[x].get_z_position()[end_index]])

              self.collision_sats_names.append([self.satellites[x].get_name(), self.satellites[y].get_name()])
              self.collision_dates.append(self.closest_distance_time)

          self.collision_status_text.set_text(f"Collision(within {self.collision_zone}km of each) has been detected")
          self.collision_status_text.set_color('red')

          self.collision_sat_text.set_text(f"Most recent collision:{self.satellites[x].get_name()} and {self.satellites[y].get_name()} ")
          self.collision_time_text.set_text(f"At {self.closest_distance_time}UTC")
          
          self.collision_coord_top_text.set_text(f'Collision is at(TEME reference frame):')
          self.collision_coord_bottom_text.set_text(f'x: {self.satellites[x].get_x_position()[end_index]:.2f} y: {self.satellites[x].get_y_position()[end_index]:.2f} z: {self.satellites[x].get_z_position()[end_index]:.2f}')

          #plot the collision
          ax.scatter(self.satellites[x].get_x_position()[end_index],self.satellites[x].get_y_position()[end_index],self.satellites[x].get_z_position()[end_index],color='red')
          ax.scatter(self.satellites[y].get_x_position()[end_index],self.satellites[y].get_y_position()[end_index],self.satellites[y].get_z_position()[end_index],color='red')


        if distance < self.tolerance_zone:
            #print("WARNING! WITHIN TOLERANCE ZONE!")
            self.tolerance_text.set_text(f'WARNING! WITHIN TOLERANCE ZONE OF {self.tolerance_zone}KM')
            self.tolerance_text.set_color('red')
            
            if self.sim_ran == False:
              sat_names =(self.satellites[x].get_name(), self.satellites[y].get_name())
              #put into tolerance list
              if sat_names not in self.tolerance_sats_names:
                sat1_coord = [self.satellites[x].get_x_position()[end_index],self.satellites[x].get_y_position()[end_index],
                self.satellites[x].get_z_position()[end_index]]

                sat2_coord = [self.satellites[y].get_x_position()[end_index],self.satellites[y].get_y_position()[end_index],self.satellites[y].get_z_position()[end_index]]

                self.tolerance_coordinates.append([sat1_coord,sat2_coord])

                self.tolerance_sats_names_set.add(sat_names)
                self.tolerance_sat_dates.append(self.closest_distance_time)
                self.tolerance_sats_names.append([self.satellites[x].get_name(), self.satellites[y].get_name()])
            

    #if we are on the very last frame put the points of the two satellites that were the closest to each other
    if frames == len(self.satellites[0].get_x_position())-2:
      
      ax.scatter(self.sat1_coordinates[0],self.sat1_coordinates[1],self.sat1_coordinates[2],color='orange')
      ax.scatter(self.sat2_coordinates[0],self.sat2_coordinates[1],self.sat2_coordinates[2],color='orange')
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
    if len(lines) /3  < number_sats:
      print(f"We can only grab at most {len(lines) / 3}")
      number_sats = len(lines) / 3

    #we are now going to grab 50 satellites 
    i=0
    while i < number_sats * 3:
      if i == 0:
        s1 = satellite.satellite("",False,True)
        s1.get_coordinates_auto(self.start_date,self.end_date,self.increments,lines,i)
        self.satellites.append(s1)
      else:
        s2 = satellite.satellite("",False,False)
        s2.get_coordinates_auto(self.start_date,self.end_date,self.increments,lines,i)
        self.satellites.append(s2)

      i+=3

    self.got_coordinates = True


  def start_simulation_plot(self):

    if len(self.satellites) == 0:
      print("Can not run test because there are no satellites in the list")
      return
    
    #We only need to reset these variables, because 
    #these variables are constantly updating in a simulation
    if self.sim_ran == True:
      self.closest_distance_value= float('inf')
      self.closest_distance_time = self.start_date

    # add subplot with projection='3d'
    ax = fig.add_subplot(111, projection='3d')

    #all the lines that are going to be displayed in each frame of the simulation
    lines = []
    

    if self.validate_sim_date(self.start_date,self.end_date,self.increments) == True:
      for index,satellite in enumerate(self.satellites):
      
        #if we never got the coordinates for the satellites, then we must get them now
        if self.got_coordinates == False:
          valid_satellite = satellite.get_coordinates_man(self.start_date,self.end_date,self.increments)

          if valid_satellite == True:
            #the plot variable is a 2D line with 3 positions(x,y,z)
            plot, = ax.plot([],[],[],color = 'r',linewidth=2)

            #the plot variables will tell the program the position to draw the line
            lines.append(plot)
            self.got_coordinates = True
          else:
            #if the first satellite can not be accessed, delete it and make the next satellite track the time
            if index == 0:
              self.satellites[index+1].set_track_time(True)
              
            self.satellites.remove(satellite)

        else:
            #the plot variable is a 2D line with 3 positions(x,y,z)
            plot, = ax.plot([],[],[],color = 'r',linewidth=2)

            #the plot variables will tell the program the position to draw the line
            lines.append(plot)

      

      # Plot the Earth as a blue sphere
      earth_radius = 6371  # Earth's radius in km

      #the angles around the equator
      u = np.linspace(0, 2 * np.pi, 100)

      #the angles from the north to the south pole
      v = np.linspace(0, np.pi, 100)

      x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
      y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
      z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
      ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.6)
      #sphere reference: YouTube, YouTube, www.youtube.com/watch?v=DV4GjHH-fvc&t=32s. Accessed 6 Oct. 2024. 
      
      animation = FuncAnimation(fig=fig,func=self.update_data,frames=len(self.satellites[0].get_x_position())-1,interval=self.playback_speed,fargs=(lines,ax,),repeat= self.repeat)

      
      # Show the updated plot with the Earth
      ax.set_xlabel('X Position (km)')
      ax.set_ylabel('Y Position (km)')
      ax.set_zlabel('Z Position (km)')

      self.sim_ran = True


      plt.show()
    else:
      print("The simulation dates are incorrect. Please try again")


  
  def start_simulation_no_plot(self):

    if len(self.satellites) == 0:
      print("Can not run test because there are no satellites in the list")
      return
    
    #Do a simulation if we haven't ran a simulation before,
    #If we had ran a simulation. All the variables should already be updated
    if self.sim_ran ==False:

      self.sim_ran = True
      
      if self.validate_sim_date(self.start_date,self.end_date,self.increments) == True:
        print("Starting Simulation")
        #if the satellites were manual put in a list then get the coordinates
        if self.got_coordinates != True:

          for index,satellite in enumerate(self.satellites):
            valid_satellite = satellite.get_coordinates_man(self.start_date,self.end_date,self.increments)
            
            if valid_satellite == True:
              self.got_coordinates = True

            else:
              #if the first satellite can not be accessed, delete it and make the next satellite track the time
              if index == 0:
                self.satellites[index+1].set_track_time(True)

              print(f'removing {satellite.get_name()}')
              #if the satellite was not able to be obtained, delete it
              self.satellites.remove(satellite)
        

              
        
        
        #stores the array of all the satellites coordinates
        for step in range(0,len(self.satellites[0].get_x_position())):
          
          #points represents all the satellites coordinates on the current step
          points = []
          for satellite in self.satellites:
            x_positions = satellite.get_x_position()
            y_positions = satellite.get_y_position()
            z_positions = satellite.get_z_position()
    
            points.append(np.array([x_positions[step], y_positions[step], z_positions[step]]))

          else:

            #calculate the distance between each point in the current step 
            for x in range(len(points)):
              for y in range(x+1,len(points)):

                #The Euclidean distance formula
                distance = abs(np.linalg.norm(points[y] - points[x])) #Source: “Calculate the Euclidean Distance Using NumPy.” GeeksforGeeks, GeeksforGeeks, 30 July 2024, www.geeksforgeeks.org/calculate-the-euclidean-distance-using-numpy/. 

                if distance < self.closest_distance_value:
                  distance = float(f"{distance:.2f}")
                  self.closest_distance_value = distance
                  self.closest_distance_time = self.satellites[0].get_times()[step] 

                  #update the values
                  self.sat1_coordinates = [self.satellites[x].get_x_position()[step], self.satellites[x].get_y_position()[step],self.satellites[x].get_z_position()[step]]

                  self.sat2_coordinates = [self.satellites[y].get_x_position()[step], self.satellites[y].get_y_position()[step],self.satellites[y].get_z_position()[step]]

                  self.sat1_name = self.satellites[x].get_name()
                  self.sat2_name = self.satellites[y].get_name()

                #message for if the satellites are within collision zone value km
                if distance <= self.collision_zone:

                  #create a hashset for the satellite pairs, so that we do not any duplicates
                  sat_names =(self.satellites[x].get_name(), self.satellites[y].get_name())
                  if sat_names not in self.collision_sats_names_set:
                    self.collision_sats_names_set.add(sat_names)

                    collision_coordinates = [self.satellites[x].get_x_position()[step],self.satellites[x].get_y_position()[step],self.satellites[x].get_z_position()[step]]

                    self.collision_coordinates.append(collision_coordinates)
                    self.collision_sats_names.append([self.satellites[x].get_name(), self.satellites[y].get_name()])
                    self.collision_dates.append(self.closest_distance_time)

                #if the distance is within the tolerance zone
                #update the variables relating to the tolerance zone variables
                if distance < self.tolerance_zone:
                    
                    #create a hashset for the satellite pairs, so that we do not any duplicates
                    sat_names =(self.satellites[x].get_name(), self.satellites[y].get_name())
                    if sat_names not in self.tolerance_sats_names_set:
                      sat1_coord = [self.satellites[x].get_x_position()[step],self.satellites[x].get_y_position()[step],
                      self.satellites[x].get_z_position()[step]]

                      sat2_coord = [self.satellites[y].get_x_position()[step],self.satellites[y].get_y_position()[step],
                      self.satellites[y].get_z_position()[step]]

                      self.tolerance_coordinates.append([sat1_coord,sat2_coord])

                      self.tolerance_sats_names_set.add(sat_names)
                      self.tolerance_sat_dates.append(self.closest_distance_time)
                      self.tolerance_sats_names.append([self.satellites[x].get_name(), self.satellites[y].get_name()])

    else:
      print("Starting Simulation")
    print("Simulation complete") 
    

  def print_info(self):
      print("\n\"Note that the SGP4 propagator returns raw x,y,z Cartesian coordinates in a “True Equator Mean Equinox” (TEME) reference frame \nthat’s centered on the Earth but does not rotate with it — an “Earth centered inertial” (ECI) reference frame.")
      print("Source: https://pypi.org/project/sgp4/ \n") 

      print(f'Result: Closest distance was {self.closest_distance_value}km, and it happened on {self.closest_distance_time}UTC')

      print(f'{self.sat1_name} Coordinates: {self.sat2_coordinates}')
      print(f'{self.sat2_name} Coordinates: {self.sat2_coordinates}')

      if len(self.collision_dates) > 0:
        print("\nCollision information:")
        print(f"the coordinates are: {self.collision_coordinates}")
        print(f"the dates are: {self.collision_dates}")
        print(f"the names of the satellites are:{self.collision_sats_names}")
      else:
        print("\nNo Collision detected")

      print(f'\nAll the sats in the tolerance zone {self.tolerance_sats_names}')
      print(f'All the dates these sats were the tolerance zone {self.tolerance_sat_dates}')
        