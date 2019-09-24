import requests
import urllib.request
from time import sleep
import pprint

def notification(message,message2):
    report = {}
    report["value1"] = message
    report["value2"] = message2
    requests.post("https://maker.ifttt.com/trigger/seat_available/with/key/bN2gQNggsfGWraE1KKfbtp", data=report)

availability = {}

crn_codes = []
crn_codes.append(input("CRN >> "))

while not crn_codes[-1] == "":
    crn_codes.append(input("CRN >> "))
crn_codes = crn_codes[:-1]

print()
    
course_site = "http://suis.sabanciuniv.edu/prod/bwckschd.p_disp_detail_sched?term_in=201901&crn_in="

try:
    while True:
        for i in range(len(crn_codes)):
            pageSource = (urllib.request.urlopen(course_site+crn_codes[i]).read().decode())
            course_name = "-".join(pageSource.split("\n")[119].split(">")[1].split("<")[0].split("-")[-2:]) + " - " + crn_codes[i]
            try:
                if not availability[crn_codes[i]] == pageSource.split("\n")[148].split(">")[1].split("<")[0]:
                    availability[crn_codes[i]] = pageSource.split("\n")[148].split(">")[1].split("<")[0]
                    notification(crn_codes[i], course_name)
            except KeyError:
                availability[crn_codes[i]] = pageSource.split("\n")[148].split(">")[1].split("<")[0]
            print(course_name + " >> " + availability[crn_codes[i]])
        print()
        sleep(1)
except KeyboardInterrupt:
    quit()