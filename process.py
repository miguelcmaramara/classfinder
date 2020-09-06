import json
import re
import pprint
pp = pprint.PrettyPrinter()

# class tree
data = {}
with open("classfinder/spiders/raw_courses.json") as file:
   data = json.load(file) 

# pp.pprint(data)

courses = {}
#   Structure --------------------------
#   courses:
#       CRS###
#           >id : CRS###
#           >name : "course of courses!"
#           >number : ###
#           >desc : 
#           SBC 
#           >coreq
#           >prereq
#           >credits


# REGEX ---------------------------------------
reIClass = "([A-Z]{3})\\xa0(\d{3}):\s(.*)"
reOClass = r"\1\2"
reONumber = r"\2"
reOName = r"\3"

reICredits = "(\d(-\d)?).*"
reOCredits = r"\1"

reICoReq = r".*[Cc]o-?requisites?:?\s?(.*)"

reIPreReq = r".*Prerequisites?:?\s?(.*)"
# Loop to enact
for rawCourse in data:
    courseId = re.sub(reIClass,reOClass,rawCourse["className"][0])
    courseNumber = re.sub(reIClass,reONumber,rawCourse["className"][0])
    courseName = re.sub(reIClass,reOName,rawCourse["className"][0])

    try:    # Credits
        courseCredits = re.sub(reICredits,reOCredits,rawCourse["credits"][0])
    except:
        courseCredits = "Unavailable"

    # Use find to find the "corequisite"/"prerequisite" word -> if the classes exist thereafter,
    # it processes it. If not, it waits for the next line
    courseCoReq = ''
    coursePreReq = ''
    nlco = False
    nlpre = False
    print(courseId)
    for extra in rawCourse["extras"]:    #Coreq
        courseCoReqArr=re.findall(reICoReq, extra)
        coursePreReqArr=re.findall(reIPreReq, extra)

        if nlco:      # See if the REGEX was caught, but the classes were not in the same line
            courseCoReq = extra
            nlco = False
        try:        # Primes reading the next line if classes not caught
            courseCoReq = courseCoReqArr[0]
            if courseCoReq == '':
                nlco = True
        except:
            pass

        if nlpre:      # See if the REGEX was caught, but the classes were not in the same line
            coursePreReq = extra
            nlpre = False
        try:        # Primes reading the next line if classes not caught
            coursePreReq = coursePreReqArr[0]
            if coursePreReq == '':
                nlpre = True
        except:
            pass

    
    
    courses[courseId] = {
            "id" : courseId,
            "number" : int(courseNumber),
            "name" : courseName,
            "credits" : courseCredits,
            "desc" : rawCourse["desc"][0],
            "coReq" : courseCoReq,
            "preReq" : coursePreReq,
            "SBC" : sbc
            }

# pp.pprint(courses)
for name, course in courses.items():
    print("------------------")
    print(name)
    print(course["coReq"])
    print(course["preReq"])


