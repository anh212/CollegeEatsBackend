#Imports for web scraper
import requests
from bs4 import BeautifulSoup

#Python library for connecting to PostgreSQL DB
import psycopg2
from psycopg2 import Error
from psycopg2 import sql

#Reading db config from JSON
import json

import sys

mapDayToNum = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
}


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


url = 'https://lehigh.sodexomyway.com/dining-near-me/hours'

'Uncomment when making actual request'
r = requests.get(url)

# print(r.content[:100])

'Save html file locally'
# save_html(r.content, 'lehighDining.html')

# For testing
# html = open_html('lehighDining.html')

diningLocations = {}
#diningLocations dict structure
"""
{
    "diningLocation":
    {
        
        [
            {"daynum": 0
            "starttime": 2
            "endtime": 16},
            ...
            ...
        ]
    }
    ...
    ...
}
"""

# Use r.content for 1st argument when making request
soup = BeautifulSoup(r.content, 'html.parser')
# #NEW CODE
diningBlocks = soup.find_all("div", attrs={"class": "dining-block"})

for diningBlock in diningBlocks:
    # Name of dining hall
    # print(diningBlock)
    diningTitleBlock = diningBlock.select("h3")
    # print(diningTitleBlock)
    # print()
    diningName = None
    if diningTitleBlock[0].find("a"):
        diningName = diningTitleBlock[0].find("a").string
    else:
        diningName = diningTitleBlock[0].string

    # diningName = diningBlock.find("h3").find("a").string
    setRegHours = diningBlock.select(".reghours")
    # print(setRegHours)
    # print()
    for regHours in setRegHours:
        # print(regHours)
        # print()

        hours = regHours.select("div")
        # print(hours)
        for hour in hours:
            # print(hour)
            setOfDays = hour.select("p")
            # print(setOfDays)
            #If clear div is found
            if not setOfDays:
                continue
            
            regDays = setOfDays[0]

            setOfRegDays = regDays["data-arrayregdays"]

            # Each set of days (array of strings) for certain hours
            # Need to map Sunday - Saturday as 0 - 6
            daysSplit = setOfRegDays.split(",")

            # The hours for set of days (could be "Closed" or there are given hours)
            setOfHours = setOfDays[-1].string #FIX

            for day in daysSplit:
                daynum = None
                starttime = None
                endtime = None

                # print(diningName)
                # print(setOfDays)


                if "Closed" in setOfHours:
                    #put as starttime: 0 and endtime: 0 in database
                    if diningName not in diningLocations:
                        diningLocations[diningName] = []

                    diningLocations[diningName].append({
                        "daynum": mapDayToNum[day],
                        "starttime": 0,
                        "endtime": 0
                    })
                
                #if there are hours
                else:
                    # Array of times [start, end] > strings
                    hoursSplit = setOfHours.split(' - ')
                    # print(hoursSplit)
                    
                    start = None
                    end = None

                    if "24 Hours" in hoursSplit:
                        if diningName not in diningLocations:
                            diningLocations[diningName] = []

                        diningLocations[diningName].append({
                            "daynum": mapDayToNum[day],
                            "starttime": 0,
                            "endtime": 24
                        })
                        continue
                    else:
                        start = hoursSplit[0]
                        end = hoursSplit[1]
                    

                    # AM or PM for both start and end times
                    startAMorPM = start[-2:]
                    # Start time format: X:XX
                    startTime = start[:-2]
                    startHourAndMinutes = startTime.split(':')


                    endAMorPM = end[-2:]
                    # End time format: X:XX
                    endTime = end[:-2]
                    endHourAndMinutes = endTime.split(':')

                    if (startAMorPM == "AM" and endAMorPM == "PM"
                            or startAMorPM == "PM" and endAMorPM == "PM"):
                        daynum = mapDayToNum[day]
                        starttime = int(startHourAndMinutes[0])
                        starttime += float(startHourAndMinutes[1]) / 60

                        endtime = int(endHourAndMinutes[0])
                        endtime += float(endHourAndMinutes[1]) / 60

                        #Add 12 if time is PM
                        if startAMorPM == "PM":
                            starttime += 12
                        if endAMorPM == "PM":
                            endtime += 12

                        if diningName not in diningLocations:
                            diningLocations[diningName] = []

                        diningLocations[diningName].append({
                            "daynum": daynum,
                            "starttime": starttime,
                            "endtime": endtime
                        })


                    elif (startAMorPM == "AM" and endAMorPM == "AM"
                            or startAMorPM == "PM" and endAMorPM == "AM"):
                        daynum = mapDayToNum[day]
                        starttime = int(startHourAndMinutes[0])
                        starttime += float(startHourAndMinutes[1]) / 60

                        endtime = 24

                        #Add 12 if starttime is PM
                        if startAMorPM == "PM":
                            starttime += 12

                        #Reset day back to Sunday if trying to get next day from Saturday
                        daynum2 = daynum
                        if daynum2 == 7:
                            daynum2 = 0

                        starttime2 = 0

                        endtime2 = int(endHourAndMinutes[0])
                        endtime2 += float(endHourAndMinutes[1]) / 60

                        if diningName not in diningLocations:
                            diningLocations[diningName] = []
                        
                        diningLocations[diningName].append({
                            "daynum": daynum,
                            "starttime": starttime,
                            "endtime": endtime
                        })

                        diningLocations[diningName].append({
                            "daynum": daynum2,
                            "starttime": starttime2,
                            "endtime": endtime2
                        })
                    
