import glob
import json

if __name__ == '__main__':
    summary = {}
    for path in glob.glob('classified/*/*.txt'):
        with open(path, 'r') as f:
            json_meta = f.readline()
            meta = json.loads(json_meta)
        category = meta['genre']
        if category in summary:
            summary[category] += 1
        else:
            summary[category] = 1

    for category in summary:
        print("{}: {}".format(category, summary[category]))
