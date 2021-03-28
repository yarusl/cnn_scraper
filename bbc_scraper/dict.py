import json
with open('data.json', 'r') as outfile:
    data = json.load(outfile)

print(data)
print(data['articles'][0])