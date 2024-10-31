# Importing neccesary libraries
from machine import Pin, PWM, ADC
from gpio_lcd import GpioLcd
from time import sleep
import time
import math


# Creating the LCD object
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)



# Displaying the initial "Power On" messages
def StartUp():
    lcd.move_to(3, 0) 
    lcd.putstr("Power on...")
    time.sleep(2)
    lcd.move_to(4, 1)  
    lcd.putstr("Hello!!")
    time.sleep(2)

    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Have fun")
    lcd.move_to(3, 1)  
    lcd.putstr("measuring!")
    time.sleep(2)
    
    lcd.clear()
    
# Clearing the screen and displaying the main menu
def MainMenu(units, SensorCount):

    lcd.clear()
    lcd.move_to(0, 0) 
    lcd.putstr("Hold to measure ")
    lcd.blink_cursor_off()
    lcd.hide_cursor()
    
    if units == 1:
        distance = ImperialDistance(SensorCount)
    elif units == 2:
        distance = MetricDistance(SensorCount)

    

# Function called while measuring, displaying and blinking the cursor
# right after smallest (in or cm) measurement
def PutCursor(distance, units):
    # Changing cursor placement based on what units are being used
    # and based on the number of digits in the inches or centimeters number
    if units == 1:
        feet = int(distance/12)
        inches = round(distance-(12*feet),1)
        
        if (inches >= 0 and inches < 10):
            lcd.show_cursor()
            lcd.blink_cursor_on()
            lcd.move_to(11, 1)
            
        elif (inches >= 10):
            lcd.show_cursor()
            lcd.blink_cursor_on()
            lcd.move_to(12, 1)
            
            
    elif units == 2:
        meters = int(distance/100)
        centimeters = round(distance-(meters*100),1)
        
        if (centimeters >= 0 and centimeters < 10):
            lcd.show_cursor()
            lcd.blink_cursor_on()
            lcd.move_to(11, 1)
            
        elif (centimeters >= 10):
            lcd.show_cursor()
            lcd.blink_cursor_on()
            lcd.move_to(12, 1)
        
    
        
        
# Function that calculates the distance and updates the display for imperial units
def ImperialDistance(SensorCount):
    # Calculating circumference in inches:
    circumference = 2.16 * math.pi
    distance = circumference/3 * SensorCount # Distance traveled every third rotation (3 magnets on the wheel)
    feet = int(distance/12) 
    inches = round(distance-(12*feet),1) # Finding remaining inches after feet were taken into account
    
    # Displaying feet and inches
    lcd.move_to(2,1)
    lcd.putstr(str(feet))
    
    lcd.move_to(8,1)
    lcd.putstr(str(inches))
    
    # Moving the suffixes (ft,in) based on the number of digita in the diplayed number
    if (feet >= 0 and feet < 10):
        lcd.move_to(4, 1)
        lcd.putstr("ft ")
    elif (feet > 9 and feet < 100):
        lcd.move_to(4, 1)
        lcd.putstr(" ft") # space in there to clear the previous "ft"
    
    if (inches < 10):
        lcd.move_to(11, 1)
        lcd.putstr(" in ")
    elif (inches >= 10):
        lcd.move_to(12, 1)
        lcd.putstr(" in") # space in there to clear the previous "in"
        
    # Returning the distance so it can be used for other functions
    return distance




# Function that calculates the distance and updates the display for metric units
def MetricDistance(SensorCount):
    # Calculating circumference in centimeters:
    circumference = 5.486 * math.pi
    distance = circumference/3 * SensorCount # Distance traveled every third rotation (3 magnets on the wheel)
    meters = int(distance/100)
    centimeters = round(distance-(meters*100),1) # Finding remaining cm after m were taken into account
    
    # Displaying meters and centimeters
    lcd.move_to(2,1)
    lcd.putstr(str(meters))
    
    lcd.move_to(8,1)
    lcd.putstr(str(centimeters))
    
    
    if (meters >= 0 and meters < 10):
        lcd.move_to(4, 1)
        lcd.putstr("m ") # space in there to clear the previous "m"
    elif (meters > 9 and meters < 100):
        lcd.move_to(4, 1)
        lcd.putstr(" m") # " "
    
    if (centimeters < 10):
        lcd.move_to(11, 1)
        lcd.putstr(" cm ") # space in there to clear the previous "cm"
    elif (centimeters >= 10):
        lcd.move_to(12, 1)
        lcd.putstr(" cm") # " "
    
    # Returning the distance so it can be used for other functions
    return distance






# Generating a 1 or a 2 from the dial to be used for imperial or metric units, respectively
def FindUnits(AValue):
    # Using placeholder varaible x for calculations
    x = AValue/33000 # Giving a value 0-1
    units = int(x+1) # Adding 1 so the value is 1-2
    
    return units
    
