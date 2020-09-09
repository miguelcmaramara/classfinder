import json
import pygraphviz as pgv
import pprint
pp = pprint.PrettyPrinter()

# class tree

# 1. Create tree class
#   xx load from file
#   xx assignment function
#   xx prereq edge flipping
#   xx create pygraphviz view
#   -- load from data if no json is available
# 2. create node class
#   x- stores classes that it is prereq to
#   -- Stores the number of credits
#   -- store pygraphviz edges

class Tree:
    courses = {}
    depTree = {}
    missCourses = []
    


    def __init__(self, fileName):
        with open(fileName + ".json") as file:
            self.treeRaw = json.load(file)

        self.assign()
        self.upDep()

    def assign(self):
        for crse in self.treeRaw:
            self.courses[crse] = self.Course(self.treeRaw[crse])
            pp.pprint(crse)

    def upDep(self):    # many for loops becuase each item in prereq list is a nested list
        for crse, attr in self.courses.items():  # Course in course dictionary
            for preReq in attr.preReqs: # Prereq item ( which is a list) in preReq attr
                for courseID in preReq:   # each course id in the list
                    try:
                        self.courses[courseID].deps.append(attr) # each dependency is a pointer to another class obj
                    except:
                        self.missCourses.append(courseID) # if class does not exist, add a missing courses list

                    try:
                        self.depTree[courseID].append(attr.ID)
                    except:
                        self.depTree[courseID] = []
                        self.depTree[courseID].append(attr.ID)
                    # try:    # appends itself to the old dependent classes
                        # self.depTree[courseID] = [self.depTree[courseID], attr.ID]
                    # except:
                        # self.depTree[courseID] = attr.ID

        # Create the graph
        self.Graph = pgv.AGraph(self.depTree)
        self.Graph.layout(prog='neato')
        self.Graph.write("graph.dot")
        self.Graph.draw('graph.png')

        

    class Course:
        ID = None
        name = None
        desc = None
        preReqs = []
        coReqs = []
        deps = []
        SBC = []

        def __init__(self, course):
            self.name = course["name"]
            self.ID = course["id"]
            self.preReqs = course["preReq"]




    

mecTree = Tree("myfile")
pp.pprint(mecTree.courses["MEC101"].name)
