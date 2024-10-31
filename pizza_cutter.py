
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #              Importing necessary libraries                  #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from machine import Pin, PWM, ADC
from gpio_lcd import GpioLcd
import pizza_functions as f
from time import sleep
import time
import math


                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #                    Creating LCD object                      #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)



              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                      Pin initialization                     #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Setting up the hall effect sensor with a pull up resistor on GPIO pin 15
# Whenever the sensor gets triggered, the pin will get grounded
hall_sensor_pin = Pin(15, Pin.IN, Pin.PULL_UP)

# Setting up the button with a pull up resistor on GPIO pin 14
# Whenver the button gets pressed, the pin will get grounded
reset_button = Pin(14, Pin.IN, Pin.PULL_UP)

# Setting up a PWM pin for the LCD display on GPIO pin 13 the the LCD screen
# The LCD screed needs a contrast pin that is an analog voltage
# This PWM pin generates a 3.3V, 50% duty cycle PWM signal at 2kHz for a effecive voltage of 1.65V
pwm_pin = PWM(Pin(13))
pwm_pin.freq(1000)
pwm_pin.duty_u16(int(65535 * 0.4))  # 16-bit PWM scale

# Setting up the analog input pin from the potentiometer
# This voltage (0-3.3) will determine the diameter of the bike wheel
# and control the speed and distance calculations
pot = ADC(Pin(26))



              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                   Variable initialization                   #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Initializing the variables to be used in calculations in and out of the main program so they are global

Ainitial = pot.read_u16() # Defining the initial analog input value of the potentiometer for detecting changes
units = f.FindUnits(Ainitial) # Defining the units before the program starts, based on the potentiometer

SensorCount = 0 # Variable used for the number of times the sensor has been triggered
flash = 0 # Variable used for counting in a loop, determining when the measuring menu flashes
distance = 0 # Initializing the distance as zero for the diplay functions



              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                      Initialization code                    #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

f.StartUp() # Call the start up screen

# Initializing the main menu with proper units
f.MainMenu(units, SensorCount)
    
    
    
    
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                         Running code                        #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

while True:
    
    # Resetting the analog time counter to 0 for counting
    ATimeCount = 0
    # Resetting the flashing time counter to 0 for counting
    flash = 0
    
    # Logic to execute once the button is pressed
    if reset_button.value() == 0:
        sleep(.75)
        # If the button is still pressed after .75 seconds, the measuring function will proceed
        # But if the button is not still pressed after .75 seconds (it was a tap and not a hold),
        # then the reset function will proceed. See below.
        if reset_button.value() == 0:
            lcd.move_to(0, 0) 
            lcd.putstr("Measuring...    ")
            
            # Turning on the flashing cursor and putting it in the right spot
            f.PutCursor(distance, units)
            
            # Creating a while loop to update the distance and flash the measuring line
            while reset_button.value() == 0:
                
                # Creating a flash variable that increments for each while loop cycle
                # and using it to count for displaying the flashing "Measuring..."
                flash = flash + 1
                if (flash % 30000 == 0):
                    lcd.move_to(0, 0) 
                    lcd.putstr("Measuring...    ")
                    # Resetting the cursor to its origional position
                    f.PutCursor(distance, units)
                elif flash % 15000 == 0:
                    lcd.move_to(0, 0) 
                    lcd.putstr("                ")
                    # Resetting the cursor to its origional position
                    f.PutCursor(distance, units)
                
                # Read the state of the Hall effect sensor
                if hall_sensor_pin.value() == 0:# Low signal (magnet detected)
                    SensorCount = SensorCount+1  # Incrementing the amount of times the sensor has tripped for distance calculations
                    
                    # Turning off the cursor and, and updating the distance
                    lcd.hide_cursor()
                    lcd.blink_cursor_off()
                    if units == 1:
                        distance = f.ImperialDistance(SensorCount)
                    elif units == 2:
                        distance = f.MetricDistance(SensorCount)
                    
                    # Resetting the cursor
                    f.PutCursor(distance, units)
                    
                    while hall_sensor_pin.value() == 0:
                        pass # Creating a latch so that the varaibles are not changed while the sensor is triggered
            
            # When the button is not pressed anymore, the main menu in reset
            f.MainMenu(units, SensorCount)
        
        # If the button is only tapped and not held, this triggers the reset code below,
        # resetting the distance and going back to the main menu
        else:
            SensorCount = 0
            lcd.clear()
            lcd.move_to(2, 0) 
            lcd.putstr("Measurement")
            lcd.move_to(5, 1) 
            lcd.putstr("Reset")
            
            sleep(2)
        
        # Diplaying the main menu
        f.MainMenu(units, SensorCount)
        
        
    # rereading the analog input from the microcontroller looking for changes
    Acurrent = pot.read_u16()
    
    # Dipsplaying the analog input if it is changed
    if abs(Acurrent - Ainitial) > 3000: # Detecting a change larger than a small bump of the dial
        units = f.FindUnits(Acurrent) # Setting units using the analog input
        
        # Clearing the screen and displaying the units when the dial is turned
        lcd.clear()
        lcd.move_to(5, 0)  
        lcd.putstr("Units:")
        if units == 1:
            lcd.move_to(0, 1)
            lcd.putstr("Imperial (ft,in)")
        elif units == 2:
            lcd.move_to(1, 1)
            lcd.putstr("Metric (ft,in)")
        
        # Jumping into a loop that will keep displaying the analog input
        # until it hasn't changed significantly for ~5 seconds
        while True:
            Ainitial = Acurrent # Resetting Ainitial so a change can be detected in the future
            Acurrent = pot.read_u16() # Gives a value between 528 and 65535 (potentiometer limitation)
            units = f.FindUnits(Acurrent) # Redefining the units as long as the dial is turning
            
            # Updating the units every .15 seconds
            if units == 1:
                lcd.move_to(0, 1)
                lcd.putstr("Imperial (ft,in)")
            elif units == 2:
                lcd.move_to(0, 1)
                lcd.putstr(" Metric (m,cm)  ")
            time.sleep(.15)
            
            # Creating a counter that increments if the value has not changed in .2 seconds
            if abs(Acurrent - Ainitial) < 1500: 
                ATimeCount = ATimeCount+1
            if ATimeCount > 25:
                break # Once the analog input hasn't chnaged for ~5 seconds, the loop breaks
        
        # Reverting back to the main menu screen
        f.MainMenu(units, SensorCount)
        

    