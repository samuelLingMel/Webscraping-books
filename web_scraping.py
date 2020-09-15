import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import date, timedelta
from decimal import Decimal
from threading import Timer
import schedule
import time

def prices():
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    print(d1)

    conn = psycopg2.connect("dbname=webscraping user=postgres password=postgres")
    cur = conn.cursor()

    amazon_URLS = [
        '',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/0316348805/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=1598990513&sr=8-2',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/0316390291/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=1599984101&sr=1-16',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/0316390305/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=1598990754&sr=1-2',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/0316390313/ref=pd_sim_14_1/358-3999729-8229606?_encoding=UTF8&pd_rd_i=0316390313&pd_rd_r=d946817c-e552-47aa-8cb3-382d518e0efe&pd_rd_w=Ze56e&pd_rd_wg=hWVdQ&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=6AYH7K7DYFD1AEQ1C63G&psc=1&refRID=6AYH7K7DYFD1AEQ1C63G',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/0316390321/ref=sr_1_14?crid=3RJS3EPVAX1KC&dchild=1&keywords=the+irregular+at+magic+high+school&qid=1598790511&sprefix=the+irregular%2Caps%2C334&sr=8-14',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/031639033X/ref=pd_sim_14_4/358-3999729-8229606?_encoding=UTF8&pd_rd_i=031639033X&pd_rd_r=27c9cd98-a4b7-4edb-9c38-9ce2418cf051&pd_rd_w=06iK4&pd_rd_wg=8djUU&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=BWSR0JQA7QQQC5BZA6TE&psc=1&refRID=BWSR0JQA7QQQC5BZA6TE',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975300076/ref=pd_sim_14_3/358-3999729-8229606?_encoding=UTF8&pd_rd_i=1975300076&pd_rd_r=8b7b4b7e-0d15-446c-ac77-c5fc790bd592&pd_rd_w=SgFv0&pd_rd_wg=IapLC&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=PHPGJ57251VJ1QZAX19B&psc=1&refRID=PHPGJ57251VJ1QZAX19B',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975327128/ref=pd_sim_14_1/358-3999729-8229606?_encoding=UTF8&pd_rd_i=1975327128&pd_rd_r=373a1112-91de-4a01-b048-77e852c188f5&pd_rd_w=BtVvG&pd_rd_wg=AS2RH&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=0RGPKC4CRPFM6P5H3MN1&psc=1&refRID=0RGPKC4CRPFM6P5H3MN1',
        'https://www.amazon.com.au/Irregular-Magic-School-Light-Novel/dp/1975327144/ref=pd_sim_14_1/358-3999729-8229606?_encoding=UTF8&pd_rd_i=1975327144&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-Light-Novel/dp/1975327160/ref=pd_sim_14_3/358-3999729-8229606?_encoding=UTF8&pd_rd_i=1975327160&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975327187/ref=pd_sim_14_6/358-3999729-8229606?_encoding=UTF8&pd_rd_i=1975327187&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975327209/ref=pd_sim_14_11?_encoding=UTF8&pd_rd_i=1975327209&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975332326/ref=pd_sim_14_9?_encoding=UTF8&pd_rd_i=1975332326&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975332474/ref=pd_sim_14_13?_encoding=UTF8&pd_rd_i=1975332474&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9',
        'https://www.amazon.com.au/Irregular-Magic-School-light-novel/dp/1975332490/ref=pd_sim_14_14?_encoding=UTF8&pd_rd_i=1975332490&pd_rd_r=f80c796f-0ced-4155-a8ca-77710cee1f24&pd_rd_w=sTREu&pd_rd_wg=1Jjhd&pf_rd_p=cb3cee4a-ac4e-4a56-8989-a52ef5b3a583&pf_rd_r=W3GBN4DQDHF382SRF0T9&psc=1&refRID=W3GBN4DQDHF382SRF0T9'
        ]

    book_depository_URLS = [
        '',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-1-light-novel-Tsutomu-Satou/9780316348805?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-2-light-novel-Tsutomu-Satou/9780316390293?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-3-light-novel-Tsutomu-Satou/9780316390309?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-4-light-novel-Tsutomu-Satou/9780316390316?ref=pd_gw_1_pd_gateway_1_1',
        '',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-6-light-novel-Tsutomu-Satou/9780316390330?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-7-light-novel-Tsutomu-Satou/9781975300074?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-8-light-novel-Tsutomu-Satou/9781975327125?ref=pd_gw_1_pd_gateway_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-9-light-novel-Tsutomu-Satou/9781975327149?ref=pd_gw_1_pd_gateway_1_1',
        '',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-11-light-novel-Tsutomu-Satou/9781975327187?ref=bd_ser_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-12-light-novel-Tsutomu-Satou/9781975327200?ref=bd_ser_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-13-light-novel-Tsutomu-Satou/9781975332327?ref=bd_ser_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-14-light-novel-Tsutomu-Satou/9781975332471?ref=bd_ser_1_1',
        'https://www.bookdepository.com/Irregular-at-Magic-High-School-Vol-15-light-novel-Tsutomu-Satou/9781975332495?ref=bd_ser_1_1'
    ]

    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    for i in range(1, 16):

        ama_page = requests.get(amazon_URLS[i], headers=headers)

        ama_soup = BeautifulSoup(ama_page.content, 'html.parser')

        title = 'Mahouka Vol.' + str(i)
        ama_price = Decimal((ama_soup.findAll("span", {"class":"a-color-price"})[0].get_text()).replace('$', ''))

        print(title)
        print(ama_price)
        
        if ((i != 5) & (i != 10)):
            bd_page = requests.get(book_depository_URLS[i], headers=headers)

            bd_soup = BeautifulSoup(bd_page.content, 'html.parser')

            bd_price = bd_soup.findAll("span", {"class":"sale-price"})[0].get_text()
            bd_price = Decimal(bd_price.replace('A$', ''))
            print(bd_price)
        else:
            bd_price = 0

        sql = "INSERT INTO books (name, date, amazon, book_depository)  VALUES (%s, %s, %s, %s);"

        cur.execute(sql, (title, d1, ama_price, bd_price,))

        conn.commit()

