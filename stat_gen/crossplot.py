import os
from time import gmtime, strftime
import argparse
import csv
import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from glob import glob

def get_args():
    parser = argparse.ArgumentParser(description='Some stats about something ...')
    parser.add_argument('-p', '--plot1', type=str, default=None, required=True, help="Path to the dir the anlayse")
    parser.add_argument('-t', '--plot2', type=str, default=None, required=True, help="Path to the dir the anlayse")

    parser.add_argument('-v', '--voltage', type=float, default=3.8, help="Set the phone voltage")
    parser.add_argument('-g','--graph1', type=int, help="Generat the plot representation of a csv file")
    parser.add_argument('-z','--graph2', type=int, help="Generat the plot representation of a csv file")
    return parser.parse_args()

def plot_gen(data, data2):
    print("Plot generation for file ....")
    x_time = [float(tmp[0]) for tmp in data]
    y_amp  = [float(tmp[1]) for tmp in data]
    
    x2_time = [float(tmp[0]) for tmp in data2]
    y2_amp  = [float(tmp[1]) for tmp in data2]

    blue_patch = mpatches.Patch(color='blue', label='Ring' )
    red_patch  = mpatches.Patch(color='red' , label='Skype')

    # plt.plot(x_time, y_amp, 'b', x2_time, y2_amp, 'r')

    line, line2 = plt.plot(x_time, y_amp, 'b'), plt.plot(x2_time, y2_amp, 'r')
    plt.annotate('placeCall()', xy=(72, 130), xytext=(65.5, 1100), arrowprops=dict(arrowstyle='|-|', facecolor='black'),)
    plt.annotate('createOutgoingCall()' , xy=(90, 130), xytext=(76.5, 1000), arrowprops=dict(arrowstyle='|-|', facecolor='black'),)

    # ax.set_ylim(-2,2)

    plt.legend(handles=[blue_patch,red_patch])
    plt.show()

def main():
    args = get_args()

    data_for_plot = []
    data_for_plot_skype = []

    # Set the voltage of the study phone
    phone_voltage = args.voltage
    gen_plot = args.graph1
    gen_plot2 = args.graph2

    for dir_file in glob(args.plot1 + "/*.csv"):
        with open(dir_file, "r") as csv_file:
            data = [tmp for tmp in csv.reader(csv_file) if float(tmp[0]) > 65]

            if gen_plot:
                if gen_plot == int(dir_file.split('/')[-1].split('_')[-1].split('.')[0]):
                    print("Plot process will be done on :" + dir_file)
                    data_for_plot = list(data)

            amp = [float(tmp[1]) for tmp in data]
            exec_time = [float(tmp[0]) for tmp in data][-1]
            amp_mean = statistics.mean(amp)

            print(dir_file.split("/")[-1])
            print("Median Amp : {0} mA".format(amp_mean))
            print("Execution time : {0}s".format(exec_time - 65))


    for dir_file in glob(args.plot2 + "/*.csv"):
        with open(dir_file, "r") as csv_file:
            data = [tmp for tmp in csv.reader(csv_file) if float(tmp[0]) > 70 ]

            if gen_plot2:
                if gen_plot2 == int(dir_file.split('/')[-1].split('_')[-1].split('.')[0]):
                    print("Plot process will be done on :" + dir_file)
                    data_for_plot_skype = list(data)

            amp = [float(tmp[1]) for tmp in data]
            exec_time = [float(tmp[0]) for tmp in data][-1]
            amp_mean = statistics.mean(amp)

            print(dir_file.split("/")[-1])
            print("Median Amp : {0} mA".format(amp_mean))
            print("Execution time : {0}s".format(exec_time - 70))

    if gen_plot:
        plot_gen(data_for_plot, data_for_plot_skype)

if __name__ == '__main__':
    main()
