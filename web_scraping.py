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

    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    conn = psycopg2.connect("dbname=webscraping user=postgres password=postgres")
    cur = conn.cursor()

# ----------------------------------------------------------------------------

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
    if (ama_gpu_soup.findAll("span", {"class":"a-color-price"})):
        ama_gpu_price = Decimal((ama_gpu_soup.findAll("span", {"class":"a-color-price"})[0].get_text()).replace('$', ''))
    else:
        ama_gpu_price = 0
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
    

#--------------------------------------------------------------------

    bb_amazon_URLS = [
        # start at volume 9
        '',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316189677/ref=sr_1_1?dchild=1&keywords=black+butler+vol.9&qid=1601772052&sr=8-1',
        '',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316225339/ref=pd_sim_14_4/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316225339&pd_rd_r=659b021c-b1f5-486c-b492-5e7f1e11d251&pd_rd_w=nYCpI&pd_rd_wg=UmXMd&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=ZSWCS1F4N7AV7S7204D8&psc=1&refRID=ZSWCS1F4N7AV7S7204D8',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316225347/ref=pd_sim_14_2/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316225347&pd_rd_r=659b021c-b1f5-486c-b492-5e7f1e11d251&pd_rd_w=nYCpI&pd_rd_wg=UmXMd&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=ZSWCS1F4N7AV7S7204D8&psc=1&refRID=ZSWCS1F4N7AV7S7204D8',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316244295/ref=pd_sim_14_3/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316244295&pd_rd_r=b85fe8f5-76ee-49e2-8f34-4a79298b35d4&pd_rd_w=0bNR6&pd_rd_wg=Z9ean&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=HH25YWSET48YBW1W1E9S&psc=1&refRID=HH25YWSET48YBW1W1E9S',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316244309/ref=pd_sim_14_1/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316244309&pd_rd_r=b85fe8f5-76ee-49e2-8f34-4a79298b35d4&pd_rd_w=0bNR6&pd_rd_wg=Z9ean&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=HH25YWSET48YBW1W1E9S&psc=1&refRID=HH25YWSET48YBW1W1E9S',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316254193/ref=pd_sim_14_4/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316254193&pd_rd_r=759b6bc8-c445-4271-a886-88ea33352310&pd_rd_w=8GpdZ&pd_rd_wg=YKm0x&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=MGSD4D92GWB72BXZAF7C&psc=1&refRID=MGSD4D92GWB72BXZAF7C',   
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316369020/ref=pd_sim_14_9?_encoding=UTF8&pd_rd_i=0316369020&pd_rd_r=22dd78c7-5f38-43fd-81cb-70860c90f737&pd_rd_w=mUK5N&pd_rd_wg=AykLy&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=Z6JTGJTFBM2KZD2CF6VH&psc=1&refRID=Z6JTGJTFBM2KZD2CF6VH',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/0316376701/ref=pd_sim_14_1/355-4405811-4057514?_encoding=UTF8&pd_rd_i=0316376701&pd_rd_r=210f5071-bb51-4308-992d-c5cc1d245e30&pd_rd_w=ftpCO&pd_rd_wg=VvcoM&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=KC9PYEC8TZ3XWSMRVS7V&psc=1&refRID=KC9PYEC8TZ3XWSMRVS7V',
        'https://www.amazon.com.au/Black-Butler-Vol-Yana-Toboso/dp/031633622X/ref=pd_sim_14_3/355-4405811-4057514?_encoding=UTF8&pd_rd_i=031633622X&pd_rd_r=b4dad185-c318-415f-a68f-0692dd7b7836&pd_rd_w=6wZhw&pd_rd_wg=bn95V&pf_rd_p=dec5644e-0ad3-467a-97e1-8e4d6a4ec7c2&pf_rd_r=ND6CSCWQ3FKC57ZH099Y&psc=1&refRID=ND6CSCWQ3FKC57ZH099Y'
    ]

    bb_book_depository_URLS = [
        '',
        'https://www.bookdepository.com/Black-Butler-Vol-9-Yana-Toboso/9780316189675?ref=pd_detail_1_sims_b_p2p_1',
        '',
        'https://www.bookdepository.com/Black-Butler-Vol-11-Yana-Toboso/9780316225335?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-12-Yana-Toboso/9780316225342?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-13-Yana-Toboso/9780316244299?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-14-Yana-Toboso/9780316244305?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-15-Yana-Toboso/9780316254199?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-16-Yana-Toboso/9780316369022?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-17-Yana-Toboso/9780316376709?ref=pd_detail_1_sims_b_p2p_1',
        'https://www.bookdepository.com/Black-Butler-Vol-18-Yana-Toboso/9780316336222?ref=pd_detail_1_sims_b_p2p_1'
    ]

    for i in range(1, 11):
        if (i != 2):

            bb_ama_page = requests.get(bb_amazon_URLS[i], headers=headers)

            bb_ama_soup = BeautifulSoup(bb_ama_page.content, 'html.parser')

            bb_title = 'Black Butler Vol.' + str(i + 8)
            bb_ama_price = Decimal((bb_ama_soup.findAll("span", {"class":"a-color-price"})[0].get_text()).replace('$', ''))

            print(bb_title)
            print(bb_ama_price)
            
            bb_bd_page = requests.get(bb_book_depository_URLS[i], headers=headers)

            bb_bd_soup = BeautifulSoup(bb_bd_page.content, 'html.parser')

            bb_bd_price = bb_bd_soup.findAll("span", {"class":"sale-price"})[0].get_text()
            bb_bd_price = Decimal(bb_bd_price.replace('A$', ''))
            print(bb_bd_price)
            
            sql = "INSERT INTO debbie (name, date, amazon, book_depository)  VALUES (%s, %s, %s, %s);"

            cur.execute(sql, (bb_title, d1, bb_ama_price, bb_bd_price,))

            conn.commit()
        else: 
            print('skip volume 10')

schedule.every().day.at("09:00").do(prices)

while True:
    schedule.run_pending()
    time.sleep(1)

# prices()

# Priorty list for improvements
# handle error and keep going

# look into Ezgmail for accessing emails 'https://pypi.org/project/EZGmail/'

# look into gmail api to access emails
# imaplib ??
