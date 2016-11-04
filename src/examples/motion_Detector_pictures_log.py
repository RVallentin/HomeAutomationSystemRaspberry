import io
import time, datetime
import picamera 
import cv2
import cv2.cv as cv
import numpy as np
from time import sleep
import picamera as camera
import logging

import os as os




def saveImage():
    print("Initializing camera...")
    with picamera.PiCamera() as camera:
        #camera.start_preview()
        print("Setting focus and light level on camera...")
        
        logging.basicConfig(filename=datetime.datetime.now().strftime("%Y-%m-%d")+'.txt',level=logging.DEBUG)
    
        print("Capture picture...")
        # Create the in-memory stream
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        
        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        tstmp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        image_file  = "image_%s_%05d.jpg" % (tstmp, count)
    
        #get the date to save the directory with the actual day
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        #get the actual directory of the aplication
        actual = os.getcwd()
        
        #test to see if the directory with the date already exist
        if os.path.exists(date):
            os.chdir(date) # go to the directory date if it exist
        
        #if the directory do not exist then, create the directory and access it
        else :
            os.mkdir(date)
                print('Directory created: ' + date)
                os.chdir(date)
        
        #save the image on the directory date
        cv2.imwrite(file_name, self.__image0)
        print("  - Image saved:", file_name)
        #return to the main directory of the aplication
        os.chdir(actual)



                


if __name__ == "__main__":
    process()
    
    
    
    
    
    