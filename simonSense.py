"""
Einav Kiderman 205363013
Inbal Carasso Lev 204694111
rules of the game:
The use need to activate the sensor in reaction to the leds pattern given by the game:
blue = fire
green = light
yellow = voice
red = potentiometer
"""
import RPi.GPIO as GPIO
import random
import wiringpi
from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



#Set up the script to use the BCM pin configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(27)

#Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


#number of pin for each part
speaker = 27
blue = 5
green = 6
yellow = 13
red = 19
leds = [blue, green, yellow, red]
sensors = ["fire", "light", "voice", "potentiometer"]
sounds = [440, 880, 20, 1760]

dSounds = dict(zip(leds, sounds))
dSensors = dict(zip(sensors, leds))
#sensor initial values - fire, light, voice, potentiometer
sensorValues = [mcp.read_adc(0), mcp.read_adc(1), mcp.read_adc(2), mcp.read_adc(3)]
listOfcolors = []


for led in leds:
    #set the led pins to output
    GPIO.setup(led, GPIO.OUT)

#light the led and play the sound
def light_led(led):
            GPIO.output(led, GPIO.HIGH)
            wiringpi.softToneWrite(speaker, dSounds[led])
            sleep(0.5)
            wiringpi.softToneWrite(speaker, 0)
            GPIO.output(led, GPIO.LOW)
            sleep(0.5)
            GPIO.output(led, GPIO.LOW)

#adds new color to the pattern for the next turn of the player
def add_color(leds, listOfcolors):
    numOfled = random.randint(0,3)
    listOfcolors.append(leds[numOfled])
   

#play pattern for the player to repeat - the list of colors is a list of the numbers of the pins of the leds
def play_pattern(listOfcolors):
    #go through the current pattern and play it
    for color in listOfcolors:
        light_led(color)

#wait for the player to repeat the notes and check if he did it correct
def vaildate_player_moves(leds, listOfcolors):
    i = 0
    #check if some button was pushed
    while i < len(listOfcolors):
            sensor = check_sensors()
            #if the user activated the wrong sensor
            if not listOfcolors[i] == sensor:
                game_over(leds, listOfcolors)
                return False
            else:
                    i += 1
                    sleep(0.5)

    #if he followed all the colors return true to continue the game
    sleep(0.5)
    return True

def check_sensors():
    
    while True:
        
        #check if the fire sensor value changed
        #the numbers are approximated by the numbers from the channels when we activated the sensors
        fireV = mcp.read_adc(0)
        if fireV < 100:
            print("fire: ", fireV)
            print(dSensors["fire"])
            sleep(0.2)
            return dSensors["fire"]
        #check if the light sensor value changed
        lightV = mcp.read_adc(1)
        if abs(lightV - sensorValues[1] > 100):
            print("light: ", lightV)
            print(dSensors["light"])
            sleep(0.2)
            return dSensors["light"]
        #check if the voice sensor value changed
        voiceV = mcp.read_adc(2)
        if abs(voiceV - sensorValues[2] > 200):
            print("voice: ", voiceV)
            print(dSensors["voice"])
            sleep(0.2)
            return dSensors["voice"]
        #check if the potentiometer sensor value changed
        potentiometerV = mcp.read_adc(3)
        if abs(potentiometerV - sensorValues[3] > 200):
            print("potentiometer: ", potentiometerV)
            print(dSensors["potentiometer"])
            sleep(0.2)
            return dSensors["potentiometer"]
        

#game over case
def game_over(leds, listOfcolors):
    #if the player failed, light all the leds 3 times and make a sound
    for i in range (3):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        wiringpi.softToneWrite(speaker, dSounds[led])
        sleep(1)
        wiringpi.softToneWrite(speaker, 0)
        GPIO.output(leds[0], GPIO.LOW)
        GPIO.output(leds[1], GPIO.LOW)
        GPIO.output(leds[2], GPIO.LOW)
        GPIO.output(leds[3], GPIO.LOW)
        sleep(1)

    print("Game Over! Your score is:", len(listOfcolors)-1)

def play():
   t = True
   while t:
        add_color(leds, listOfcolors)
        play_pattern(listOfcolors)
        t = vaildate_player_moves(leds, listOfcolors)
        


#start game
play()
