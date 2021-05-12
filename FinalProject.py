#Name: Nguyen Vo
#ID: 1673509



import csv                         #working with csv files
from datetime import datetime      #this will allow accessing time for later use

#initialize class for every output
class InventoryReports:
    def __init__(self, item_list):
        self.item_list = item_list      #provide list to create new file


    #Part a
    #Create FullInventory.csv for entire inventory
    #Following order ID, manufacture name, item type, price, service date, damaged
    def fullInventory(self):
        with open('FullInventory.csv', 'w') as file:
            items = self.item_list
            keys = sorted(items.keys(), key=lambda x: items[x]['manufacturer'])              #sorted alphabetically by manufacture
            for item in keys:
                id = item
                manufacture = items[item]['manufacturer']
                itemType = items[item]['item_type']
                price = items[item]['price']
                serviceDate = items[item]['service_date']
                damaged = items[item]['damaged']
                file.write('{},{},{},{},{},{}\n'.format(id, manufacture, itemType, price, serviceDate, damaged))

    #Part b
    #Create Inventorylist for each item type
    #This will produce 3 seperate cvs files: PhoneInventory, TowerInventory, LaptopInventory
    #Following order ID, manufacture, price, service date, and if damaged
    def inventoryList(self):
        items = self.item_list
        types = []
        keys = sorted(items.keys())                 #the items sorted by ID
        for item in items:
            itemType = items[item]['item_type']
            if itemType not in types:
                types.append(itemType)
        for type in types:
            file_name = type.capitalize() + 'Inventory.csv'
            with open('Inventorylist' + '-' + file_name, 'w') as file:
                for item in keys:
                    id = item
                    manufacture = items[item]['manufacturer']
                    price = items[item]['price']
                    serviceDate = items[item]['service_date']
                    damaged = items[item]['damaged']
                    itemType = items[item]['item_type']
                    if type == itemType:
                        file.write('{},{},{},{},{}\n'.format(id, manufacture, price, serviceDate, damaged))

    #Part c
    #Crate PastServiceDateInventory.csv
    #Following order ID, manufacture, item type, price, service date
    def pastService(self):
        items = self.item_list
        keys = sorted(items.keys(), key=lambda x: datetime.strptime(items[x]['service_date'], "%m/%d/%Y").date())        #sorted date from oldest to most recent
        with open('PastServiceDateInventory.csv', 'w') as file:
            for item in keys:
                id = item
                manufacture = items[item]['manufacturer']
                itemType = items[item]['item_type']
                price = items[item]['price']
                serviceDate = items[item]['service_date']
                damaged = items[item]['damaged']
                today = datetime.now().date()
                service_expiration = datetime.strptime(serviceDate, "%m/%d/%Y").date()
                expired = service_expiration < today
                if expired:                                                      #list if it damaged
                    file.write('{},{},{},{},{},{}\n'.format(id, manufacture, itemType, price, serviceDate, damaged))

    #Part d
    #Create DamagedInventory.csv for items that are damaged
    #Following order ID, manfacture, item type, price, service date
    def damagedInventory(self):
        items = self.item_list
        #order to file based on price
        keys = sorted(items.keys(), key=lambda x: items[x]['price'], reverse=True)     #order being reserved so that it sort from expensive to cheap
        with open('DamagedInventory.csv', 'w') as file:
            for item in keys:
                id = item
                manufacture = items[item]['manufacturer']
                itemType = items[item]['item_type']
                price = items[item]['price']
                serviceDate = items[item]['service_date']
                damaged = items[item]['damaged']
                if damaged:                                      #condition to write for damaged items
                    file.write('{},{},{},{},{}\n'.format(id, manufacture, itemType, price, serviceDate))


if __name__ == '__main__':           #main program
    items = {}
    files = ['ManufacturerList(1).csv', 'PriceList(1).csv', 'ServiceDatesList(1).csv']        #create list of input files and read every files
    for file in files:
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                item_id = line[0]
                if file == files[0]:
                    items[item_id] = {}
                    manufacture = line[1]
                    itemType = line[2]
                    damaged = line[3]
                    items[item_id]['manufacturer'] = manufacture.strip()
                    items[item_id]['item_type'] = itemType.strip()
                    items[item_id]['damaged'] = damaged
                elif file == files[1]:
                    price = line[1]
                    items[item_id]['price'] = price
                elif file == files[2]:
                    serviceDate = line[1]
                    items[item_id]['service_date'] = serviceDate

    inventory = InventoryReports(items)
    # Create all the output files
    inventory.fullInventory()
    inventory.pastService()
    inventory.damagedInventory()
    inventory.inventoryList()

    # Part 2 start here
#store the data in a dictionary

data = {"id" : [1167234, 2347800, 2390112, 9034210, 7346234, 1009453, 3001265],

"manufacturer":["Apple", "Apple", "Dell", "Dell", "Lenovo", "Lenovo", "Samsung"],

"type" : ["phone", "laptop", "laptop", "tower", "laptop", "tower", "phone"],

"price": [534, 999, 799, 345, 239, 599, 1200],

"date": [2/1/2022, 7/3/2020, 7/2/2020, 5/27/2020, 9/1/2021, 10/1/2021, 12/1/2023],

"condition": [' ', ' ', ' ', ' ', ' ', 'damaged', ' ', ' ']}

#create while loop to ask user input
#continue prompt user input until q
while True:
    user_input = input("Enter item or q to quit: ")
    if user_input == "q":
        break
    item = ""
    types = ""
    for i in data["manufacturer"]:
        if i in user_input:
            item = i
    for i in data["type"]:
        if i in user_input:
            types = i
    if(item == "" or types == ""):                             #checking for bad input otherwise procceed to print message of item
        print("No such item in inventory")
    else:
        details = ["", "", "", 0]
        for i in range(len(data["id"])):
            if(data["manufacturer"][i] == item and data["type"][i] == types):
                if(details[3] < data["price"][i]):
                    details[0] = data["id"][i]
                    details[1] = data["manufacturer"][i]
                    details[2] = data["type"][i]
                    details[3] = data["price"][i]
        print("Your item is " + str(details[0]) + " " + str(details[1]) + " " + str(details[2]) + " " + str(details[3]))

    #create a list of other recommended items base on user manufacturer input
    consider = []
    for i in range(len(data["id"])):
        if(data["type"][i] == types and data["manufacturer"][i] != item):
            consider.append([data["id"][i], data["manufacturer"][i], data["type"][i], data["price"][i]])
    if(len(consider) != 0):
        print("You may, also, consider:")
        for i in range(len(consider)):
            print(str(consider[i][0]) + " " + consider[i][1] + " " + consider[i][2] + " " + str(consider[i][3]))



