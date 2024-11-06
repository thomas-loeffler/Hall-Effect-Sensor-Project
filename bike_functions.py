from machine import Pin, PWM, ADC
from gpio_lcd import GpioLcd
from time import sleep, ticks_diff, ticks_ms
import time

lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)


def StartUp(test):
    # Displaying the initial "Power On" messages
    lcd.move_to(3, 0) 
    lcd.putstr("Power on...")
    time.sleep(2)
    lcd.move_to(4, 1)  
    lcd.putstr("Hello!!")
    time.sleep(2)

    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Have a")
    lcd.move_to(3, 1)  
    lcd.putstr("great ride!")
    time.sleep(2)
    
    distance = 0
    
    if test == True:
        TestScreen()
    else:
        RunningScreen(distance)





def RunningScreen(distance):
    # Displaying the running screen
    lcd.clear()
    lcd.putstr("Distance: ")
    lcd.move_to(0, 1)  
    lcd.putstr("Speed:")
    lcd.move_to(11, 1)  
    lcd.putstr("MPH")
    
    # Moving the inches label depending on the value of the distance
    if (distance < 10):
        lcd.move_to(12, 0)  
        lcd.putstr("in")
    elif (distance < 100 and distance > 9):
        lcd.move_to(12, 0)  
        lcd.putstr(" in")
    elif (distance < 1000 and distance > 99):
        lcd.move_to(13, 0)  
        lcd.putstr(" in")
        
    
    
# All of the functions that have a "test" in their name are ran when the test mode is active
# This mode allows for more data to be displayed on the screen, creating an easier environment for troubleshooting
def TestScreen():
    # Displaying a test screen with more data
    lcd.clear()
    lcd.putstr("D: ")
    lcd.move_to(6, 0)  
    lcd.putstr("ft")
    lcd.move_to(9, 0)  
    lcd.putstr("F:")
    lcd.move_to(0, 1)  
    lcd.putstr("S:")
    lcd.move_to(5, 1)  
    lcd.putstr("fts")
    lcd.move_to(13, 1)  
    lcd.putstr("MPH")
    
    
    
    


def RunningUpdate(distance, periodMS, SpeedDelay, diameter):
    # A function that updates the values on the running screen
    distance = distance/63360 # Converting inches to miles
    
    lcd.move_to(10, 0)  
    lcd.putstr(str(distance))
    
    
    periodS = round(periodMS/1000,3)
    if (periodS > 0):
        freq = round((1/periodS),1)
    else:
        freq = 0
    
    
    
   
    speedFTS = round(freq*(diameter/12),1) # In feet per second
    speedMPH = round(speedFTS*0.681818,1) #mph=ft/s×0.681818
    
    # Updating speed
    if (SpeedDelay%30 == 0):    
        lcd.move_to(7, 1)  
        lcd.putstr(str(speedMPH))
    
        if (speedMPH > 10):
            lcd.move_to(11, 1)  
            lcd.putstr(" MPH")
        else:
            lcd.move_to(10, 1)  
            lcd.putstr(" MPH ")
            
        
    
    
    if (distance < 10):
        lcd.move_to(12, 0)  
        lcd.putstr("mi")
    elif (distance < 100 and distance > 9):
        lcd.move_to(12, 0)  
        lcd.putstr(" mi")
    elif (distance < 1000 and distance > 99):
        lcd.move_to(13, 0)  
        lcd.putstr(" mi")
        




def TestUpdate(distance, periodMS):
    # Updating the values of the test screen
    lcd.move_to(2, 0)  
    lcd.putstr(str(distance))
    
    
    periodS = round(periodMS/1000,3)
    if (periodS > 0):
        freq = round((1/periodS),1)
    else:
        freq = 0
    lcd.move_to(12, 0)  
    lcd.putstr(str(freq))
    
    speedFTS = round(freq*(diameter/12),1) # In feet per second
    speedMPH = round(speedFTS*0.681818,1) #mph=ft/s×0.681818
    
    lcd.move_to(2, 1)  
    lcd.putstr(str(speedFTS))
    
    lcd.move_to(9, 1)  
    lcd.putstr(str(speedMPH))
    
    
    
    
    

def FindDiameter(AValue):
    # Using placeholder varaibles(x,y,z) for calculations
    x = AValue/6553 # Giving a value 0-10
    y = x+18 # Adding 12 so the value is 12-30
    z = int(y*2)/2 # Ensuring the value ends in .0 or .5
    return z







