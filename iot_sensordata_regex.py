#!/usr/bin/env python
# coding: utf-8
import json
from json import JSONEncoder
import re
import time
import datetime



class SensorData:
    def __init__(self):
        self.date = ''        # data collection date
        self.temperature = [] # temperature values
        self.humidity = []    # humdity values




class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__ 
   


# In[ ]:


def process_sensor_data(file_name):
    start_time = time.time()    
    
    # Extract date value from each line
    PATTERN_HEADER = r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
    # Data pattern is used for iterating available temperature and humdity pairs
    PATTERN_DATA = r'(?i)(?P<temperature>\d{4}|NNNN)(?P<humidity>\d{3}|NNN)'
    
    sensor_data_regex = re.compile(PATTERN_DATA)
    
    all_data = []
    
    with open(file_name,'r', encoding='utf-8') as rdr:            
        for line in rdr:
            # One row contains a day worth of data
            sensor_data = SensorData()
            
            match = re.search(PATTERN_HEADER, line)

            if match:
                sensor_data.date =                     '-'.join([match.group('year'),match.group('month'),match.group('day')])
                
                header_len = len(match.group(0))
                
                # compiled object - you can search from specific point in text
                #  skip the header portion and look for temperature-humdity pairs
                match_iter = sensor_data_regex.finditer(line,header_len)
                
                for match in match_iter:
                    # access temperature and humidity groups
                    sensor_data.temperature.append(match.group('temperature'))
                    sensor_data.humidity.append(match.group('humidity'))                    

                all_data.append(sensor_data)
        
        print ('Elapsed time for parsing and format conversion: {0:.2f}s'.format(time.time()-start_time))
        
        with open(file_name+'.json','w', encoding='utf-8') as wr:
            json.dump(all_data, wr, ensure_ascii=False, cls=MyEncoder, indent=True)
            
        print ('Elapsed time write to File : {0:.2f}s'.format(time.time()-start_time))


# In[ ]:


#file_name =  r"../iotsensor/data/sensordata.txt"
file_name =  r"sensordata.txt"
process_sensor_data(file_name)





