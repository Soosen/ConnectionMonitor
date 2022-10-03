import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import signal


DEFAULT_PING_ADDRES = "8.8.8.8"
LOCAL_HOST = "LOCALHOST"

def main():
    pingHost(DEFAULT_PING_ADDRES, 0.5)
    print("Closed correctly")


def pingHost(hostname, frequency):
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
        respond = str(subprocess.check_output("ping " + hostname + " -n 1", shell=False))

        #add a new measurement as the first element
        measures = np.insert(measures, 0, getPingFromRespond(respond))

        #remove the las (the oldest) element
        measures = np.delete(measures, -1)

        #make sure the data fits to the plot
        ax.set_ylim([0, max(measures) + 50 - max(measures)%50])

        #update x and y data
        line.set_xdata(x)
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


#close the program on keyboard interrupt
def keyboardInterruptHandler(signum, frame):
    exit(1)

#add the signal
signal.signal(signal.SIGINT, keyboardInterruptHandler)

if __name__ == "__main__":
    main()
