from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import math
import csv

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.headless = True
PATH = 'C:\chromedriver.exe'
driver = Chrome(PATH,chrome_options=chrome_options)

driver.get('http://epds.bihar.gov.in/DistrictWiseRationCardDetailsBH.aspx')
driver.find_element(By.ID, 'btnLoad').click()

soup = BeautifulSoup(driver.page_source, features="html5lib")
rows = soup.find_all('tr')

f = open('data.csv', 'w', encoding='utf-8')
writer = csv.writer(f)
header = ['District',
          'Block',
          'Panchayat',
          'Village',
          'Ration Card',
          'Card Type',
          'Card Holder',
          'Father\'s Name',
          'Number of Family Members',
          'FPS Dealer']
writer.writerow(header)
count = 0
for row in rows[20:]:
    tds = row.find_all('td')
    if len(tds) == 10:
        print(rows.index(row))
        print(tds[1].text.strip())
        district_name = tds[1].text.strip()
        district_link = tds[2].find('a')['id']
        driver.find_element(By.ID, district_link).click()
        soup = BeautifulSoup(driver.page_source, features="html5lib")
        block_page_rows = soup.find_all('tr')
        for block_page_row in block_page_rows:
            blocks = block_page_row.find_all('td')
            if len(blocks) == 5:
                block_name = blocks[1].text.strip()
                try:
                    block_link = blocks[1].a['id']
                except:
                    continue
                # print(block_name)
                driver.find_element(By.ID, block_link).click()
                soup = BeautifulSoup(driver.page_source, features="html5lib")
                panchayat_page_rows = soup.find_all('tr')
                for panchayat_page_row in panchayat_page_rows:
                    panchayats = panchayat_page_row.find_all('td')
                    if len(panchayats) == 5:
                        panchayat_name = panchayats[1].text.strip()
                        try:
                            panchayat_link = panchayats[1].a['id']
                        except:
                            continue
                        # print(panchayat_name)
                        driver.find_element(By.ID, panchayat_link).click()
                        soup = BeautifulSoup(
                            driver.page_source, features="html5lib")
                        village_page_rows = soup.find_all('tr')
                        for village_page_row in village_page_rows:
                            villages = village_page_row.find_all('td')
                            if len(villages) == 5:
                                village_name = villages[1].text.strip()
                                total_cards = int(villages[4].text.strip())
                                total_pages = math.floor(total_cards/50)
                                if total_cards > 500:
                                    total_pages -= 2
                                elif total_pages > 1000:
                                    total_pages -= 3
                                total_pages = 0
                                try:
                                    village_link = villages[1].a['id']
                                except:
                                    continue
                                # print(village_link)
                                driver.find_element(
                                    By.ID, village_link).click()
                                time.sleep(0.5)
                                soup = BeautifulSoup(
                                    driver.page_source, features="html5lib")
                                ration_page_rows = soup.find_all('tr')
                                # print(ration_page_rows)
                                for ration_page_row in ration_page_rows:
                                    rations = ration_page_row.find_all(
                                        'td')

                                    if len(rations) == 7:
                                        try:
                                            print(rations[1].text)
                                            ration_card = rations[1].text.strip(
                                            )
                                            card_type = rations[2].text.strip(
                                            )
                                            card_holder = rations[3].text.strip(
                                            )
                                            father_name = rations[4].text.strip(
                                            )
                                            family_num = rations[5].text.strip(
                                            )
                                            fps_dealer = rations[6].text.strip(
                                            ).replace(' ', '', 1000)
                                            final_data = {
                                                'District': district_name,
                                                'Block': block_name,
                                                'Panchayat': panchayat_name,
                                                'Village': village_name,
                                                'Ration Card': ration_card,
                                                'Card Type': card_type,
                                                'Card Holder': card_holder,
                                                'Father\'s Name': father_name,
                                                'Number of Family Members': family_num,
                                                'FPS Dealer': fps_dealer
                                            }
                                            # header = final_data.keys()
                                            row = final_data.values()
                                            writer.writerow(row)
                                            count += 1
                                            print(count)
                                            print(final_data)
                                        except:
                                            continue
                                if total_pages == 1:
                                    continue
                                for page in range(total_pages):
                                    page_url = f"javascript:__doPostBack('gridmain','Page${page+2}')"
                                    driver.execute_script(page_url)
                                    soup = BeautifulSoup(
                                        driver.page_source, features="html5lib")
                                    ration_page_rows = soup.find_all('tr')
                                    for ration_page_row in ration_page_rows:
                                        rations = ration_page_row.find_all(
                                            'td')
                                        if len(rations) == 7:
                                            try:
                                                ration_card = rations[1].text.strip(
                                                )
                                                card_type = rations[2].text.strip(
                                                )
                                                card_holder = rations[3].text.strip(
                                                )
                                                father_name = rations[4].text.strip(
                                                )
                                                family_num = rations[5].text.strip(
                                                )
                                                fps_dealer = rations[6].text.strip(
                                                ).replace(' ', '', 1000)
                                                final_data = {
                                                    'District': district_name,
                                                    'Block': block_name,
                                                    'Panchayat': panchayat_name,
                                                    'Village': village_name,
                                                    'Ration Card': ration_card,
                                                    'Card Type': card_type,
                                                    'Card Holder': card_holder,
                                                    'Father\'s Name': father_name,
                                                    'Number of Family Members': family_num,
                                                    'FPS Dealer': fps_dealer
                                                }
                                                # header = final_data.keys()
                                                row = final_data.values()
                                                writer.writerow(row)
                                                count += 1
                                                print(count)
                                            except:
                                                continue

                                for page in range(total_pages):
                                    driver.back()
                                driver.back()
                        driver.back()
                driver.back()
        driver.back()
