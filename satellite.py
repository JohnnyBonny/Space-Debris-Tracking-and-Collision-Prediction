import datetime
import requests

#this will be used to parse the data
from sgp4.api import Satrec

#this will be used to format the julian date
from sgp4.api import jday


#this is used to validate the simulation date in the get_coordinates()
def validate_date(start_date:datetime, end_date:datetime,steps:int):
  #insures that at least 1 simulation can be ran
  if (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4])) < end_date and start_date < end_date:
    return True
  else:
    return False

def get_TLE_Data(is_file,url, file_name):
  if is_file == False:
    response = requests.get(url)
    if response.status_code == 200:
      print("request successful")
      return response.text.strip().splitlines()
    else:
        print(f'The request from the url can not be met. Error {response.status_code}')

  else: 
    with open(file_name,'r') as file:
      content = file.read()
      return content.strip().splitlines()

  

class satellite:
  def __init__(self, url,file ,is_file:bool):
    self.url = url
    self.name = ""
    self.x_position = []
    self.y_position = []
    self.z_position = []
    self.file = file
    self.is_file = is_file


  '''
  def verify(self):
    response = response.get(self.url)

    if response == 200:
      self.verify = True
  '''
    
  def get_url(self):
    return self.url
  
  def get_name(self):
    return self.name
  
  def get_x_position(self):
    return self.x_position
  
  def get_y_position(self):
    return self.y_position
  
  def get_z_position(self):
    return self.z_position
  
  
  #will update the array values of x,y,z
  #steps will take list: [weeks, days, hours, minutes, seconds]
  def get_coordinates(self,start_date:datetime, end_date:datetime,steps:list[int]):

    #check if the simulation dates are valid
    if validate_date(start_date, end_date, steps):

      tle_data = get_TLE_Data(is_file=self.is_file,url="",file_name=self.file)
      
      # Example: Parse the TLE
      if self.name == "":
        self.name = tle_data[0]

      satellite_line1 = tle_data[1]
      satellite_line2 = tle_data[2]

      satellite_info = Satrec.twoline2rv(satellite_line1, satellite_line2)

      #Now we will convert the dates
      future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))
      
      while future_time < end_date:
        jd, fr = jday(future_time.year, future_time.month, future_time.day, future_time.hour, future_time.minute, future_time.second)
        
        e, r, v = satellite_info.sgp4(jd, fr) # can delete the v(velocity) if not needed

        # Append position data
        self.x_position.append(r[0])
        self.y_position.append(r[1])
        self.z_position.append(r[2])

        start_date = future_time
        future_time = (start_date + datetime.timedelta(weeks=steps[0], days=steps[1], hours=steps[2], minutes=steps[3], seconds=steps[4]))

      

      print("We good")
      
    else:
      print("The simulation dates are incorrect. Please try again")


    

    