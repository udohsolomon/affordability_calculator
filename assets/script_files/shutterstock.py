import time
import requests
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import os


def is_stop(real):
    file1 = open('{}data.txt'.format(path_files), 'r')
    data1 = file1.readlines()
    file1.close()
    data1 = data1[0].strip()
    if data1 == 'stop':
        return 1000
    else:
        return real

def is_pause():
    file1 = open('{}data.txt'.format(path_files), 'r')
    data1 = file1.readlines()
    file1.close()
    data1 = data1[0].strip()
    if data1 == 'pause':
        while True:
            file1 = open('{}data.txt'.format(path_files), 'r')
            data1 = file1.read()
            file1.close()
            data1 = data1.strip()
            if data1 == 'resume':
                break
            elif data1 == 'stop':
                break
            time.sleep(2)


path = ''
search = ''
# path_files = 'C://Users/DELL/PycharmProjects/shutterstock/assets/gui_files/'
path_files = os.getcwd().replace('\\', '/') + '/assets/gui_files/'
# path_files = path_files.replace('/assets/script_files/', '')
# path_media = os.getcwd().replace('\\', '/').replace('/assets/script_files/', '') + '/assets/media/'

# output_folder = os.getcwd().replace('\\', '/')


class ShutterStock(scrapy.Spider):
    name = 'shutterstock'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'CONCURRENT_REQUESTS': 1,
        # 'ROBOTSTXT_OBEY': False
    }
    headers = {"authority": "www.shutterstock.com",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "accept-language": "en-US,en;q=0.9",
               "cache-control": "no-cache",
               "pragma": "no-cache",
               "referer": "https://www.google.com/",
               "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-platform": "\"Windows\"",
               "sec-fetch-dest": "document",
               "sec-fetch-mode": "navigate",
               "sec-fetch-site": "same-origin",
               "sec-fetch-user": "?1",
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
               }
    page_count = -1
    total_pics = 0
    complete_pics = 0
    def start_requests(self):
        url = 'https://www.shutterstock.com/search/{}?page=1'.format(search.strip().replace(' ', '-'))

        yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        h = 1
        pic_headers = {"authority": "www.shutterstock.com",
                       "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                       "accept-language": "en-US,en;q=0.9",
                       "cache-control": "no-cache",
                       "pragma": "no-cache",
                       "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
                       "sec-ch-ua-mobile": "?0",
                       "sec-ch-ua-platform": "\"Windows\"",
                       "sec-fetch-dest": "document",
                       "sec-fetch-mode": "navigate",
                       "sec-fetch-site": "none",
                       "sec-fetch-user": "?1",
                       "upgrade-insecure-requests": "1",
                       "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                       }
        data = response.css('script[type="application/json"]::text').extract_first()
        pages = json.loads(data).get('props').get('pageProps').get('meta').get('pagination').get('totalPages')
        total_record = json.loads(data).get('props').get('pageProps').get('meta').get('pagination').get('totalRecords')
        boxes = json.loads(data).get('props').get('pageProps').get('assets')
        if self.page_count == -1:
            if total_record < 1000:
                self.total_pics = total_record
            else:
                self.total_pics = 1000
            self.page_count = pages

        for box in boxes:
            self.complete_pics = is_stop(self.complete_pics)
            if self.complete_pics >= self.total_pics:
                h = 1
                break
            pic_id = box.get('id')
            pic_title = box.get('title')
            url = box.get('displays').get('1500W').get('src')
            # filename = (pic_id + pic_title).replace('-', '').replace(':', '').replace('.', '').replace(' ', '').replace(',', '').replace('\n', '').replace('\r', '').replace('|', '').replace('\t', '')
            filename = search.strip().replace(' ', '-') + pic_id
            pic_response = requests.get(url.strip(), stream=True, headers=pic_headers)
            is_pause()
            try:
                with open(path + '/{}.jpg'.format(filename), 'wb') as f:
                    for chunk in pic_response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                print('one download')
                self.complete_pics = self.complete_pics + 1
                file_prog = open('{}prog.txt'.format(path_files), 'w')
                file_prog.write(str(self.complete_pics) + 'by' + str(self.total_pics))
                file_prog.close()
                time.sleep(.75)
            except Exception as e:
                print('error with url ->', url, e)

        if int(response.url.split('?page=')[-1]) < self.page_count and self.complete_pics < self.total_pics:
            url_next = str(response.url.split('?page=')[0]) + '?page=' + str(int(response.url.split('?page=')[-1]) + 1)
            yield scrapy.Request(url=url_next, headers=self.headers, callback=self.parse)

        # qheaders = {
        #     "authority": "www.shutterstock.com",
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "accept-language": "en-US,en;q=0.9",
        #     "cache-control": "no-cache",
        #     "pragma": "no-cache",
        #     "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": "\"Windows\"",
        #     "sec-fetch-dest": "document",
        #     "sec-fetch-mode": "navigate",
        #     "sec-fetch-site": "none",
        #     "sec-fetch-user": "?1",
        #     "upgrade-insecure-requests": "1",
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        # }
    def close(spider, reason):
        h=1
        file = open('{}prog.txt'.format(path_files), 'w')
        file.write('0by1000')
        file.close()
        file = open('{}data.txt'.format(path_files), 'w')
        file.write('finish')
        file.close()
        if spider.page_count == -1:
            file_e = open('{}data.txt'.format(path_files), 'w')
            file_e.write('error')
            file_e.close()



if __name__ == '__main__':
    file = open('{}data.txt'.format(path_files), 'r')
    data = file.readlines()
    file.close()
    path = data[0].strip()
    search = data[1].strip()
    path = path + '/' + search
    if not os.path.exists(path):
        os.makedirs(path)
    process = CrawlerProcess({})
    process.crawl(ShutterStock)
    process.start()

