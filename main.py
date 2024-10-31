
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                #              Importing necessary libraries                  #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from machine import Pin, PWM, ADC
from gpio_lcd import GpioLcd
from time import sleep, ticks_diff, ticks_ms
import time



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

program = 1 


              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
              #                        Main Function                        #
              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Generating a 1 or a 2 from the dial to be used for imperial or metric units, respectively
def FindProgram(AValue):
    # Using placeholder varaible x for calculations
    x = AValue/33000 # Giving a value 0-1
    units = int(x+1) # Adding 1 so the value is 1-2
    
    return units
    

lcd.putstr("Program:")

lcd.move_to(2,1)
lcd.putstr("Push to run")


while True:
    
    # Logic to take place when the button gets pressed
    if reset_button.value() == 0:
        if program == 1:
            # Running the bike program
            import bike_spedometer
        elif program == 2:
            # Running the pizza cutter program
            import pizza_cutter
            
        
        
        
        
    # Read analog input value from the potentiometer
    A = pot.read_u16()
    

    program = FindProgram(A) # Redefining the diameter as long as the dial is turning
    
    if program == 1:
        lcd.move_to(9,0)
        lcd.putstr("Bike ")
    elif program == 2:
        lcd.move_to(9,0)
        lcd.putstr("Pizza")
        
    
    
    
    
    time.sleep(0.1) 

        
        
