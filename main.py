from matplotlib.animation import FuncAnimation

from satellite import satellite
import datetime

#this will be used to plot out our orbits
import matplotlib.pyplot as plt

import numpy as np

start_year = 2024
start_month = 1
start_day = 1

end_year = 2024
end_month = 9
end_day = 29

closest_distance_value = float('inf')
closest_distance_time = datetime.datetime(start_year, start_month, start_day)

#updates the frame of the animation to only show 3 points at a time
def update_data(frames,satellites, lines, tolerance):
  start_index = max(0,frames-2) # we want to make sure that we do not accidently go over the coordinates list
  end_index = frames + 1

  global closest_distance_value
  global closest_distance_time

  points = []
  for index,satellite in enumerate(satellites):
    x_positions = satellite.get_x_position()
    y_positions = satellite.get_y_position()
    z_positions = satellite.get_z_position()
    
    lines[index].set_data(x_positions[start_index:end_index],y_positions[start_index:end_index])
    lines[index].set_3d_properties(z_positions[start_index:end_index])  # Set the Z data for 3D
    points.append(np.array([x_positions[end_index], y_positions[end_index], z_positions[end_index]]))

  for x in range(len(points)):
    for y in range(x+1,len(points)):
      distance = abs(np.linalg.norm(points[y] - points[x]))
      if distance < closest_distance_value:
        if distance < tolerance:
          print("WARNING! WITHIN TOLERANCE ZONE!")
        closest_distance_value = distance
        closest_distance_time = satellites[0].get_times()[end_index]

        print(f'The closest distance between the two objects is {closest_distance_value}km')
        print(f'This occured on {closest_distance_time}')
        



  #calculate the closest two lines were to each other

    #if the distance is within the tolorance or less than the closest distance
      #update the closest distance variable and update the date it happened(and collison warning if needed) 
      #closet_date = satellite[0].get_times()[end_index]
  
  return lines,

def main():
  url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=33853&FORMAT=tle'
  file = 'Data/TLE data/Iridium 33 deb.txt'

  url2 = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=61219&FORMAT=tle' 
  file2 ='Data/TLE data/Cosmos 2251 deb.txt'

  Iridium_deb = satellite(file,is_file=True,track_time=True) #we only need to track the time of 1 sat

  # STARLINK WILL NOT WORK BECAUSE THE STARLINK DID NOT EXIST IN THE BEGINNING OF THE YEAR    
  STARLINK_32248 = satellite(file2,is_file=True,track_time=False) 


  start_date = datetime.datetime(start_year,start_month,start_day)
  end_date = datetime.datetime(end_year,end_month,end_day)

  #steps =  [weeks, days, hours, minutes, seconds]
  steps = [0,0,0,3,0] #this will get coordinates every 3 mins
  
  Iridium_deb.get_coordinates(start_date,end_date,steps)

  STARLINK_32248.get_coordinates(start_date,end_date,steps)
  
  fig = plt.figure()
   
  # add subplot with projection='3d'
  ax = fig.add_subplot(111, projection='3d')

  #this line represents the iridium debris coordinates
  Iridium_deb_line, = ax.plot([], [], [],color ='red')

  #this line represents the Starlink coordinates
  STARLINK_32248_line, = ax.plot([], [], [], color = "green")

  satellites = [Iridium_deb,STARLINK_32248]
  lines = [Iridium_deb_line,STARLINK_32248_line]

  tolerance = 100 #km

  animation = FuncAnimation(fig=fig,func=update_data,frames=len(Iridium_deb.get_x_position()),interval=10,fargs=(satellites,lines,tolerance,))


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