import schedule
import time

def job():
    print("I'm working...")

if __name__=="__main__":
    while True:
        schedule.run_pending()
        schedule.every(10).seconds.at(":00").do(job)
        time.sleep(1)