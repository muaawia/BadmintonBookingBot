# python3 GymAuto.py "Cardel" "Yoga" "Thursday" "7:30 PM" "mmuaawia@gmail.com" "6134624696" "Mav Arshad"
# python3 GymAuto.py "Cardel" "Badminton - 16+" "Saturday" "7:00 PM" "mmuaawia@gmail.com" "6134624696" "Mav Arshad"
# python3 GymAuto.py "Cardel" "Badminton - 16+" "Saturday" "8:00 PM" "mmuaawia@gmail.com" "6134624696" "Mav Arshad"
#python3 GymAuto.py "Cardel" "Badminton - 16+" "Saturday" "7:00 PM" "mmuaawia@outlook.com" "6138904200" "Ali Arshad"
#python3 GymAuto.py "Cardel" "Badminton - 16+" "Saturday" "8:00 PM" "mmuaawia@outlook.com" "6138904200" "Ali Arshad"
from os import path
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By

Browser = 1
import chromedriver_autoinstaller 
chromedriver_autoinstaller.install()

import sys
import os
import pause
import requests

from fetchcode import fetch_code
from time import sleep
from datetime import datetime
import pytz
from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', 'c834d6ff5b1b44ec320fb418dfcd6b92')
solver = TwoCaptcha(api_key)

password = 'EmailPassword'
imap_url = 'outlook.office365.com'

# Get current time in Eastern timezone
eastern_tz = pytz.timezone('US/Eastern')
current_eastern_time = datetime.now(eastern_tz)

# Get today's date in Eastern timezone
CurrentDay = current_eastern_time.day
CurrentMonth = current_eastern_time.month
CurrentYear = current_eastern_time.year

# Create target time: 6:00 PM Eastern today
target_time_eastern = eastern_tz.localize(datetime(CurrentYear, CurrentMonth, CurrentDay, hour=18, minute=0, second=0))

# Testing
"""
SiteLoc = 'Cardel'
SportType = 'Pickleball - adult'
TargetDate = 'Friday'
TargetTime = '1:45 PM' 
user = 'xxxx@outlook.com'BookPhone = '6130000000'
BookName = 'XXXX XX' 

"""
SiteLoc = sys.argv[1]
SportType = sys.argv[2]
TargetDate = sys.argv[3]
TargetTime = sys.argv[4] 
user = sys.argv[5]
BookPhone = sys.argv[6]
BookName = sys.argv[7]


# Website settings
CardelURL = "https://reservation.frontdesksuite.ca/rcfs/cardelrec/Home/Index?Culture=en&PageId=a10d1358-60a7-46b6-b5e9-5b990594b108&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"
RcSCURL = "https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?Culture=en&PageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"
NePeanURL = "https://reservation.frontdesksuite.ca/rcfs/nepeansportsplex/Home/Index?Culture=en&PageId=b0d362a1-ba36-42ae-b1e0-feefaf43fe4c&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"
EVJamesURL = "https://reservation.frontdesksuite.ca/rcfs/evajamescc/Home/Index?Culture=en&PageId=96907058-93c6-46fd-bead-33729bea33c6&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"

GroupSize = '2'

match SiteLoc:
    case "Cardel":
        CurrentURL = CardelURL
    case "RichCraft":
        CurrentURL = RcSCURL
    case "NepeanSportsPlex":
        CurrentURL = NePeanURL
    case "EVJames":
        CurrentURL = EVJamesURL
    case _:
        print("Site Not Found!")


def slow_type(element, text, delay=0.03):
    """Send a text to an element one character at a time with a delay."""
    count = 0
    for character in text:
        element.send_keys(character)
        # sleep(delay)
        print(count)
        if count < 5:
            print("Sleeping for 0.05 seconds")
            sleep(delay)
        count += 1

def Booking():
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()
    browser = webdriver.Chrome()

    try:
        MainCount = 5
        Confirm = 1
        SleepTime = 0.5
        TypingDelay = 0.05
        UseCapture = 0

        while MainCount and Confirm :
            MainCount = MainCount - 1
            browser.get(CurrentURL)
            sleep(SleepTime)

            browser.get(CurrentURL)
            
            # Wait until exactly 6:00 PM Eastern Time
            print(f"Waiting until 6:00 PM Eastern Time ({target_time_eastern})")
            pause.until(target_time_eastern)
            print("6:00 PM Eastern reached! Starting booking process...")
            # sleep(0.95)
            browser.refresh()
            browser.find_element(By.PARTIAL_LINK_TEXT,SportType).click()
            
            Count = 5
            FindLink = 1
            while FindLink and Count :
                Count = Count - 1
                try:
                    GroupNum = browser.find_element(By.XPATH, '//*[@id="reservationCount"]') 
                    GroupNum.clear()
                    GroupNum.send_keys(GroupSize)
                    browser.find_element(By.XPATH, '//*[@id="submit-btn"]').click()
                    FindLink = 0
                except Exception as e:
                    print(e)
                    if Count == 3 :
                        browser.refresh()
                    sleep(SleepTime/10)
                    print("Link Not Available!")

            Count = 2400 #10 minutes max
            FindLink = 1
            while FindLink and Count :
                Count = Count - 1
                try:
                    browser.find_element(By.PARTIAL_LINK_TEXT,TargetDate).click()
                    FindLink = 0
                except:
                    if (Count % 100) == 0 :
                        browser.refresh()
                    sleep(SleepTime/5)
                    print("Date Not Available!")  

            Count = 10
            FindLink = 1
            while FindLink and Count :
                Count = Count - 1
                try:
                    browser.find_element(By.LINK_TEXT, TargetTime).click()
                    FindLink = 0
                except:
                    sleep(SleepTime/50)

            Count = 10
            FindLink = 1
            while FindLink and Count :
                Count = Count - 1
                try:
                    PhoneBox = browser.find_element(By.XPATH, '//*[@id="telephone"]') 
                    FindLink = 0
                except:
                    sleep(SleepTime/50)

            PhoneBox.clear()
#             PhoneBox.send_keys(BookPhone)
            slow_type(PhoneBox, BookPhone)
            EmailBox = browser.find_element(By.XPATH, '//*[@id="email"]') 
            EmailBox.clear()
            EmailBox.send_keys(user)

            NameBox = browser.find_element(By.XPATH, '//*[@id="mainForm"]/div[2]/div/div[4]/div[1]/label/Input')
            NameBox.clear()
            NameBox.send_keys(BookName)
            # sleep(100000)

            Count = 10
            FindLink = 1
            while FindLink and Count :
                Count = Count - 1
                try:
                    browser.find_element(By.XPATH, '//*[@id="submit-btn"]').click()
                    sleep(100000)
                    if browser.find_element(By.XPATH, '//*[@id="code"]') :
                        FindLink = 0
                        Confirm = 0
                    else:
                        sleep(SleepTime)
                except:
                    sleep(SleepTime/5)

        print("Fetching code from email")
        # sleep(100000)
        VrCode = fetch_code(user, password, imap_url)

        CodeBox = browser.find_element(By.XPATH, '//*[@id="code"]') 
        CodeBox.clear()
        CodeBox.send_keys(VrCode)

        browser.find_element(By.CSS_SELECTOR, '.mdc-button').click()

        if SiteLoc == 'NepeanSportsPlex' :
            sleep(SleepTime/5)
            browser.find_element(By.XPATH, '//*[@id="submit-btn"]').click()

        print("Booked Successfully!")

    except:
        print("Booking Failed!")

    finally:
        #browser.quit()
        print("Done!")

if __name__ == '__main__':
    Booking()