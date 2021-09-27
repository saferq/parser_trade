import asyncio
import re
import time
from pprint import pprint

import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from support import json_work


class PareserSber():
    ''' Запуск парсера '''

    def __init__(self):
        '''  '''
        print('-------------------------------------')
        print('PareserSber')
        self.json = json_work.JsonWork()
        # путь к драйверу chrome firefox
        options = Options()
        options.headless = True
        driver = 'C:/webdriver/geckodriver'
        self.browser = webdriver.Firefox(
            options=options, executable_path=driver)

    def click_elem_xpath(self, driver, xpath):
        """ Нажать на элемент по xpath """
        elem = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", elem)

    def send_text_xpath(self, driver, xpath, text):
        """ Добавить текст в поле по xpath """
        elem = driver.find_element_by_xpath(xpath)
        elem.send_keys(text)

    def soup_get_urls_lot(self, page):
        """ Получение ссылок """
        print("Получение ссылок")
        soup = BeautifulSoup(page, 'html5lib')
        tables = soup.find_all(class_='purch-reestr-tbl-div')
        urls_lot = []
        for table in tables:
            lot_url = table.find(content="leaf:objectHrefTerm")
            urls_lot.append(lot_url['value'])
        return urls_lot

    def parse_utpsber(self, url, category, count, len_link):
        """ Парсинг сайта с url где utp.sberbank-ast.ru """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        browser = self.browser
        browser.implicitly_wait(10)
        browser.get(url)
        page = browser.page_source
        # browser.quit()
        soup = BeautifulSoup(page, 'html5lib')
        json_data = self.json.open_json('temp.json')

        # Площадка
        tag = 'platform'
        val = 'utp.sberbank-ast.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.find(content="leaf:RequesterName")
        if elem == None:
            elem = soup.find(content="leaf:OrgName")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, elem.get_text())
        self.json.save_json('temp.json', json_data)

        # Способ размещения
        tag = 'placement_method'
        elem_type = soup.find(content="leaf:PurchaseTypeName")
        elem_code = soup.find(content="leaf:PurchaseCode")

        if (elem_type == None) and (elem_code == None):
            val = '---'
        elif (elem_type != None) and (elem_code == None):
            val = elem_type.get_text()
        elif (elem_type == None) and (elem_code != None):
            val = elem_code.get_text()
        elif (elem_type != None) and (elem_code != None):
            val = elem_type.get_text() + ' ' + elem_code.get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.find(content="leaf:PurchaseName")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, elem.get_text())
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.find(content="leaf:BidObjectLocation")
        if elem == None:
            elem = soup.find(content="leaf:BidDeliveryPlace")
            if elem == None:
                elem = soup.find(content="leaf:RequesterAddressFact")
                if elem == None:
                    elem = soup.find(content="leaf:CustomerAddressFact")
                    if elem == None:
                        elem = soup.find(content="leaf:OrgAddressFact")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, elem.get_text())
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.find(content="leaf:BidPrice")
        if elem == None:
            elem = soup.find(content="leaf:PurchaseAmount")
            if elem == None:
                elem = soup.find(content="leaf:BidAmount")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала подачи заявок
        tag = 'date_start'
        elem = soup.find(content="leaf:RequestStartDate")
        if elem == None:
            elem = soup.find(content="leaf:ApplSubmissionStartDate")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, elem.get_text())
        self.json.save_json('temp.json', json_data)

        # Дата окончания подачи заявок
        tag = 'date_end'
        elem = soup.find(content="leaf:RequestStopDate")
        if elem == None:
            elem = soup.find(content="leaf:ApplSubmissionStopDate")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, elem.get_text())
        self.json.save_json('temp.json', json_data)

        # Дата рассмотрения заявок
        tag = 'date_consideration'
        elem = soup.find(content="leaf:PurchaseRequestReviewDate")
        if elem == None:
            elem = soup.find(content="leaf:ExaminationDate")
            if elem == None:
                elem = soup.find(content="leaf:RequestReviewDate")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала торговой сессии
        tag = 'date_trading'
        elem = soup.find(content="leaf:AuctionStartDate")
        if elem == None:
            elem = soup.find(content="leaf:AuctionDate")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата подведения итогов
        tag = 'date_summarizing'
        elem = soup.find(content="leaf:PurchaseResultDate")
        if elem == None:
            elem = soup.find(content="leaf:SummingupDate")
            if elem == None:
                elem = soup.find(content="leaf:PurchaseAuctionResultDate")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

    def parse_sberast(self, url, category, count, len_link):
        """ Парсинг сайта с url где purchaseview """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        browser = self.browser
        browser.implicitly_wait(10)
        browser.get(url)
        page = browser.page_source
        soup = BeautifulSoup(page, 'html5lib')
        json_data = self.json.open_json('temp.json')

        # Площадка
        tag = 'platform'
        val = 'sberbank-ast.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.find(content="leaf:orgname")
        if elem.get_text() == '':
            elem = soup.find_all(content="leaf:orgname")[1]
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Способ размещения
        tag = 'placement_method'
        elem_type = soup.find(content="leaf:purchTypeName")
        elem_code = soup.find(content="leaf:purchCode")
        if elem_type == None:
            val = '---'
        if elem_code == None:
            val = ''
        else:
            val = elem_type.get_text() + ' ' + elem_code.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.find(content="leaf:purchname")
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.find(content="leaf:purchDescr")
        if elem.get_text() == 'по месту нахождения Исполнителя':
            elem = soup.find(content="leaf:deliveryplace")
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.find(content="leaf:purchAmount")
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата окончания подачи заявок
        tag = 'date_end'
        elem_date = soup.find(content="leaf:requestdate")
        elem_time = soup.find(content="leaf:requestdatetime")

        if elem_date == None:
            val = '---'
        else:
            val = elem_date.get_text() + " " + elem_time.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата рассмотрения заявок
        tag = 'date_consideration'
        elem_date = soup.find(content="leaf:requestacceptdate")
        if elem_date == None:
            elem_date = soup.find(content="leaf:ResultDate")

        if elem_date == None:
            val = '---'
        else:
            val = elem_date.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала торговой сессии
        tag = 'date_trading'
        elem_date = soup.find(content="leaf:auctionbegindate")
        elem_time = soup.find(content="leaf:auctionbegindatetime")

        if elem_date == None:
            val = '---'
        else:
            val = elem_date.get_text() + " " + elem_time.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

    def parse_sberb2b(self, url, category, count, len_link):
        """ Парсинг сайта с url где PurchaseView """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        browser = self.browser
        browser.implicitly_wait(10)
        browser.get(url)
        page = browser.page_source
        # browser.quit()
        soup = BeautifulSoup(page, 'html5lib')
        json_data = self.json.open_json('temp.json')

        # Площадка
        tag = 'platform'
        val = 'sberb2b.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.select_one(
            '#vue-content > div.container.order > div > div.order__content > div.dashboard-info > div.dashboard-info__content > div:nth-child(2) > span.dashboard-info__text-text.dashboard-info__text--bold.dashboard-info__text--green > a')
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Способ размещения
        tag = 'placement_method'
        elem = soup.find(
            '#vue-content > div.container.order > div > div.order__content > div.order__heading > span')

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.select_one(
            '#vue-content > div.container.order > div > div.order__content > div.order__heading > div > span')
        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.select_one(
            '#vue-content > div.container.order > div > div.order__content > div.dashboard-info > div.dashboard-info__content > div:nth-child(4) > span.dashboard-info__text.dashboard-info__text--bold')
        if elem == None:
            val = '---'
        else:
            val = elem.get_text().strip()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.select_one(
            '#vue-content > div.container.order > div > div.order__content > div.dashboard-info > div.dashboard-info__content > div:nth-child(7) > span.dashboard-info__text.dashboard-info__text--bold')
        if elem == None:
            val = '---'
        else:
            val = elem.get_text().strip()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # # Дата окончания подачи заявок
        tag = 'date_end'
        elem = soup.select_one(
            '#vue-content > div.container.order > div > div.order__content > div.dashboard-info > div.dashboard-info__content > div:nth-child(5) > span.dashboard-info__text.dashboard-info__text--bold')
        if elem == None:
            val = '---'
        else:
            val = elem.get_text().strip()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

    def safe_to_html(self, html):
        with open('page.html', 'w', encoding="utf-8") as f:
            f.writelines(html)
        print("save html")

    def main(self, ids):
        browser = self.browser
        # Переход на страницу входа
        browser.implicitly_wait(10)
        browser.get('https://www.sberbank-ast.ru/UnitedPurchaseList.aspx')
        # Работа с фильтром
        # Нажать кнопку добавить фильтр
        print("Работа с фильтром")
        xpath_1 = '//*[@id="filters"]/div/table/tbody/tr[1]/td[2]/button[1]'
        self.click_elem_xpath(browser, xpath_1)
        # Нажать кнопку Этап проведения
        xpath_2 = '//*[@id="specialFilters"]/table[1]/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'
        self.click_elem_xpath(browser, xpath_2)
        # Выбрать Подача заявок
        check_phase = '//tbody/tr[8]/td[1]/input'
        self.click_elem_xpath(browser, check_phase)
        # Нажать кнопку Применить
        btn_check = '//*[@id="shortDictionaryModal"]/div/div/div[3]/input'
        self.click_elem_xpath(browser, btn_check)
        # Работа с запросом
        # Ввод запроса
        print("Работа с запросом")
        search_field = '//*[@id="searchInput"]'
        self.send_text_xpath(browser, search_field, 'лом')
        # Нажать кнопку поиск
        btn_search = '//*[@id="OkCansellBtns"]/input[1]'
        self.click_elem_xpath(browser, btn_search)
        # Получить результат
        time.sleep(2)
        browser.implicitly_wait(15)
        page = browser.page_source
        # Работа парсера
        print("Работа парсера")
        urls = self.soup_get_urls_lot(page)
        len_link = len(urls)
        count = 1
        category = 'lots'
        for url in urls:
            if url not in ids:
                if 'PurchaseView' in url:
                    self.parse_utpsber(url, category, count, len_link)
                elif 'purchaseview' in url:
                    self.parse_sberast(url, category, count, len_link)
                elif 'sberb2b.ru' in url:
                    self.parse_sberb2b(url, category, count, len_link)
                else:
                    print('other')
            else:
                print('-------------------------------------')
                print(f'parse_link: {count} in {len_link}')
                print(f"Есть: {url}")
            count += 1

        browser.quit()


