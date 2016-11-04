import time, datetime
import RPi.GPIO as GPIO
import os
from Tkinter import *
import picamera as camera
import logging
import numpy as np
import cv2.cv as cv
import picamera
import cv2

light_pin = 16
pir_pin = 4
servo_pin = 23

ROW = [7,11,13,15] #Inputs of the keypad
COL = [12,16,18,22] #Outputs of the keypad

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D']]


class Adafruit_CharLCD(object):
    
    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80
    
    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00
    
    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00
    
    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    
    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00
    
    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00
    
    def __init__(self, pin_rs=21, pin_e=20, pins_db=[16, 12, 25, 24], GPIO=None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)
        
        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)
        
            self.write4bits(0x33)  # initialization
            self.write4bits(0x32)  # initialization
            self.write4bits(0x28)  # 2 line 5x7 matrix
            self.write4bits(0x0C)  # turn cursor off 0x0E to enable cursor
            self.write4bits(0x06)  # shift cursor right
            
            self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
            
            self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
            self.displayfunction |= self.LCD_2LINE
            
            # Initialize to default text direction (for romance languages)
            self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
            self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode
            
                self.clear()

def begin(self, cols, lines):
    if (lines > 1):
        self.numlines = lines
            self.displayfunction |= self.LCD_2LINE

def home(self):
    self.write4bits(self.LCD_RETURNHOME)  # set cursor position to zero
        self.delayMicroseconds(3000)  # this command takes a long time!

    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY)  # command to clear display
        self.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

def setCursor(self, col, row):
    self.row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self.numlines:
            row = self.numlines - 1  # we count rows starting w/0
    self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

def noDisplay(self):
    """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

def noCursor(self):
    """ Turns the underline cursor off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Turns the underline cursor on """
        self.displaycontrol |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

def noBlink(self):
    """ Turn the blinking cursor off """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self):
        """ Turn the blinking cursor on """
        self.displaycontrol |= self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

def DisplayLeft(self):
    """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

def leftToRight(self):
    """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

def autoscroll(self):
    """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

def write4bits(self, bits, char_mode=False):
    """ Send command to LCD """
        self.delayMicroseconds(1000)  # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
    for i in range(4):
        if bits[i] == "1":
            self.GPIO.output(self.pins_db[::-1][i], True)
        self.pulseEnable()
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4, 8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)
self.pulseEnable()
    
    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)  # divide microseconds by 1 million for seconds
        sleep(seconds)
    
    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)       # commands need > 37us to settle
    
    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0)  # next line
            else:
                self.write4bits(ord(char), True)


def light():
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light_pin,GPIO.OUT)
    GPIO.output(light_pin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.cleanup(light_pin)


def music():
    os.system('omxplayer TNT.mp3 &')


def pir():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
    previous_state = False
    current_state = False
    #while True:
        time.sleep(0.1)
        previous_state = current_state
        current_state = GPIO.input(sensor)
        if current_state != previous_state:
            new_state = "HIGH" if current_state else "LOW"
            print("GPIO pin %s is %s" % (sensor, new_state))


def servo():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 100)
    pwm.start(5)

    class App:
    
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            scale = Scale(frame, from_=0, to=180,
                      orient=HORIZONTAL, command=self.update)
            scale.grid(row=0)
    
        def update(self, angle):
            duty = float(angle) / 10.0 + 2.5
            pwm.ChangeDutyCycle(duty)

    root = Tk()
    root.wm_title('Servo Control')
    app = App(root)
    root.geometry("200x50+0+0")
    root.mainloop()


def keypad():

    GPIO.setmode(GPIO.BOARD)

    for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j],1)

    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)


    #function that read the input
    def read(num): #Parameter num is the number of inputs necessary.
        try:
            passcode = ""
            while(num):
                for j in range(4):
                    GPIO.output(COL[j],0)
                    
                    for i in range(4):
                        if GPIO.input(ROW[i]) == 0:
                            
                            passcode += str(MATRIX[i][j])#append the key pressed on the keypad
                            num -= 1
                            while(GPIO.input(ROW[i]) == 0):
                                pass
                
                GPIO.output(COL[j],1)
        
            return passcode

        except KeyboardInterrupt:
            GPIO.cleanup()




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




#Function that create the logs inside the archive.
def log_start(alarm):
    
    if alarm :
        logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' Event with the alarm system on.')
        else :
            logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' Record from motion detection with the alarm off.')
        
        return datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


#Function that close the logs inside the archive.
def log_finish(date_time):
    logging.warning(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + ' End of the event started at '+ date_time)


if __name__ == '__main__':
    lcd = Adafruit_CharLCD()
    lcd.clear()
    lcd.message("  Adafruit 16x2\n  Standard LCD")







