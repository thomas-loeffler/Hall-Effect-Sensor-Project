
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #              Importing necessary libraries                  #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from machine import Pin, PWM, ADC
from gpio_lcd import GpioLcd
from time import sleep, ticks_diff, ticks_ms
import time
import bike_functions as f


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
              #                      Pin Initialization                     #
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
              #                   Variable Initialization                   #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Initializing the variables to be used in calculations in and out of the main program so they are global

distance = 0 # Starting the distance travelled as 0
Tinitial = time.ticks_ms() # Defining an inital time to be used for period calculations
periodMS = 0 # Defining the initial period to be 0
Ainitial = pot.read_u16() # Defining the initial analog input value for detecting changes
                          # pot.read_u16 is a number between 65,535 and 0                                      
diameter = f.FindDiameter(Ainitial) # Turning the analog input number into a number 12-30
ATimeCount = 0 # Variable used for displaying the wheel size from potentiometer
speed = 0 #initializing the speed as 0

test = False # Varaible definfing what mode we are operating in
             # True = Test mode, False = Normal mode

SpeedDelay = 120 # Variable used in a delay loop for controlling when speed is updated,
                 # and resetting speed to 0 after a certain amount of time with no motion

SensorCount = 0 # Another counting varable for detecting if the speed is above 0

x = SensorCount # Comparison varaible used in resetting the speed to 0 after a certain amount of time with no motion

# Calling the initialization function
f.StartUp(test)


              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                        Main Function                        #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

while True:
    # Resetting the analog time counter to 0 for counting
    ATimeCount = 0
    
    # Logic to take place when the button gets pressed
    if reset_button.value() == 0:
        # Clearing the screen and diplaying "RESETTING TRIP" for 2 seconds
        lcd.clear()
        lcd.move_to(4, 0)  
        lcd.putstr("RESETTING")
        lcd.move_to(6, 1)  
        lcd.putstr("TRIP")
        time.sleep(2)
        
        # Resetting the display back to the main screen depending on the operating mode
        distance = 0
        periodMS = 0
        
        if test == True:
            f.TestScreen()
        else:
            f.RunningScreen(distance)
        
        # Resetting the speed and distance to 0
        distance = 0
        periodMS = 0
        
        
        
    # Read analog input value from the potentiometer, 528-65535 across voltage range 0.01V - 3.3V (potentiometer limitation)
    Acurrent = pot.read_u16()
    
    # Dipsplaying the analog input if it is changed
    if abs(Acurrent - Ainitial) > 3000: # Detecting a change larger than a small bump of the dial
        
        diameter = f.FindDiameter(Acurrent) # Defining the diameter of the wheel using the analog input
        # Clearing the screen and displaying the diameter selected when the dial is turned
        lcd.clear()
        lcd.move_to(0, 0)  
        lcd.putstr("Wheel Diameter:")
        lcd.move_to(4, 1)
        lcd.putstr(str(diameter))
        lcd.move_to(9, 1)
        lcd.putstr("in")
        
        # Jumping into a loop that will keep displaying the analog input
        # until it hasn't changed significantly for ~5 seconds
        while True:
            Ainitial = Acurrent
            Acurrent = pot.read_u16() # Gives a value between 528 and 65535 (potentiometer limitation)
            diameter = f.FindDiameter(Acurrent) # Redefining the diameter as long as the dial is turning
            lcd.move_to(4, 1)
            lcd.putstr(str(diameter)) # Displaying the diameter
            time.sleep(.15) # Delay so that the value isnt read every millisecond
            # Creating a counter that increments if the value has not changed in .2 seconds
            if abs(Acurrent - Ainitial) < 3000: 
                ATimeCount = ATimeCount+1
            if ATimeCount > 25:
                break # Once the analog input hasn't chnaged for ~5 seconds, the loop breaks
            
        #resetting the display to the main screen
        if test == True:
            f.TestScreen()
        else:
            f.RunningScreen(distance)
     
            
    
    
   
    # Read the state of the Hall effect sensor
    if hall_sensor_pin.value() == 0:# Low signal (magnet detected)
        SensorCount = SensorCount+1  # Counting varaible used for determining if the bike is moving
                                     # without calling the speed funciton
        
        Tnew = time.ticks_ms() # Gets the number of milliseconds since the system was started
        periodMS = Tnew - Tinitial # Finds the time since the last sensor trigger (period in ms)
        
        Tinitial = Tnew # Resetting Tinitial to now, to be compared at next trigger
        
        distance = int(distance + diameter) # Incrementing the distance in inches
        
        while hall_sensor_pin.value() == 0:
            pass # Creating a latch so that the varaibles are not changed while the sensor is triggered
            
            
    
    
    # Updating the display, passing the new diameter, distance, period between sensor triggers, and SpeedDelay varaible        
    if test == True:
        f.TestUpdate(distance, periodMS)
    else:
        f.RunningUpdate(distance, periodMS, SpeedDelay, diameter)
    
    
    
    if (SpeedDelay > 120):
        SpeedDelay = 0
        x = SensorCount
        
    if (SensorCount > 1000):
        SensorCount = 0
    
    # Logic that checks every 120 cycles if the sensor count has changed(if the bike isn't moving)
    # And resets the speed to 0, since it doesnt on its own
    if (SpeedDelay == 120 and x-SensorCount == 0):
        x = SensorCount
        periodMS = 0
        SpeedDelay = 0
        
    SpeedDelay = SpeedDelay+1 # Incrementing the speed delay varaible once per full cycle
    
    
    time.sleep(0.01) 

        
        