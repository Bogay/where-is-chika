import json

from pixivpy3 import *

USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

if __name__ == '__main__':
    # 把帳密等設定讀進來
    with open('.config.json', 'r') as f:
        CONFIG = json.load(f)

    # 設定帳密
    USERNAME = CONFIG['username']
    PASSWORD = CONFIG['password']

    # 建立一個API物件並且登入
    api = AppPixivAPI()
    api.login(USERNAME, PASSWORD)

    # 放圖的資料夾
    base_dir = 'test'

    # 取得搜尋結果
    illusts = api.search_illust('藤原千花')

    # 當還有下一頁的時候
    while illusts is not None:
        # 讀取每一張圖的資料
        for illust in illusts['illusts']:
            # 取得圖片URL
            image_url = illust['image_urls']['large']
            # 副檔名
            extension = image_url.split('.')[-1]
            # 檔名
            name = f'{illust["id"]}.{extension}'
            # 下載圖片
            api.download(image_url, path=base_dir, name=name)

        #　翻頁
        illusts = api.parse_qs(illusts['next_url'])

        # 到最後一頁了
        if illusts is None:
            break
        
        # 取得下一頁的結果
        illusts = api.search_illust(**illusts)