# -------------------------------------------------------------------------

    RTX_2070_super = [
        'https://www.amazon.com.au/Gigabyte-nVidia-GeForce-Gaming-Graphics/dp/B07WZ6FWPK/ref=sr_1_22?crid=185JYGEWF8X67&dchild=1&keywords=2080+super&qid=1600044028&sprefix=2080+s%2Caps%2C361&sr=8-22',
        'https://www.msy.com.au/gigabyte-nvidia-gv-n207sgaming-oc-8gd-8gb-rtx-2070-super-gaming-oc-pci-e-vga-card'
    ]

    ama_gpu_page = requests.get(RTX_2070_super[0], headers=headers)

    ama_gpu_soup = BeautifulSoup(ama_gpu_page.content, 'html.parser')

    gpu_title = 'Gigabyte RTX 2070 super'
    ama_gpu_price = Decimal((ama_gpu_soup.findAll("span", {"id":"priceblock_ourprice"})[0].get_text()).replace('$', ''))

    print(gpu_title)
    print(ama_gpu_price)
    
    msy_gpu_page = requests.get(RTX_2070_super[1], headers=headers)

    msy_gpu_soup = BeautifulSoup(msy_gpu_page.content, 'html.parser')

    msy_gpu_price = Decimal((msy_gpu_soup.findAll("span", {"class":"price-value-13019"})[0].get_text()).replace('$', ''))

    print(msy_gpu_price)

    sql = "INSERT INTO gpus (name, date, amazon, msy)  VALUES (%s, %s, %s, %s);"

    cur.execute(sql, (gpu_title, d1, ama_gpu_price, msy_gpu_price,))

    conn.commit()

    print('done')

schedule.every().day.at("09:00").do(prices)

while True:
    schedule.run_pending()
    time.sleep(1)