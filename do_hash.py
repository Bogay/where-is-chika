import os
import json

from PIL import Image

def compare(ha, hb):
    hd = ha ^ hb
    return bin(hd).count('1') < 5

# reference: https://www.jianshu.com/p/193f0089b7a2
def dhash(img_name):
    w = 9
    h = 8

    img = Image.open(img_name)
    img = img.resize((w, h)).convert('L')

    px = list(img.getdata())
    diff = []

    for r in range(h):
        d = w // 2
        l = w * r # left index
        base_val = px[l + d]
        diff.extend('1' if p > base_val else '0' for p in px[l:l + d])
        diff.extend('1' if p > base_val else '0' for p in px[l + d + 1:l + w])

    ret = int(''.join(diff), 2)

    # if ret == 0:
    #     print(img_name)
    #     print(''.join(diff))

    return ret

if __name__ == '__main__':
    base_dir = './chika/'
    files = os.listdir(base_dir)
    illust_ids = [f.split('_')[0] for f in files]

    d = {}

    for f, i in zip(files, illust_ids):
        h = dhash(base_dir + f)

        if h in d:
            d[h].append(i)
        else:
            d[h] = [i]

    o = []
    for k, v in d.items():
        o.append({ 'hash':k, 'illust_ids':v })

    with open('chikas.json', 'w') as f:
        json.dump(o, f)