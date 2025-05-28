# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 23:47:44 2025

@author: jaime
"""

import time
from picamera2 import Picamera2
import io
import base64


class CAMERA_CAPTURE:
  
    def __init__(self):
        
        self.picam= Picamera2()
        self.MAX_B64_LENGTH=16000
    
    def schedule(self, event_input_name, event_input_value, res_height, res_width, delay):
    
        if event_input_name == 'INIT':
            if res_height == None:
                res_height=240
            if res_width == None:
                res_width=360
                
            config=self.picam.create_still_configuration(main={"size": (res_width, res_height)})
            self.picam.configure(config)
            self.picam.start()
            
            print("Camera ready to capture...")
            return [event_input_value, None, -1]
        
        elif event_input_name == 'READ':
            if delay == None:
                delay=1
            time.sleep(delay)
            data=io.BytesIO()
            self.picam.capture_file(data, format='jpeg')
            data.seek(0)
            encoded_image= base64.b64encode(data.read()).decode('utf-8')
            if len(encoded_image)>self.MAX_B64_LENGTH:
                print(f"Image too large: ({len(encoded_image)} chars)")
                print("Recommended maximum resolution width and height to prevent crashing: 400x400")
                return [None, event_input_value, []]
            
            print("New image captured")
            return [None, event_input_value, encoded_image] 
        
        elif event_input_name == 'STOP':
            
            self.picam.stop()
            self.picam.close()
            print("Camera closing.")
            return [None,None,None]
   