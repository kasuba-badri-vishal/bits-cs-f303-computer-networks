import csv
import subprocess
import re
import matplotlib.pyplot as plt
import argparse
import time
# from datetime import datetime as dt

parser = argparse.ArgumentParser(description="Tracking hosts.")
parser.add_argument('-f', type=int, default = 4, \
                     help="number of times network should be probed per hour.")
parser.add_argument('-s', type=int, default=24, help="subnet mask")

def plot_graph():
    x=[]
    y=[]

    with open('output.csv', 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[1])
            y.append(row[0])

    plt.plot(x,y)
    plt.title('Data from the CSV File: No of hosts and Time')
    plt.xlabel('Number of Hosts')
    plt.ylabel('Time')
    plt.show()

def write_output(data):
    # fields = ['Time of Day', 'Number of Hosts']
    filename = "output.csv"

    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

def find_hosts(subnet):
    host = f'172.16.34.0/{subnet}'
    result = subprocess.check_output(['nmap','-sP',host]).decode('utf-8')
    print(result)
    # match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} IST', result)
    cur_time = time.localtime()
    match = f'{cur_time.tm_year}-{cur_time.tm_mon}-{cur_time.tm_mday} {cur_time.tm_hour}:{cur_time.tm_min} IST'
    match2 = re.search(r'[0-9]+ hosts up', result)
    res = []
    res.append(match2.group().split()[0])
    # res.append(match.group())
    res.append(match)
    res.append(subnet)
    return res


if __name__ == "__main__":
    args = parser.parse_args()
    while(True):
        data = find_hosts(args.s)
        print(data)
        write_output(data)
        time.sleep((3600/args.f))
        # plot_graph()