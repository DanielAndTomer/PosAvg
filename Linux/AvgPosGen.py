import serial
import time
import re
from datetime import datetime
import sys
import ctypes
from tkinter import messagebox as mb

import threading



f = open("POSAVE LOG.txt", "a")

def ShowDialog(title, text):
    t=threading.Thread(target=mb.showerror, args=(title, text))
    t.start()
    

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
        if char == '\n':
            num+=1
            line += ' '
    ####print ('DEBUG: '+line)
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
    ##print ('DEBUG2: '+line)
    return line

def timeSet(opt, time_value):       #converts to hours and seconds. Return list - [S,H]
    ##print("start AvgPosGen def timeSet")
    #errors setup
    err40_400 = 'Please enter number between 40-40'
    err1_60 = 'Please enter number between 1-60'
    err01_48 = 'Please enter number between 0.1-48'
    
    timeList = []
    if opt == 1:
        try:
            waitTime = float(time_value)
            if 0.1 <= waitTime <= 48:
                flag = 0
            else:
                ShowDialog("Error",err01_48)
        except ValueError:
            ShowDialog("Error",err01_48)
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
                ShowDialog("Error",err1_60)
        except ValueError:
            ShowDialog("Error",err1_60)
            pass
        f.write(str(datetime.now()) + "  " + 'User start pos for ' + str(waitTime) + ' Minutes\n')
        timeInSecs = waitTime * 60  # Convert time in Minutes to seconds
        waitTime = round(waitTime / 60, 2)
        timeList.append(timeInSecs)
        timeList.append(waitTime)
        return timeList
    elif opt == 3:
        try:
            waitTime = float(time_value)
            ##print(waitTime)
            if 40 <= waitTime <= 400:
                flag = 0
            else:
                ShowDialog("Error",err40_400)
        except ValueError:
            ShowDialog("Error",err40_400)
            pass
        f.write(str(datetime.now()) + "  " + 'User start pos for ' + str(waitTime) + ' Seconds\n')
        timeInSecs = waitTime
        waitTime = round(waitTime / 60 / 60, 6)
        timeList.append(timeInSecs)
        timeList.append(waitTime)
        return timeList
    else:
        ShowDialog("Error",'Error when convert time')
        logWrite("  [ERROR]: Error when converting selected time\n")

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
            ShowDialog('Error', 'Connection error - Unable to connect to Novatel.')
            return None  
            return

        time_list = timeSet(opt,time_value)
        time_in_secs=time_list[0]
        waitTime=time_list[1]
        ##print(waitTime)
        c='posave on '+str(waitTime)+' 0.5 0.5'+'\n'
        ser.write(bytes(c, encoding="ascii"))		
        logWrite("  [DEBUG]: "+c)
        getPosaveOK=readValue(ser)
        if '<OK' in getPosaveOK:
            value=getPosaveOK
            logWrite('  [DEBUG]: Msg from Novatel after sending posave on: '+value+'\n')
            time.sleep(time_in_secs + 3) #Wait POS time +5secs for safety, then check if finished.
            ser.write(b'log bestpos\n')
            logWrite('  [DEBUG]: log bestpos\n')
            getOK=readValue(ser)
            if '<OK' in getOK:
                time.sleep(1)
                value=getOK
                logWrite("  [DEBUG] Msg from Novatel after sending log bestpos: "+value+"\n")
                if 'FIXEDPOS' in value:
                    ser.write(b'fix none\n')
                    logWrite('  [DEBUG]: fix none\n')
                    time.sleep(1)
                    getOK=readValueOK(ser)
                    if '<OK' in getOK:
                        splitTillCordinate=value.split("FIXEDPOS ",1)[1] #split until the first cordinate
                        cordinates='fix position '+' '.join(splitTillCordinate.split()[:3])+'\n' #get only 3 first words
                        ser.write(bytes(cordinates, encoding="ascii"))
                        logWrite("  [DEBUG]: "+cordinates)
                        time.sleep(1)
                        getOK=readValueOK(ser)
                        if '<OK' in getOK:
                            ser.write(b'saveconfig\n')
                            logWrite('  [DEBUG]: saveconfig\n')
                            time.sleep(1)
                            getOK=readValueOK(ser)
                            if '<OK' in getOK:
                                logWrite('  [DEBUG]: Finished\n')
                                ser.close()
                                return True
                            else:
                                logWrite('   [ERROR]: Cant send saveconfig to Novatel..\n.')
                                ShowDialog('Error', 'Cant send saveconfig to Novatel..')
                                return
                        else:
                            logWrite('   [ERROR]: Cant send fix position to Novatel..\n.')
                            ShowDialog('Error', 'Cant send fix position to Novatel..')
                            return
                    else:
                        logWrite('   [ERROR]: Something went worng, starting again...\n.')
                        ShowDialog('Error', 'Something went worng, starting again..')
                        return
                else:
                    logWrite('  [ERROR]: Sorry you need to wait some more time.\n')
                    ShowDialog('Error', 'Sorry you need to wait some more time.')
                    return
            else:
                logWrite('  [ERROR]: Unable to log bestpos...\n.')
                ShowDialog('Error', 'Unable to log bestpos...')
                return        	
        else:
            logWrite('  [ERROR]: Failed to send posave on command\n')
            ShowDialog('Error', 'Failed to send posave on command')
            return

        
        logWrite('---------------------------------------------------------------------------------\n')
        ser.close()
        return None
