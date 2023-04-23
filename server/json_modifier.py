import json
import re

finalJsonMap = {}

# Read JSON file
# Opening JSON file
with open("/Users/suryakanteti/Desktop/CSCI_BD_21_22.json", 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)

# Courses
courseNames = set()
for each_json in json_object:
    courseNames.add(each_json["Crse Title"])

for course in courseNames:
    print(course)

# Create JSON
for courseName in courseNames:
    single_course_list = []

    for each_json in json_object:
        if each_json["Crse Title"] == courseName:
            single_course_list.append(each_json)
    
    # Replace invalid characters
    courseNameKey = courseName.replace("&amp;","and")
    courseNameKey = courseNameKey.replace(".","and")
    courseNameKey = courseNameKey.replace("$","and")
    courseNameKey = courseNameKey.replace("#","and")
    courseNameKey = courseNameKey.replace("[","and")
    courseNameKey = courseNameKey.replace("]","and")
    courseNameKey = courseNameKey.replace("/","and")
    courseNameKey = courseNameKey.replace(":","")
    courseNameKey = courseNameKey.replace("/"," ")
    courseNameKey = courseNameKey.replace("-"," ")


    finalJsonMap[courseNameKey] = single_course_list

# Write JSON to a file
finalJson = json.dumps(finalJsonMap, indent=4)
with open("sample.json", "w") as outfile:
    outfile.write(finalJson)