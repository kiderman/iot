"""
Einav Kiderman 205363013
Inbal Carasso 204694111

"""
import RPi.GPIO as GPIO
import random
import wiringpi
from time import sleep

#Set up the script to use the BCM pin configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(26)

#number of pin for each part
speaker = 26
blue = 5
green = 6
yellow = 13
red = 19
leds = [blue, green, yellow, red]
sounds = [440, 880, 20, 1760]
dictionary = dict(zip(leds, sounds))
listOfcolors = []


for led in leds:
    #set the button pins to input with a pull up resistor
    GPIO.setup(leds[led],GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    #set the led pins to output
    GPIO.setup(leds[led], GPIO.OUT)





#when button pressed light the led and play the sound
def button_light_led(led):
        buttonState = GPIO.input(led)
        if(not buttonState):
            GPIO.output(led, GPIO.HIGH)
            wiringpi.softToneWrite(speaker, dictionary[led])
            sleep(1)
            wiringpi.softToneWrite(speaker, 0)
            GPIO.output(led, GPIO.LOW)
        else:
            GPIO.output(led, GPIO.LOW)

#adds new color to the pattern for the next turn of the player
def add_color(leds, listOfcolors):
    numOfled = random.randint(1,5)
    listOfcolors.append(leds[numOfled])

#play pattern for the player to repeat - the list of colors is a list of the numbers of the pins of the leds
def play_pattern(listOfcolors):
    #go through the current pattern and play it
    for color in listOfcolors:
        button_light_led(color)

#wait for the player to repeat the notes and check if he did it correct
def vaildate_player_moves(listOfcolors):
    for color in listOfcolors:
        sleep(5)
        #if the user didn't press the button on time or pressed another button
        if(not GPIO.input(color) == GPIO.HIGH):
            return False

        else:
            button_light_led(color)
    #if he followed all the colors return true to continue the game
    return True

#game over case
def game_over(leds, listOfcolors):
    #if the player failed, light all the leds 3 times and make a sound
    for i in range (3):
        GPIO.output(leds[0], GPIO.HIGH)
        GPIO.output(leds[1], GPIO.HIGH)
        GPIO.output(leds[2], GPIO.HIGH)
        GPIO.output(leds[3], GPIO.HIGH)
        wiringpi.softToneWrite(speaker, dictionary[led])
        sleep(1)
        wiringpi.softToneWrite(speaker, 0)
        GPIO.output(leds[0], GPIO.LOW)
        GPIO.output(leds[1], GPIO.LOW)
        GPIO.output(leds[2], GPIO.LOW)
        GPIO.output(leds[3], GPIO.LOW)

    print("Game Over! Your is:", len(listOfcolors))

def play():

    while True:
        add_color(leds)             #level number 1 - only 1 led is on
        play_pattern(listOfcolors)
        vaildate_player_moves(listOfcolors)


#start game
play()
