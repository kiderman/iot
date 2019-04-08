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
wiringpi.softToneCreate(24)

#number of pin for each part
speaker = 24
blue = 5
green = 6
yellow = 13
red = 19
leds = [blue, green, yellow, red]
buttons = [25, 12, 16, 21]
sounds = [440, 880, 20, 1760]
dSounds = dict(zip(leds, sounds))
dButtons = dict(zip(leds, buttons))
listOfcolors = []


for button in buttons:
    #set the button pins to input with a pull up resistor
    GPIO.setup(button,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
for led in leds:
    #set the led pins to output
    GPIO.setup(led, GPIO.OUT)





#when button pressed light the led and play the sound
def button_light_led(led):
        buttonState = GPIO.input(dButtons[led])
        if(not buttonState):
            GPIO.output(led, GPIO.HIGH)
            wiringpi.softToneWrite(speaker, dSounds[led])
            sleep(1)
            wiringpi.softToneWrite(speaker, 0)
            GPIO.output(led, GPIO.LOW)
        else:
            GPIO.output(led, GPIO.LOW)

#adds new color to the pattern for the next turn of the player
def add_color(leds, listOfcolors):
    numOfled = random.randint(0,3)
    listOfcolors.append(leds[numOfled])
    print(listOfcolors)

#play pattern for the player to repeat - the list of colors is a list of the numbers of the pins of the leds
def play_pattern(listOfcolors):
    #go through the current pattern and play it
    for color in listOfcolors:
        button_light_led(color)

#wait for the player to repeat the notes and check if he did it correct
def vaildate_player_moves(leds, listOfcolors):
    print("validate", listOfcolors)
    i = 0
    #check if some button was pushed
    while (i < len(listOfcolors)):
        for led in leds:
            print(led)
            print(dButtons[led])
            current = (GPIO.input(dButtons[led]) == GPIO.HIGH)
            if current:
                print("True")
            #if the user clicked the wrong button
                if (not listOfcolors[i] == current):
                    game_over(leds, listOfcolors)
                    return False
                else:
                        i += 1
                        sleep(1)

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
        wiringpi.softToneWrite(speaker, dSounds[led])
        sleep(1)
        wiringpi.softToneWrite(speaker, 0)
        GPIO.output(leds[0], GPIO.LOW)
        GPIO.output(leds[1], GPIO.LOW)
        GPIO.output(leds[2], GPIO.LOW)
        GPIO.output(leds[3], GPIO.LOW)

    print("Game Over! Your score is:", len(listOfcolors))

def play():
   t = True
   while t:
        add_color(leds, listOfcolors)
        play_pattern(listOfcolors)
        t = vaildate_player_moves(leds, listOfcolors)


#start game
play()
