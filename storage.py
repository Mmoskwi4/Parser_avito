import json
import csv

class Storage:
    def __init__(self, context:dict, data:list):
         self.context = context
         self.data = data
    
    def create_exel(self):
            with open("items.xls", 'w', newline='', encoding='utf-16') as workbook:
                workbook = csv.writer(workbook, delimiter="\t")
                # Название колонок
                names=list([key.capitalize() for key in self.context.keys()])
                workbook.writerow(names)

                # Заполнение строк
                for i in range(0, len(self.data)):
                    value=list([val for val in self.data[i].values()])
                    workbook.writerow(value)

    def save_json(self):
        with open('items.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)