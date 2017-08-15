import serial
import time
import re
from datetime import datetime
import sys
f = open("POSAVE LOG.txt", "a")

def logOpen():
    f = open("POSAVE LOG.txt", "a")
    f.write('\n\n---------------------------------------------------------------------------------\n')
    f.write(str(datetime.now()) + "  " + 'Script opened\n\n')
    
def logWrite(msg):
    f = open("POSAVE LOG.txt", "a")  # Make a log file
    f.write(str(datetime.now()) + msg)
    f.close()


def readValue(ser): # Reads Novatel commands
    value=''
    char='0'
    line=''
    num=0
    while (num<6):
        # Read a line and convert it from b'xxx\r\n' to xxx
        char = ser.read().decode('utf-8')
        line += char
        if char == '\r':
            num+=1
            line += ' '
    print ('DEBUG: '+line)
    return line

def readValueOK(ser): # Reads Novatel O.K commands
    value=''
    char='0'
    line=''
    num=0
    while (num<2):
        # Read a line and convert it from b'xxx\r\n' to xxx
        char = ser.read().decode('utf-8')
        line += char
        if char == '\n':
            num+=1
            line += ' '
    print ('DEBUG2: '+line)
    return line

def timeSet(opt, time_value):       #converts to hours and seconds. Return list - [S,H]
    print("start AvgPosGen def timeSet")
    #errors setup
    err40_400 = '\n****************************************\n*** Please enter number between 40-400 ***\n****************************************\n'
    err1_60 = '\n****************************************\n*** Please enter number between 1-60 ***\n****************************************\n'
    err01_48 = '\n****************************************\n*** Please enter number between 0.1-48 ***\n****************************************\n'
    
    timeList = []
    if opt == 1:
        try:
            waitTime = float(time_value)
            if 0.1 <= waitTime <= 48:
                flag = 0
            else:
                print(err01_48)
        except ValueError:
            print(err01_48)
            pass
        f.write(str(datetime.now()) + "  " + 'User start pos for ' + str(waitTime) + ' Hours\n')
        timeInSecs = (waitTime * 60) * 60  # Convert time in Hours to seconds
        timeList.append(timeInSecs)
        timeList.append(waitTime)
        return timeList
    elif opt == 2:
        try:
            waitTime = float(time_value)
            if 1 <= waitTime <= 60:
                flag = 0
            else:
                print(err1_60)
        except ValueError:
            print(err1_60)
            pass
        f.write(str(datetime.now()) + "  " + 'User start pos for ' + str(waitTime) + ' Minutes\n')
        timeInSecs = waitTime * 60  # Convert time in Minutes to seconds
        waitTime = round(waitTime / 60, 2)
        timeList.append(timeInSecs)
        timeList.append(waitTime)
        return timeList
    elif opt == 3:
        print ("I'm In 3")
        try:
            waitTime = float(time_value)
            print(waitTime)
            if 40 <= waitTime <= 400:
                flag = 0
            else:
                print(err40_400)
        except ValueError:
            print(err40_400)
            pass
        print("I passed")
        f.write(str(datetime.now()) + "  " + 'User start pos for ' + str(waitTime) + ' Seconds\n')
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        timeInSecs = waitTime
        waitTime = round(waitTime / 60 / 60, 6)
        timeList.append(timeInSecs)
        timeList.append(waitTime)
        print (timeList)
        return timeList
    else:
        print('not good')

def start_pos(opt,time_value,COM):

    logWrite("  [DEBUG]: Values has been past to the script.\n") # DEBUG MASSEGE
    
    with serial.Serial() as ser:

        ser.baudrate = 115200
        ser.port = COM
        try:
            ser.open()
            logWrite("  [DEBUG]: Connected to Novatel.\n") # DEBUG MASSEGE
        except Exception:
            logWrite("  [ERROR]: Connection error - Unable to connect to Novatel.\n") # DEBUG MASSEGE
            return None
            

        time_list = timeSet(opt,time_value)
        time_in_secs=time_list[0]
        waitTime=time_list[1]
        print(waitTime)

        c='posave on '+str(waitTime)+' 0.5 0.5'+'\n'
        logWrite("  [DEBUG]: "+c)
        ser.write(bytes(c, encoding="ascii"))
        #time.sleep(time_in_secs + 1) #Wait POS time then check if finished
        ser.write(b'log bestpos\n')
        time.sleep(3)
        logWrite('  [DEBUG]: log bestpos\n')
        getOK=readValueOK(ser)
        if '<OK' in getOK:
            time.sleep(1)
            value=readValue(ser)
            logWrite("  [DEBUG]: "+value+"\n")
            if 'FIXEDPOS' in value:
               ser.write(b'fix none\n')
               time.sleep(1)
               dd=value.split("FIXEDPOS ",1)[1] #split until the first cordinate
               cordinates='fix position '+' '.join(dd.split()[:3])+'\n' #get only 3 first words
               getOK=readValueOK(ser)
               print (str(getOK))
               if '<OK' in getOK:
                   ser.write(bytes(cordinates, encoding="ascii"))
                   logWrite("    [DEBUG]:"+cordinates)
                   time.sleep(1)
                   ser.write(b'saveconfig\n')
                   logWrite('    [DEBUG]: saveconfig\n')
                   logWrite('    [DEBUG]: Finished\n')
               else:
                   logWrite('    [WARRNING]: Something went worng, starting again...\n.')
            else:
                logWrite('    [WARRNING]: Sorry you need to wait some more time.')

        else:
            logWrite('    [ERROR]: unable log bestpos...\n.')
            return
        

        logWrite('---------------------------------------------------------------------------------\n')
        ser.close()
