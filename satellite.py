import datetime
import requests

#this will be used to parse the data
from sgp4.api import Satrec

#this will be used to format the julian date
from sgp4.api import jday

class satellite:
  def __init__(self, source,is_file:bool,track_time:bool):
    self.source = source
    self.name = ""
    self.x_position = []
    self.y_position = []
    self.z_position = []
    self.is_file = is_file
    self.times = []
    self.data_recorded = datetime.datetime.now()

    #we only need to make 1 sat track the time since the simulation are all done at the sametime
    self.track_time =track_time


  
    
  def get_source(self):
    return self.source
  
  def get_name(self):
    return self.name
  
  def get_x_position(self):
    return self.x_position
  
  def get_y_position(self):
    return self.y_position
  
  def get_z_position(self):
    return self.z_position
  
  def get_times(self):
    return self.times
  

  def _get_TLE_Data(self,is_file,source):
    if is_file == False:
      response = requests.get(source)
      if response.status_code == 200:
        print("request successful")
        return response.text.strip().splitlines()
      else:
          print(f'The request from the url can not be met. Error {response.status_code}')

    else: 
      with open(source,'r') as file:
        content = file.read()
        return content.strip().splitlines()
      
  #will update the array values of x,y,z
  #steps will take list: [weeks, days, hours, minutes, seconds]
  def get_coordinates_man(self,start_date:datetime, end_date:datetime,steps:list[int]):
    tle_data = self._get_TLE_Data(is_file=self.is_file,source=self.source)
    
    # Example: Parse the TLE
    if self.name == "":
      self.name = tle_data[0].rstrip()

    satellite_line1 = tle_data[1]
    satellite_line2 = tle_data[2]

    satellite_info = Satrec.twoline2rv(satellite_line1, satellite_line2)
    
    #Now we will convert the dates
    future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))
    
    while future_time < end_date:
      if self.track_time:
        self.times.append(future_time)

      jd, fr = jday(future_time.year, future_time.month, future_time.day, future_time.hour, future_time.minute, future_time.second)
      
      e, r, v = satellite_info.sgp4(jd, fr) # can delete the v(velocity) if not needed

      # Append position data
      self.x_position.append(r[0])
      self.y_position.append(r[1])
      self.z_position.append(r[2])

      start_date = future_time
      future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))

    print("We good")

  #ONLY USE THIS IF YOU ARE USING POPULATE_SAT() IN SIMULATION FILE!
  #will update the array values of x,y,z
  #steps will take list: [weeks, days, hours, minutes, seconds]
  def get_coordinates_auto(self,start_date:datetime, end_date:datetime,steps:list[int],response, i):
    tle_data = response
    
    # Example: Parse the TLE
    if self.name == "":
      self.name = tle_data[i].rstrip()

    satellite_line1 = tle_data[i+1]
    satellite_line2 = tle_data[i+2]

    satellite_info = Satrec.twoline2rv(satellite_line1, satellite_line2)
    
    #Now we will convert the dates
    future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))
    
    while future_time < end_date:
      if self.track_time:
        self.times.append(future_time)

      jd, fr = jday(future_time.year, future_time.month, future_time.day, future_time.hour, future_time.minute, future_time.second)
      
      e, r, v = satellite_info.sgp4(jd, fr) # can delete the v(velocity) if not needed

      # Append position data
      self.x_position.append(r[0])
      self.y_position.append(r[1])
      self.z_position.append(r[2])

      start_date = future_time
      future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))

    print(f"We good {i/3}")


    


    

'''
  #this is used to validate the satellite data and see if it existed when the sim dates occur
  def validate_sat_date(self,start_date:datetime, satellite_info):

    #Converts epoch date to Python datetime.
    self.data_recorded = sat_epoch_datetime(satellite_info) #Source(8)

    #we are going to be using UTC as the time zone
    self.data_recorded = self.data_recorded.replace(tzinfo=datetime.timezone.utc)
    
    print(self.data_recorded)
    print(start_date)
    #insures that at least 1 simulation can be ran
    if (start_date < self.data_recorded):
      return True
    else:
      return False
    
  '''

'''
  def verify(self):
    response = response.get(self.url)

    if response == 200:
      self.verify = True
  '''