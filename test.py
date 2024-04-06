import json

with open('test_1.json') as f:
    data = json.load(f)
    print(data["forecasts"][2])

print(list(range(0, 10)))