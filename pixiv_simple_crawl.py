import requests as rq
import json
import os

from bs4 import BeautifulSoup as bs


# return illust IDs [list]
def query_page(key_word, page_idx):
    url = f'https://www.pixiv.net/search.php?s_mode=s_tag&word={key_word}&p={page_idx}'

    # search for IDs
    resp = rq.get(url)
    soup = bs(resp.text, 'lxml')
    # look for a <input> tag whose id is 'js-mount-point-search-result-list'
    tag = soup.find('input', id='js-mount-point-search-result-list')

    # if not found
    if not tag:
        print(f'can not find ids in {key_word}, p.{page_idx}')

    # get the 'data-items' attribute and parse it
    items = json.loads(tag['data-items'])
    # get IDs
    ill_ids = [item['illustId'] for item in items]
    # filter None
    ill_ids = [_id for _id in ill_ids if _id]

    return ill_ids

def query_keyword(key_word):
    idx = 1
    ret = set()

    # because guest can browse only 10 pages
    while idx <= 10:
        temp = query_page(key_word, idx)
        if len(temp) == 0: break

        print(f'get id: {key_word} - p.{idx}')
        ret |= set(temp)
        idx += 1

    return ret

def crawl_illust(base_dir, illust_id):
    target = f'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust_id}'
    resp = rq.get(target)
    soup = bs(resp.text, 'lxml')

    # get image
    target_img = soup.find(lambda x: x.name == 'img' and x['src'].find('600x600') != -1)

    # check whether we find the image
    if target_img:
        # get the image source path
        target_img = target_img['src']
        # use illust id as filename, avoid special characters
        img_title = illust_id + '.jpg'

        # if the file exists, skip it to save time
        if os.path.isfile(img_title):
            print(f'{img_title} exist, skip.')
            return

        print(f'download {img_title}')

        # download the image, ensure you set the Referer
        resp = rq.get(target_img, headers = { 'Referer': target })
        if resp.status_code == 200:
            with open(base_dir + img_title, 'wb+') as f:
                f.writelines(resp)
        else: # donload fail
            print(f'download {illust_id} fail!')
    else: # can not find the image by id
        print(f'can not found {illust_id}')
        
if __name__ == '__main__':
    ill_ids = set()
    ill_ids |= query_keyword('藤原書記')
    ill_ids |= query_keyword('藤原千花')

    print('%d illusts found.' % len(ill_ids))

    for ill_id in ill_ids:
        crawl_illust('./chika/', ill_id)

