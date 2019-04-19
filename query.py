import json
import sys

from do_hash import dhash, compare

if __name__ == '__main__':
    chikas = None

    with open('chikas.json', 'r') as f:
        chikas = json.load(f)
    
    if chikas is None:
        print('Chika not found!')

    h = dhash(sys.argv[1])
    print(h)
    r = []

    for chika in chikas:
        c = compare(h, chika['hash'])
        if c:
            r.append(chika['illust_ids'])

    print(r)