#This program controls a simple 7-segment display for the raspberry pi.


import RPi.GPIO as GPIO
import time

#********* IO Pinouts
SEG_A = 23
SEG_B = 24
SEG_C = 22
SEG_D = 27
SEG_E = 17
SEG_F = 18
SEG_G = 15
SEG_DP = 10

#optional switch for testing
SW_IN = 14


#********** segment map: 

#     ---A---
#    |       |
#    F       B
#    |       |
#     ---G---
#    |       |
#    E       C
#    |       |
#     ---D---   DP

segList = [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G]

dig0List = [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F]
dig1List = [SEG_B, SEG_C]
dig2List = [SEG_A, SEG_B, SEG_G, SEG_E, SEG_D]
dig3List = [SEG_A, SEG_B, SEG_G, SEG_C, SEG_D]
dig4List = [SEG_F, SEG_G, SEG_B, SEG_C]
dig5List = [SEG_A, SEG_F, SEG_G, SEG_C, SEG_D]
dig6List = [SEG_A, SEG_F, SEG_G, SEG_E, SEG_D, SEG_C]
dig7List = [SEG_A, SEG_B, SEG_C]
dig8List = [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G]
dig9List = [SEG_F, SEG_A, SEG_B, SEG_G, SEG_C, SEG_D]
digAList = [SEG_E, SEG_F, SEG_A, SEG_B, SEG_C, SEG_G]
digBList = [SEG_F, SEG_E, SEG_D, SEG_C, SEG_G]
digCList = [SEG_A, SEG_F, SEG_E, SEG_D]
digDList = [SEG_B, SEG_C, SEG_D, SEG_E, SEG_G]
digEList = [SEG_A, SEG_F, SEG_G, SEG_E, SEG_D]
digFList = [SEG_A, SEG_F, SEG_G, SEG_E]
digGList = [SEG_A, SEG_F, SEG_E, SEG_D, SEG_C]
digHList = [SEG_F, SEG_E, SEG_G, SEG_B, SEG_C]
digIList = [SEG_F, SEG_E]
digJList = [SEG_E, SEG_D, SEG_C, SEG_B]
digLList = [SEG_F, SEG_E, SEG_D]
digOList = [SEG_C, SEG_D, SEG_E, SEG_G]
digPList = [SEG_F, SEG_E, SEG_A, SEG_B, SEG_G]
digRList = [SEG_E, SEG_G]
digSList = [SEG_A, SEG_F, SEG_G, SEG_C, SEG_D]
digUList = [SEG_F, SEG_E, SEG_D, SEG_C, SEG_B]
digYList = [SEG_F, SEG_E, SEG_G, SEG_B]

digDashList = [SEG_G]

digDecList = [dig0List, dig1List, dig2List, dig3List, dig4List, dig5List, dig6List, dig7List, dig8List, dig9List]
digHexList = [dig0List, dig1List, dig2List, dig3List, dig4List, dig5List, dig6List, dig7List, dig8List, dig9List, digAList, digBList, digCList, digDList, digEList, digFList]
digAlfaList = [digAList, digBList, digCList, digDList, digEList, digFList, digGList, digHList, digIList, digJList, digDashList, digLList, digDashList, digDashList, digOList, digPList, digDashList, digRList, digSList, digDashList, digUList, digDashList, digDashList, digDashList, digYList, digDashList]

DEC = 0
HEX = 1 
ALFA = 2

ALFA_OFFSET = ord('a')

maxList = [10, 16, 26]

SEG_ON = GPIO.LOW
SEG_OFF = GPIO.HIGH

GPIO.setmode(GPIO.BCM)

for seg in segList:
    GPIO.setup(seg, GPIO.OUT)
    GPIO.output(seg, SEG_OFF)

GPIO.setup(SEG_DP, GPIO.OUT)
GPIO.output(SEG_DP, SEG_OFF)

#need pull up resistor on switch, otherwise we get unstable results
GPIO.setup(SW_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#*********** API Functions ***************

def allOff():   #turn all segments off
    for seg in segList:
        GPIO.output(seg, SEG_OFF)

def displayDecDigit(digit):   #display a decimal digit
    allOff()
    for seg in digDecList[digit]:
        GPIO.output(seg, SEG_ON)

def displayHexDigit(digit):   #display a hex digit
    allOff()
    for seg in digHexList[digit]:
       GPIO.output(seg, SEG_ON)

def displayAlfaChar(char):    #display an alpha char
    allOff()
    i = ord(char.lower()) - ALFA_OFFSET
    for seg in digAlfaList[i]:
       GPIO.output(seg, SEG_ON)

def displayDpOn():	      #turn on dp
    GPIO.output(SEG_DP, SEG_ON)

def displayDpOff():	      #turn off dp
    GPIO.output(SEG_DP, SEG_OFF)

def displayDash():            #display a dash
    allOff()
    for seg in digDashList:
        GPIO.output(seg, SEG_ON)

def displayDigitTest(digit, dp, mode):   #test utility 
    if mode == HEX:
        displayHexDigit(digit)
    elif mode == ALFA:
	displayAlfaChar(chr(digit + ALFA_OFFSET))
    else:
	displayDecDigit(digit)
    if dp == True:
        GPIO.output(SEG_DP, SEG_ON)
    else:
        GPIO.output(SEG_DP, SEG_OFF)

#******* Main: perform test if running standalone...
if __name__ == "__main__":

    try:
        digit = 0
	dp = False
        mode = DEC
        while 1:
            displayDigitTest(digit, dp, mode)
	    if GPIO.input(SW_IN):
                sw_last = False
            else:
                if sw_last == False:
	           digit += 1
                   if digit >= maxList[mode]:
                       digit = 0
                       if dp == True:
                           dp = False
		           if mode == HEX: mode = ALFA 
                           elif mode == ALFA: mode = DEC
                           else: mode = HEX
                       else:
                           dp = True
                sw_last = True
            time.sleep(0.100)
    except KeyboardInterrupt:
        GPIO.cleanup()