print()
print()                    
# print(diningLocations)

mapDiningToLocation = {
    "Cort @ Lower UC": "Lower University Center",
    "Rathbone Dining Hall": "Rathbone Dining Hall",
    "Brodhead Dining Hall": "Brodhead House",
    "Baker's Junction": "Upper University Center",
    "Upper UC Food Market": "Upper University Center",
    "Pandini's": "Upper University Center",
    "Global Café": "William's Hall (2nd Floor)",
    "Lucy's Café": "Linderman Library (Lower level)",
    "Iacocca Café": "Iacocca Hall",
    "The Grind @ FML": "E.W. Fairchild-Martindale Library",
    "Hawk's Nest": "Hawk's Nest Eatery",
    "Common Grounds": "Rauch Business Center (2nd Floor)",
    "Fud Truk": "Near E.W. Fairchild-Martindale Library",
    "Market X": "Building C (Mountaintop Campus)",
    "ASA Packer Dining Room": "University Center"
}

try:
    #Read database config from json
    with open('./config.json') as jsonFile:
        data = json.load(jsonFile)
    print(data)

    #Open database connection
    connection = psycopg2.connect(user = data['user'],
                                  password = data['password'],
                                  host = data['host'],
                                  port = data['port'],
                                  database = data['database'])

    cursor = connection.cursor()

    #Selected school
    schoolName = 'lehigh'
    #Get school_id for school
    cursor.execute("""SELECT school_id
                FROM schools WHERE school_name=%s;"""
                ,(schoolName,))
    
    #Returns array of tuples
    school_idFetch = cursor.fetchall()

    school_id = None
    #Check if school is in the database or not
    if school_idFetch:
        school_id = school_idFetch[0][0]
    else:
        #Insert into database if school is not in database
        cursor.execute("""INSERT INTO schools(school_name) 
                        VALUES (%s);""", (schoolName))
        
        newSchool_idFetch = cursor.fetchall()
        school_id = school_idFetch[0][0]
    
    #Clear schedules to insert new schedule
    cursor.execute("""TRUNCATE hours""")
    # connection.commit()

    for diningLocation, schedule in diningLocations.items():
        print(diningLocation)

        #Insert dining location if it does not exist already
        cursor.execute(("""INSERT INTO dining_locations (school_id, dining_name, location_name) VALUES (
	    (SELECT school_id FROM schools WHERE school_name=%s),
        %s,
        %s)
        ON CONFLICT DO NOTHING"""),
        (schoolName, diningLocation, mapDiningToLocation[diningLocation])
        )

        #Insert new hours into hours table
        for eachSchedule in schedule:
            print(eachSchedule)
            daynum = eachSchedule["daynum"]
            starttime = eachSchedule["starttime"]
            endtime = eachSchedule["endtime"]

            print('test1')
            # cursor.execute("""(SELECT dining_id FROM dining_locations WHERE dining_name=%s)""",(diningLocation,))
            # print(cursor.fetchall()[0][0])

            #FIX ERROR
            cursor.execute(("""INSERT INTO hours (school_id, dining_id, daynum, starttime, endtime) 
            VALUES (
                    (SELECT school_id FROM schools WHERE school_name=%s),
                    (SELECT dining_id FROM dining_locations WHERE dining_name=%s),
                    %s,
                    %s,
                    %s)"""),
                    (schoolName, diningLocation, daynum, starttime, endtime)
                )
            print('test2')
    
    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    print(line_num)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

