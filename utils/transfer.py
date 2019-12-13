import json
import glob
import shutil
import os
import hashlib

if __name__ == '__main__':
    for path in glob.glob('database/*.txt'):
        with open(path, 'r') as f:
            json_meta = f.readline()
            meta = json.loads(json_meta)
        directory = 'classified/{}/'.format(hashlib.md5(meta['genre'].encode()).hexdigest()[:8])
        name = os.path.basename(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.move(path, directory + name)
