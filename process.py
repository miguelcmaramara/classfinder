import json
import re
import pprint
pp = pprint.PrettyPrinter()

# class tree
data = {}
with open("classfinder/spiders/raw_courses.json") as file:
   data = json.load(file) 

# pp.pprint(data)

def reqParse(reqs):
    # How to structure prereq:
    # "," indicates "or", ";" indicated "and"
    # a & b -> a;b -> [[a][b]]
    # a or b -> a,b -> [[a, b]]
    # no need for testing, usually we end up with long lists
    reqs = re.sub(r"[,|\s]?\Wand\W", r";", reqs)            # and with ;
    reqs = re.sub(r"[,|\s]?\Wor\W", r",", reqs)             # or with ,
    reqs = re.sub(r"\s", r"", reqs)                         # \s with ""
    reqs = re.sub(r"([A-Z]{3})(\d{3}.)(\d{3})", r"\1\2\1\3", reqs)     # or with ,
    reqs = re.sub(r"([A-Z]{3})(\d{3}.)(\d{3})", r"\1\2\1\3", reqs)     # repeat to catch multiple cases
    reqs = re.sub(r"([A-Z]{3})(\d{3}.)(\d{3})", r"\1\2\1\3", reqs)     # repeat to catch multiple cases
    
    reqs = re.sub(r"([;,]?)[^,;]*[pP]lacement[^,;]*([;,]?)", r"\1Placement\2", reqs)              # changes placement
    reqs = re.sub(r"([,;]?)(U\d)[^,;]*([,;]?)", r"\1\2\3", reqs)            # U1-U4
    reqs = re.sub(r"([,;]?)[^,;]*[gG].?[pP].?[aA][^,;]*([,;]?)", r"\1GPA\2", reqs)            # gpa
    reqs = re.sub(r"([,;]?)[^,;]*[dD].?[eE].?[cC][^,;]*([,;]?)", r"", reqs)            # DEC
    reqs = re.sub(r"([,;]?)[^,;]*([A-Z]{3}\d{3})[^,;]*([,;]?)", r"\1\2\3", reqs)            # cleans AAA000 classformat
    reqs = re.sub(r"[;,]?[pP]ermission[^,;]*[;,]?", r"", reqs)              # Gets rid of 'permission'
    reqs = re.sub(r"[;,]?[^,;]*[gG]rade[^,;]*[;,]?", r"", reqs)              # Gets rid of 'grades'
    reqs = re.sub(r"[;,]?[^,;]*[lL]evel[^,;]*[;,]?", r"", reqs)              # Gets rid of 'level'
    # reqs = re.sub(r"([,;]?)[^,;]*[,;]?[^,;]*betterin([A-Z]{3}\d{3})([,;]?)", r"\1\2\3", reqs)            # "betterin

    results = []    # turns long string into lists, filtering out long and short
    result = []
    for req in reqs.split(";"):
        for subreqs in req.split(","):
            if (len(subreqs) >= 2 and len(subreqs) <= 10):
                result.append(subreqs)
        results.append(result)
        results = list(filter(None, results))
        result = []
            
    return results


courses = {}
#   Structure --------------------------
#   courses:
#       CRS###
#           >id : CRS###
#           >name : "course of courses!"
#           >number : ###
#           >desc : 
#           >SBC 
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

# REGEX post Processing ---------------------
# Loop to enact
for rawCourse in data:
    courseId = re.sub(reIClass,reOClass,rawCourse["className"][0])
    courseNumber = re.sub(reIClass,reONumber,rawCourse["className"][0])
    courseName = re.sub(reIClass,reOName,rawCourse["className"][0])

    try:    # Credits
        courseCredits = re.sub(reICredits,reOCredits,rawCourse["credits"][0])
    except:
        courseCredits = "Unavailable"

    # checks length -- as SBC name lengths are between 3 and 4 inclusively
    # Use find to find the "corequisite"/"prerequisite" word -> if the classes exist thereafter,
    # it processes it. If not, it waits for the next line
    courseCoReq = ''
    coursePreReq = ''
    sbc = []
    nlco = False
    nlpre = False
    for extra in rawCourse["extras"]:    #Coreq
        courseCoReqArr=re.findall(reICoReq, extra)
        coursePreReqArr=re.findall(reIPreReq, extra)

        if(len(extra) <=4 and len(extra) >= 3):
            sbc.append(extra)

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
    coursePreReq = reqParse(coursePreReq)
    courseCoReq = reqParse(courseCoReq)

    courses[courseId] = {
            "id" : courseId,
            "number" : int(courseNumber),
            "name" : courseName,
            "credits" : courseCredits,
            "desc" : rawCourse["desc"][0],
            "coReq" : courseCoReq,
            "preReq" : coursePreReq,
            "SBC" : sbc,
            }



# pp.pprint(courses)
for name, course in courses.items():
    print("------------------")
    print(name)
    print("number")
    print(course["number"])
    print("id")
    print(course["id"])
    print("desc")
    print(course["desc"])
    print("coReq")
    print(course["coReq"])
    print("preReq")
    print(course["preReq"])
    print("SBC")
    print(course["SBC"])
    print("credits")
    print(course["credits"])
out_file = open("myfile.json", "w") 

json.dump(courses,out_file,indent =4)
out_file.close()

