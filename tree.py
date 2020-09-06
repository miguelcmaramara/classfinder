import json
import pprint
pp = pprint.PrettyPrinter()
# class tree
with open("classfinder/spiders/file.json") as file:
   data = json.load(file) 

pp.pprint(data)
