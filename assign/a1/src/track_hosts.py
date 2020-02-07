import csv
import subprocess
import re
import matplotlib.pyplot as plt
import schedule
import time



def plot_graph():
    x=[]
    y=[]

    with open('output.csv', 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[1])
            y.append(row[0])

    # print(x)
    # print(y)
    # print(type(x))
    # print(type(y))
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

def find_hosts():
    
    host = '172.16.34.0/24'
    result = subprocess.check_output(['nmap','-sP',host]).decode('utf-8')
    print(result)
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} IST', result)
    match2 = re.search(r'\d[0-9]+ hosts up', result)
    res = []
    res.append(match2.group().split()[0])
    res.append(match.group())
    return res


def main():
    data = find_hosts()
    write_output(data)
    plot_graph()

# schedule.every().hour.at(":00").do(main)

if __name__ == "__main__":
    # host = input("Enter the desired subnet : ")
    # freq = input("Enter the desired probing Frequency : ")
  
    while True:
        # schedule.run_pending()
        
        # time.sleep(1)
        main()
  

    