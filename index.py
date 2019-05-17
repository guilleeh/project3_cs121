import json

if __name__ == "__main__":
    with open('./WEBPAGES_RAW/bookkeeping.json', 'r') as myfile:
        data = json.load(myfile)

    for k, v in data.items():
        print(k, v)
