import serial
import matplotlib.pyplot as plt
import numpy as np

a = 1
ser = serial.Serial('/dev/ttyS1', 9600)

#arduino.close()

if(ser.isOpen()):
    print("a")
    ser.write(9)
while True:
    print("b")
    ser.flushInput()

    plot_window = 20
    y_var = np.array(np.zeros([plot_window]))

    plt.ion()
    fig, ax = plt.subplots(constrained_layout=True)
    line, = ax.plot(y_var)
    print("c")
    try:
        ser_bytes = ser.readline()
        print("d")
        try:
            print("e")
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            print(decoded_bytes)
            if decoded_bytes == 504:  #eeh
                break
        except:
            continue
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([time.time(),decoded_bytes])
        y_var = np.append(y_var,decoded_bytes)
        y_var = y_var[1:plot_window+1]
        line.set_ydata(y_var)
        ax.relim()
        #ax.set_ylim(510)
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        print("Keyboard Interrupt")
        break
    #exec(open('fin.py').read())