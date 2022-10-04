##to DO
#predkosci
#mapa urzadzen
#otwarte porty
#packet loss

import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import signal
import random
import socket


DEFAULT_PING_ADDRES = "8.8.8.8"
LOCAL_HOST = "LOCALHOST"

def main():
    #pingHost(DEFAULT_PING_ADDRES, 0.5)
    IpMacs = getDevicesInNetwork()
    DefaultGateway = IpMacs[0][0]
    tracertHost(DefaultGateway)
    #Mask = getMask()
    #IpHostnameDict = getIpHostnameDict(IpMacs)    
    print("Closed correctly")

def tracertHost(hostname):
    try:
        respond = subprocess.check_output("tracert " + hostname, shell=False)
        respond = respond.decode("ascii", errors="ignore")
        print(respond)
    except:
        print("tracert timed out.")

def pingHost(hostname, frequency):

    try:
        respond = str(subprocess.check_output("ping " + hostname + " -n 1", shell=False))
    except:
            print("Request timed out.")
            return

    # to run GUI event loop
    plt.ion()

    #create array of ping values for one minute depending 
    #on the frequency and set them all to 0
    measures = np.zeros(round(60/frequency))

    #create x values for one min
    x = np.zeros(round(60/frequency))

    #set the steps to 60/frequency
    for i in range(x.size):
        x[i] = i * frequency 

    # here we are creating sub plots
    figure = plt.figure("Ping Graph. Host: " + hostname)
    ax = figure.add_subplot(111)
    line, = ax.plot(x, measures)
    ax.set_ylim([0, 50])

    # naming the x axis
    plt.xlabel('Time in s')
    # naming the y axis
    plt.ylabel('Ping in ms')

    # giving a title to my graph
    plt.title('Ping Graph. Host: ' + hostname)

    while(True):
        if not plt.get_fignums():
            break

        #get current ping value
        try:
            respond = str(subprocess.check_output("ping " + hostname + " -n 1", shell=False))
        except:
            print("Request timed out.")
            plt.close()
            return

        #add a new measurement as the first element
        measures = np.insert(measures, 0, getPingFromRespond(respond))

        #remove the las (the oldest) element
        measures = np.delete(measures, -1)

        #make sure the data fits to the plot
        ax.set_ylim([0, max(measures) + 50 - max(measures)%50])

        #update x and y data
        line.set_ydata(measures)

        # drawing updated values
        figure.canvas.draw()

        # This will run the GUI even
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()

        time.sleep(frequency)
        

def getPingFromRespond(respond):
    #filter out the ping from the string and return it as an int
    respond = respond[respond.index("time=") + 5:respond.index("ms")]
    return int(respond)


def getDevicesInNetwork():
    output = []
    respond = subprocess.check_output("arp -a", shell=False)
    respond = respond.decode("ascii", errors="ignore")

    for line in respond.splitlines():
        if("dynamic" in line):
            temp = removeMultipleSpaces(line).split(" ")
            output.append([temp[1], temp[2]])

    return output

def getMask():
    output = []
    respond = subprocess.check_output("ipconfig", shell=False)
    respond = respond.decode("ascii", errors="ignore")
    for line in respond.splitlines():
        if("Mask" in line):
            output.append(line[line.index(":") + 2:])
    
    if("255.255.255.0" in output):
        return "255.255.255.0"
    return output        

def getIpHostnameDict(IpMacs):
    output = {}
    for ip in IpMacs:
        try:
            respond = socket.gethostbyaddr(ip[0])
            output[respond[0]] = respond[2][0]
        except:
            print("Failed for " + ip[0])
            continue
    return output

def removeMultipleSpaces(string):
    output = ""
    for s in range(len(string) - 1):
        if(string[s] == ' ' and string[s+1] == ' '):
            continue

        output += string[s]
    return output

#close the program on keyboard interrupt
def keyboardInterruptHandler(signum, frame):
    exit(1)

#add the signal
signal.signal(signal.SIGINT, keyboardInterruptHandler)

if __name__ == "__main__":
    main()
