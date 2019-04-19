import requests as rq
import json
import os

from bs4 import BeautifulSoup as bs


# return illust IDs [list]
def query_page(key_word, page_idx):
    init_url = 'https://www.pixiv.net/search.php?s_mode=s_tag&word={}&p={}'
    url = init_url.format(key_word, page_idx)

    resp = rq.get(url)
    soup = bs(resp.text, 'lxml')
    tag = soup.find('input', id='js-mount-point-search-result-list')

    items = json.loads(tag['data-items'])
    ill_ids = [item['illustId'] for item in items]
    ill_ids = [_id for _id in ill_ids if _id]

    return ill_ids

def query_keyword(key_word):
    idx = 1
    ret = set()

    while True:
        temp = set(query_page(key_word, idx))
        if len(temp - ret) == 0: break

        print('crawl id: %s - p.%d' % (key_word, idx))
        ret |= temp
        idx += 1

    return ret

def crawl_illust(base_dir, illust_id):
    base_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='

    target = base_url + illust_id
    resp = rq.get(target)
    soup = bs(resp.text, 'lxml')

    # get image src
    target_img = soup.find(lambda x: x.name == 'img' and x['src'].find('600x600') != -1)

    if target_img:
        target_img = target_img['src']
        img_title = '%s_%s.jpg' % (illust_id, soup.find('meta', property='og:title')['content'][:-7].replace('/', '_'))

        if os.path.isfile(img_title):
            print('%s exist, skip.' % (img_title))
            return

        print('download %s' % (img_title))

        resp = rq.get(target_img, headers = { 'Referer': target })
        if resp.status_code == 200:
            with open(base_dir + img_title, 'wb+') as f:
                f.writelines(resp)
        
if __name__ == '__main__':
    ill_ids = set()
    ill_ids |= query_keyword('藤原書記')
    ill_ids |= query_keyword('藤原千花')

    print('%d illusts found.' % len(ill_ids))

    for ill_id in ill_ids:
        crawl_illust('./chika/', ill_id)

