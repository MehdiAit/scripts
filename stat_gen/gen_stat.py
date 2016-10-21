import os
from time import gmtime, strftime
import argparse
import csv
import statistics
import matplotlib.pyplot as plt

from glob import glob

def get_args():
    parser = argparse.ArgumentParser(description='Some stats about something ...')
    parser.add_argument('-p', '--path', type=str, default=None, required=True, help="Path to the dir the anlayse")
    parser.add_argument('--mean', action="store_true", help="Simple view of detected code smells")
    parser.add_argument('-v', '--voltage', type=float, default=3.8, help="Set the phone voltage")
    parser.add_argument('-s', '--split', type=float, default=0.0, help="Strat the computation on the csv files from the split input")
    parser.add_argument('-g','--plot', type=int, help="Generat the plot representation of a csv file")
    return parser.parse_args()

def plot_gen(data):
    print("Plot generation for file ....")
    x_time = [float(tmp[0]) for tmp in data]
    y_amp  = [float(tmp[1]) for tmp in data]
    plt.plot(x_time, y_amp)
    plt.show()

def main():
    args = get_args()

    global_amp_mean = []
    global_time_mean = []
    data_for_plot = []

    # Set the voltage of the study phone
    phone_voltage = args.voltage
    split_time = args.split
    gen_plot = args.plot

    for dir_file in glob(args.path + "/*.csv"):
        with open(dir_file, "r") as csv_file:
            if split_time:
                print(" ***** SPLIT OPTION ON *****")
                data = [tmp for tmp in csv.reader(csv_file) if float(tmp[0]) > split_time]
            else:
                data = [tmp for tmp in csv.reader(csv_file)]

            if gen_plot:
                if gen_plot == int(dir_file.split('/')[-1].split('_')[-1].split('.')[0]):
                    print("Plot process will be done on :" + dir_file)
                    data_for_plot = list(data)

            amp = [float(tmp[1]) for tmp in data]
            exec_time = [float(tmp[0]) for tmp in data][-1]
            amp_mean = statistics.mean(amp)

            print(dir_file.split("/")[-1])
            print("Median Amp : {0} mA".format(amp_mean))
            print("Execution time : {0}s".format(exec_time - split_time))

            global_amp_mean.append(amp_mean)
            global_time_mean.append(exec_time - split_time)

    all_mean_amp = statistics.mean(global_amp_mean)
    all_mean_time = statistics.mean(global_time_mean)

    print(dir_file.split("/")[-2])
    print("GLOBAL --- MEAN Amp : {0} mA".format(all_mean_amp))
    print("GLOBAL --- MEAN Execution time : {0}s".format(all_mean_time))
    print("PHONE VOLTAGE --- {0} V \n".format(phone_voltage))

    global_energy = []

    for i in range(0, len(global_amp_mean)):
        energy = phone_voltage * (global_amp_mean[i]/1000) * global_time_mean[i]
        global_energy.append(energy)

    print("*******************************************************************")    
    print("GLOBAL ENERGY --- {0} (J)\n".format(statistics.mean(global_energy)))

    if gen_plot:
        plot_gen(data_for_plot)

if __name__ == '__main__':
    main()
