import csv
from groq import Groq
from apikey import key


class Inventory:
    def __init__(self,name,barcode,price,stock=0):
        self.name = name
        self.barcode = barcode
        self.price = float(price)
        self.stock = float(stock)

    def increase_stock(self,amount):
        self.stock += amount

    def decrease_stock(self, amount):
        self.stock -= amount

    def get_report(self):
        if float(self.stock) == 0:
            return f"{self.name}: Out of Stock"
        elif float(self.stock) <= 1:
            return f'Low Stock: {self.name} has only {self.stock} remaining'
        else:
            return f'You have {self.stock} left of {self.name}'

    def __repr__(self):
        return [self.name,self.barcode,self.price,self.stock]


def stock_report(inventory_list): #takes in list of inventory objects, returns reports of inventory
    for item in inventory_list:
        print(item.get_report())


def csv_to_list():
    # with open('inventory.csv', 'r') as file:
    #     csv_reader = csv.reader(file)
    #     data_list = []
    #     for row in csv_reader:
    #         if row[1] != 'barcode':
    #             item = Inventory(row[0],row[1],row[2],row[3])
    #             data_list.append(item)
    f = open('inventory.csv','r')
    csv_reader = csv.reader(f)
    data_list = []
    for row in csv_reader:
        if row[1] != 'barcode':
                item = Inventory(row[0],row[1],row[2],row[3])
                data_list.append(item)
    f.close()
    return data_list


def inventory_save(list):
    #first, convert object list to regular list
    new_list = [['name','barcode','price','stock']]
    for item in list:
        item = item.__repr__()
        new_list.append(item)
    #convert list into csv file to save progress
    with open('inventory.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in new_list:
            csv_writer.writerow(row)


def low_stock(inventory_list):
    for item in inventory_list:
        if int(item.stock) <= 1:
            print(item.get_report())


def find_prices(low_items):
    item_list = ''
    for item in low_items:
        item_list+=item.name
    prompt = f'give me all deals and their prices for these items at walmart.com {item_list}'
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(messages=[{'role':'user','content':prompt}],model='llama-3.1-8b-instant')
    print(chat_completion.choices[0].message.content)


def stock_editor(inventory_list):
    edit_item = input('Which item would you like to edit?: ')
    increase_decrease = input('Would you like to increase or decrease stock?')
    if increase_decrease == 'increase':
        i = input('By how much would you like to increase it?: ')
        for item in inventory_list:
            if item.name == edit_item:
                edit_item = item
        edit_item.increase_stock(float(i))
    if increase_decrease == 'decrease':
        i = input('By how much would you like to decrease it?: ')
        for item in inventory_list:
            if item.name == edit_item:
                edit_item = item
        edit_item.decrease_stock(float(i))


def main():
    inventory_list = csv_to_list()
    while True:
        print("Welcome to your Personal Inventory Manager")
        answer = input('Would you like to see current inventory? (y/n)')
        if answer == 'y':
            stock_report(inventory_list)
        request = input("What would you like to do?\n"
                          "1) Add new Item\n"
                          "2) View low Stock\n"
                          "3) Edit Stock\n"
                          "4) Delete item from inventory\n"
                          "5) Save/Exit Program\n")

        if request == '5':#Save/Exit Program
            inventory_save(inventory_list)
            print('Thanks!')
            return False

        elif request == '1': #New Item
            name = input("Enter the Item: ")
            barcode = input("Enter the Barcode #")
            price = float(input("Enter Price: $"))
            stock = float(input("Enter amount of item in Stock: "))
            if stock >= 100:
                print('Invalid Input: Stock must be less that 100')
                stock = input("Enter amount of item in Stock: ")
            new_item = Inventory(name,barcode,price,stock)
            inventory_list.append(new_item)

        elif request == '2': #Low Stock Items
            low_stock(inventory_list)
            #Maybe put restocking prices/links?
            low_stock_items = []
            for item in inventory_list:
                if item.stock >= 0:
                    low_stock_items.append(item)
            find_prices(low_stock_items)

        elif request == '3': #Increase/Decrease stock
            stock_report(inventory_list)
            stock_editor(inventory_list)

        elif request == '4': #Delete item
            edit_item = input('What item would you like to delete?: ')
            for x in range(len(inventory_list)-1):
                if inventory_list[x].name == edit_item:
                    inventory_list.pop(x)
                else:
                    print(f'{edit_item} not found:(')

        else:
            print('Invalid input: must be 1-4')


if __name__ == '__main__':
    main()