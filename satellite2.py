import datetime
import requests
import validators
#this will be used to parse the data
from sgp4.api import Satrec

#this will be used to format the julian date
from sgp4.api import jday

class satellite2:
  def __init__(self, source):
    self.source = source
    self.name = ""
    self.x_position = []
    self.y_position = []
    self.z_position = []

    #represents the file or url being split into many lines
    self.lines = []

    

  def get_name(self):
    return self.name
  
  def set_name(self,name):
    self.name = name

  def set_lines(self,lines):
    self.lines = lines
  
  def get_x_position(self):
    return self.x_position
  
  def get_y_position(self):
    return self.y_position
  
  def get_z_position(self):
    return self.z_position
  
  def get_times(self):
    return self.times
  
  def validate_TLE_Data(self):
    #if it a url,parse the url
    if validators.url(self.source):
      response = requests.get(self.source)
      if response.status_code == 200:
        print("request successful")
        self.lines = response.text.strip().splitlines()
      else:
          print(f'The request from the url can not be met. Error {response.status_code}')
           
    else: 
      try:
        with open(self.source,'r') as file:
          content = file.read()
          self.lines = content.strip().splitlines()
      
      except FileNotFoundError:
        print(f"The file does not exist for {self.source}")
        

      
  def get_coordinates(self,jd:float,fr:float):
      #if there are coordinates in the list, clear them
        self.x_position.clear()
        self.y_position.clear()
        self.z_position.clear()
      #if the source has already been verified, then we will skip the verification process
        if len(self.lines) == 0:
          self.validate_TLE_Data()

      #once verified, we will now get the coordinates
        if len(self.lines) != 0:

          #get tle data and pass in a index variable to get the specific lines of the for the satellite
          # Example: Parse the TLE
          if self.name == "":
            self.name = self.lines[0].rstrip()

          satellite_line1 = self.lines[1]
          satellite_line2 = self.lines[2]

          satellite_info = Satrec.twoline2rv(satellite_line1, satellite_line2)

          e, r, v = satellite_info.sgp4(jd, fr)

          #get the coordinates from the date and store them into the coordinates variable
          # Append position data
          self.x_position.append(r[0])
          self.y_position.append(r[1])
          self.z_position.append(r[2]) 

      

      #get the coordinates from the date and store them into the coordinates variable

    


    