class PareserTektorg():
    ''' Запуск парсера на www.tektorg.ru '''

    def __init__(self):
        print('-------------------------------------')
        print('PareserTektorg')
        self.json = json_work.JsonWork()

    def init_browser(self, url):
        ''' Получение страницы '''
        options = Options()
        options.headless = True
        driver = 'C:/webdriver/geckodriver'
        browser = webdriver.Firefox(
            options=options, executable_path=driver)
        # Переход на страницу входа
        browser.implicitly_wait(10)
        browser.get(url)
        page = browser.page_source
        browser.quit()
        return page

    def click_elem_xpath(self, driver, xpath):
        """ Нажать на элемент по xpath """
        elem = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", elem)

    def send_text_xpath(self, driver, xpath, text):
        """ Добавить текст в поле по xpath """
        elem = driver.find_element_by_xpath(xpath)
        elem.send_keys(text)

    def soup_get_urls_lot(self, page):
        """ Получение ссылок """
        print("Получение ссылок")
        soup = BeautifulSoup(page, 'html5lib')
        tables = soup.find_all(class_='section-procurement__item')
        urls_lot = []
        for table in tables:
            lot_url = table.find(class_="section-procurement__item-title")
            urls_lot.append('https://www.tektorg.ru' + lot_url.get('href'))
        return urls_lot

    def parse_links_sale(self, url, count, len_link):
        """ Парсинг сайта с url где www.tektorg.ru """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        json_data = self.json.open_json('temp.json')
        page = self.init_browser(url)
        soup = BeautifulSoup(page, 'html5lib')
        category = 'lots'

        # Площадка
        tag = 'platform'
        val = 'www.tektorg.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.find('td', string='Наименование организатора:').parent
        elem = elem.select('td')[1]

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Способ размещения
        tag = 'placement_method'
        elem_type = soup.find('td', text=re.compile('Тип процедуры'))
        if elem == None:
            elem_type = soup.find('td', text=re.compile('Способ закупки'))
        elem_code = soup.find('td', text=re.compile('Номер процедуры'))
        if elem == None:
            elem_code = soup.find('td', text=re.compile('Номер закупки'))

        if (elem_type == None) and (elem_code == None):
            val = '---'
        elif (elem_type != None) and (elem_code == None):
            val = elem_type.get_text()
        elif (elem_type == None) and (elem_code != None):
            val = elem_code.get_text()
        elif (elem_type != None) and (elem_code != None):
            val = elem_type.parent.find_all('td')[1].get_text() + ' ' + \
                elem_code.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.find('span', class_="procedure__item-name")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.find('td', text=re.compile(
            'Регион ПИ'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Место'))
            if elem == None:
                elem = soup.find('td', text=re.compile(
                    'Почтовый адрес'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.select('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.find('td', class_="procedure__lot-cost")

        if elem == None:
            val = '---'
        else:
            val = elem.get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала подачи заявок
        tag = 'date_start'
        elem = soup.find('td', text=re.compile(
            'Дата начала подачи заявок'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Дата и время начала подачи'))
            if elem == None:
                elem = soup.find('td', text=re.compile(
                    'Дата публикации процедуры'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата окончания подачи заявок
        tag = 'date_end'
        elem = soup.find('td', text=re.compile(
            'Дата окончания приема заявок'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Дата и время окончания подачи'))
            if elem == None:
                elem = soup.find('td', text=re.compile(
                    'Дата окончания срока подачи'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала торговой сессии
        tag = 'date_trading'
        elem = soup.find('td', text=re.compile(
            'Дата проведения торгов'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Дата проведения аукциона'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата подведения итогов
        tag = 'date_summarizing'
        elem = soup.find('td', text=re.compile(
            'Дата проведения торгов'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Подведение итогов не позднее'))
            if elem == None:
                elem = soup.find('td', text=re.compile(
                    'Дата окончания предоставления разъяснений'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

    def main(self, url, ids):
        """  """
        page = self.init_browser(url)
        links = self.soup_get_urls_lot(page)
        len_link = len(links)
        count = 1
        for link in links:
            if link not in ids:
                self.parse_links_sale(link, count, len_link)
            else:
                print('-------------------------------------')
                print(f'parse_link: {count} in {len_link}')
                print(f"Есть: {link}")
            count += 1


class PareserB2Bcenter():
    ''' Запуск парсера на b2b-center.ru '''

    def __init__(self):
        print('-------------------------------------')
        print('PareserB2Bcenter')
        self.json = json_work.JsonWork()

    def init_browser(self, url):
        ''' Получение страницы '''
        print('init_browser')
        options = Options()
        options.headless = True
        driver = 'C:/webdriver/geckodriver'
        browser = webdriver.Firefox(
            options=options, executable_path=driver)
        # Переход на страницу входа
        browser.implicitly_wait(10)
        browser.get(url)
        browser.implicitly_wait(10)
        page = browser.page_source
        browser.quit()
        return page

    def click_elem_xpath(self, driver, xpath):
        """ Нажать на элемент по xpath """
        elem = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", elem)

    def send_text_xpath(self, driver, xpath, text):
        """ Добавить текст в поле по xpath """
        elem = driver.find_element_by_xpath(xpath)
        elem.send_keys(text)

    def soup_get_urls_lot(self, page):
        """ Получение ссылок """
        print('soup_get_urls_lot')
        soup = BeautifulSoup(page, 'html5lib')
        tables = soup.find_all('a', class_="search-results-title")
        urls_lot = []
        for row in tables:
            link = 'https://www.b2b-center.ru' + row.get('href')
            urls_lot.append(link.split('/#btid')[0])
        return urls_lot

    def parse_links_sale(self, url, count, len_link):
        """ Парсинг сайта с url где www.tektorg.ru """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        json_data = self.json.open_json('temp.json')
        page = self.init_browser(url)
        soup = BeautifulSoup(page, 'html5lib')
        category = 'lots'

        # Площадка
        tag = 'platform'
        val = 'www.b2b-center.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.find('td', text=re.compile(
            'Организатор'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # # Способ размещения
        tag = 'placement_method'
        elem = soup.find(itemprop="headline")
        del_txt = elem.find('div', class_="s2")
        if elem == None:
            val = '---'
        else:
            txt1 = elem.get_text()
            txt2 = del_txt.get_text()
            val = txt1.replace(txt2, '')
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.find(itemprop="headline")
        del_txt = elem.find('div', class_="s2")
        if elem == None:
            val = '---'
        else:
            txt1 = elem.get_text()
            txt2 = del_txt.get_text()
            val = txt2.replace(txt1, '')
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.find('td', text=re.compile(
            'Адрес места поставки товара, проведения работ'))
        if elem == None:
            val = '---'
        else:
            val = elem.parent.select(
                'td')[1].get_text().replace('<br />', '\n')
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.find('td', text=re.compile(
            'Общая начальная стоимость'))
        if elem == None:
            elem = soup.find('td', text=re.compile(
                'Общая стоимость'))
            if elem == None:
                elem = soup.find('td', text=re.compile(
                    'Начальная цена'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.select('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала подачи заявок
        tag = 'date_start'
        elem = soup.find('td', text=re.compile(
            'Дата публикации'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата окончания подачи заявок
        tag = 'date_end'
        elem = soup.find('td', text=re.compile(
            'Дата окончания подачи'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала торговой сессии
        tag = 'date_trading'
        elem = soup.find('td', text=re.compile(
            'Дата начала процедуры'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата рассмотрения заявок
        tag = 'date_consideration'
        elem = soup.find('td', text=re.compile(
            'Дата рассмотрения'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('td')[1].get_text()
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # # Дата подведения итогов
        # tag = 'date_summarizing'

    def main(self, url, ids):
        """  """
        page = self.init_browser(url)
        links = self.soup_get_urls_lot(page)
        len_link = len(links)
        count = 1
        for link in links:
            if link not in ids:
                # print('-------------------------------------')
                # print(f'parse_link: {count} in {len_link}')
                # print(f"Новый: {link}")
                self.parse_links_sale(link, count, len_link)
            else:
                print('-------------------------------------')
                print(f'parse_link: {count} in {len_link}')
                print(f"Есть: {link}")
            count += 1


class PareserEtpgpb():
    ''' Запуск парсера на etpgpb.ru '''

    def __init__(self):
        print('-------------------------------------')
        print('PareserEtpgpb')
        self.json = json_work.JsonWork()

    def init_browser(self, url):
        ''' Получение страницы '''
        print('init_browser')
        options = Options()
        options.headless = True
        driver = 'C:/webdriver/geckodriver'
        browser = webdriver.Firefox(
            options=options, executable_path=driver)
        # Переход на страницу входа
        browser.implicitly_wait(10)
        browser.get(url)
        browser.implicitly_wait(10)
        page = browser.page_source
        browser.quit()
        return page

    def click_elem_xpath(self, driver, xpath):
        """ Нажать на элемент по xpath """
        elem = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", elem)

    def send_text_xpath(self, driver, xpath, text):
        """ Добавить текст в поле по xpath """
        elem = driver.find_element_by_xpath(xpath)
        elem.send_keys(text)

    def soup_get_urls_lot(self, page):
        """ Получение ссылок """
        print('soup_get_urls_lot')
        soup = BeautifulSoup(page, 'html5lib')
        tables = soup.find_all('div', class_="procedure__info")
        urls_lot = []
        for row in tables:
            urls_lot.append('https://etpgpb.ru' + row.find(
                'a', class_='procedure__link procedure__infoTitle').get('href'))
        return urls_lot

    def parse_links_sale(self, url, count, len_link):
        """ Парсинг сайта с url где www.tektorg.ru """
        print('-------------------------------------')
        print(f'parse_link: {count} in {len_link}')
        print(f'Новый: {url}')
        json_data = self.json.open_json('temp.json')
        page = self.init_browser(url)
        soup = BeautifulSoup(page, 'html5lib')
        category = 'lots'

        # Площадка
        tag = 'platform'
        val = 'etpgpb.ru'
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Ссылка
        tag = 'link'
        val = url
        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Организация
        tag = 'customer_lot'
        elem = soup.find('p', text=re.compile(
            'Продавец / инициатор продажи'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Способ размещения
        tag = 'placement_method'
        elem = soup.find('p', text=re.compile(
            'Номер извещения'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Наименование лота
        tag = 'name_lot'
        elem = soup.find('p', text=re.compile(
            'Наименование процедуры'))
        if elem == None:
            elem = soup.find('p', text=re.compile(
                'Наименование закупки'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Место нахождения
        tag = 'location'
        elem = soup.find('p', text=re.compile(
            'Адрес местонахождения'))

        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Стоимость
        tag = 'price'
        elem = soup.find('p', text=re.compile(
            'Начальная цена'))
        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала подачи заявок
        tag = 'date_start'
        elem = soup.find('p', text=re.compile(
            'Дата и время начала срока подачи заявок'))
        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата окончания подачи заявок
        tag = 'date_end'
        elem = soup.find('p', text=re.compile(
            'Дата окончания срока рассмотрения заявок'))
        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # Дата начала торговой сессии
        tag = 'date_trading'
        elem = soup.find('p', text=re.compile(
            'Дата и время проведения'))
        if elem == None:
            val = '---'
        else:
            val = elem.parent.find_all('p')[1].get_text()

        json_data = self.json.add_value_list(
            json_data, category, url, tag, val)
        self.json.save_json('temp.json', json_data)

        # # Дата рассмотрения заявок
        # tag = 'date_consideration'

        # # Дата подведения итогов
        # tag = 'date_summarizing'

    def main(self, url, ids):
        """  """
        page = self.init_browser(url)
        links = self.soup_get_urls_lot(page)
        len_link = len(links)
        count = 1
        for link in links:
            if link not in ids:
                self.parse_links_sale(link, count, len_link)
            else:
                print('-------------------------------------')
                print(f'parse_link: {count} in {len_link}')
                print(f"Есть: {link}")
            count += 1


if __name__ == '__main__':
    pass
