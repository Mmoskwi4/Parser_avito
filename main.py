import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from storage import Storage


class AvitoPars:
    def __init__(self, url:str, items:list, count:int=100):
        self.url = url
        self.items = items
        self.count = count
        self.id = 1
        self.data = []
        self.context = {'id': int,
                'name': str,
                'price': int,
                'link': str,
                'description': str
                }

        self.storage = Storage(self.context, self.data)

    def __set_up(self):
        self.driver = uc.Chrome()
    
    def __get_url(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']") and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count -= 1

    def __parse_page(self):
        
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in titles:
            self.context = {
                'id': self.id,
                'name': title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text,
                'price': int(title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute('content')),
                'link': title.find_element(By.CSS_SELECTOR, "[itemprop='url']").get_attribute('href'),
                'description': f"{title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text}"
            }
            if any([item.lower() in self.context['description'].lower() for item in self.items]):
                self.data.append(self.context)
                self.storage.create_exel()
                self.storage.save_json()  
                self.id += 1

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    url = str(input("Вставьте ссылку для парса: "))
    items = input("Введите через запятую ключевые слова для поиска: ").split(',')
    print(items)
    count = int(input("Введите количество страниц: "))
    AvitoPars(url=url, items=items, count=count).parse()