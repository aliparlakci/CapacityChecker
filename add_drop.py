import requests
import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import pprint

def getApiKey(config_file):
    apiKey = ""
    with open(config_file,"r") as f:
        apiKey = f.readlines()[0]
    return apiKey

def sendNotification(apiKey,message1,message2):
    report = {}
    report["value1"] = message1
    report["value2"] = message2
    requests.post("https://maker.ifttt.com/trigger/seat_available/with/key/"+apiKey, data=report)

def getCourseHtml(crn):
    course_path = "https://suis.sabanciuniv.edu/prod/bwckschd.p_disp_detail_sched?term_in=201902&crn_in="
    return urllib.request.urlopen(course_path+crn).read().decode()

def getAvailability(soup):
    return int(soup.find_all("td",{"class": "dddefault"})[3].string)

def getCourseInfo(soup):
    name, crn, course_code, section = [el.strip() for el in next(soup.find_all("th", {"class":"ddlabel"})[0].strings).split("-")]
    return {
        "name": name,
        "crn": crn,
        "code": course_code,
        "section": section
    }

def getCrnCodes():
    crn_codes = []
    crn_codes.append(input("CRN >> "))

    while not crn_codes[-1] == "":
        crn_codes.append(input("CRN >> "))
    print()
    return crn_codes[:-1]

def main():
    prevAvailability = {}
    crn_codes = getCrnCodes()
    apiKey = getApiKey("api_key.txt")
    while True:
        for crn in crn_codes:
            soup = BeautifulSoup(getCourseHtml(crn), 'html.parser')
            course_info = getCourseInfo(soup)
            course_info["availability"] = getAvailability(soup)

            print(f"{crn} - {course_info['code']} {course_info['section']} >> {course_info['availability']}",end="")

            # TODO
            # Bug: Program doesn't send notification
            # if there are available seats on the first check

            if not crn in prevAvailability:
                prevAvailability[crn] = course_info["availability"]

            if (course_info["availability"] != 0) and (not prevAvailability[crn] == course_info["availability"]):
                title = f"{crn} - {course_info['code']} {course_info['section']}"
                details = f"{course_info['availability']} seat available."
                sendNotification(apiKey, title, details)
                prevAvailability[crn] = course_info["availability"]
                print(", notification sent!")
            
            print()

        sleep(1)

try:
    main()
except KeyboardInterrupt:
    quit()