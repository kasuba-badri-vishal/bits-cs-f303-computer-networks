import os
import subprocess

def mainmenu():
    print("-"*80)
    print("\t\t\t NMAP SECURITY SCANNER")
    print("-"*80)
    print()
    print("\t\t\t1---> Host Discovery")
    print()
    Host_Discovery()
    quit_program()

def Host_Discovery():
    host = input("[*]Please enter Host address to Scan : ")
    print("-"*80)
    subprocess.check_call(['nmap','-n','-v','-Pn','-sn','-sL','-PE','-PP','-oN','HostDiscovery.txt',host])
    print("-"*80)

def clear():
    os.system('cls||clear')

def quit_program():
    quit()

if __name__ == "__main__":
    mainmenu()