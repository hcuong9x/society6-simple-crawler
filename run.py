
import datetime
import shutil
import time
import sys

from core.usefull import get_data_in_file
from inc.society6 import Society6

def crawl_product(data):
    url = data[0]
    print(f'Processing url {url}')
    crawler = Society6()
    crawler.crawler(url.strip())

def app():
    print("===== Start =====")
    # Start timer
    start_time = time.perf_counter()

    datas = get_data_in_file('input/datas.csv')
    if not datas:
        print('Empty! Please check the import file!')
        sys.exit()
    print(f'Have {len(datas)} links')

    for data in datas:
        print(f'Processing data: {data}')
        crawl_product(data)

    # End timer
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

    now = datetime.datetime.now()
    src_path = 'spf_products.csv'
    dst_path = f'output/spf_products-{now.day}-{now.hour}-{now.minute}-{now.second}.csv'

    shutil.move(src_path, dst_path)
    print(f'Output file: {dst_path}')
    print('===== End ======')
    input('Finish crawler. Press any key to exit!')
    sys.exit()

if __name__ == '__main__':
    app()