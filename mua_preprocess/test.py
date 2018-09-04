import json

with open('options.json') as file:
    data = json.load(file)
    print(data)
