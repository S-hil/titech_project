import glob
import json

if __name__ == '__main__':
    categories = set()
    tags = set()
    for path in glob.glob('database/*.txt'):
        with open(path, 'r') as f:
            json_meta = f.readline()
            meta = json.loads(json_meta)
        categories.add(meta['genre'])
        for tag in meta['tag']:
            tags.add(tag)
    print(categories)
    print(tags)
    
