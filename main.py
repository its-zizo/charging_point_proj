import json
import datetime
import os

print ('Welcome To Charging Point Management System!')

def File_Generator ():
    """
    description : This function create new json file every day.
    """
    todayS = str (datetime.date.today())
    fileName = f'data/clients_{todayS}.json'
    return fileName

def import_data():
    """
    description : This function import json file data.
    """
    fileName = File_Generator()
    if not os.path.exists(fileName):
         with open(fileName, 'w') as file:
             json.dump({},file , indent=4)
    with open (fileName,'r') as file:
         return json.load(file)

#I'll complete this function ASAP.
    #Done

def save_data(data):
    """
    description : This function save client's data in json file.
    """
    fileName = File_Generator()
    with open(fileName , 'w') as file:
        json.dump(data ,file , indent=4 )


def Add_New_Client(name , device , price):
    """
    input : name: client's Name
    select: device
    output : client's ID , client's Name , devices , total Price
    """
    
    while True:
        print("1.Smart Phone")
        print("2.Small Battery")
        print("3.Large Battery")
        print("4.Laptop")
        print("5.PowerBank")
        selection =   input('Please select device number:') 
        if selection == '4' or selection == '5':
            price +=2
            if selection == '4':
                device.append("Laptop")
            else:
                device.append("PowerBank")
            break

        elif selection == '1' or selection == '2' or selection == '3':
            
                    while True:
                        print("\nis your device with charger?")
                        print('1.Yes')
                        print('2.No')
                        ans =  input('Please type a number: ') 
                        if ans == '1' :
                            if selection == '1':
                                device.append("Phone with charger")
                                price +=1
                            elif selection == '2':
                                device.append("Small Battery with charger")
                                price +=2
                            else:
                                device.append("Large Battery with charger")
                                price +=3
                            break
                        elif ans == '2':
                            if selection == '1':
                                device.append("Phone without charger")
                                price +=2
                            elif selection == '2':
                                device.append("Small Battery without charger")
                                price +=3
                            else:
                                device.append("Large Battery without charger")
                                price +=4
                            break
                                
                        else:
                            print ('\nPlease Select 1 or 2!')

                    break
                
        else:
            print("\nPlease Type a number between 1-5!")

    while True:

        print("\n1.Yes")
        print("2.No")
        answer = input('Do You want to add another device? ')
        if answer == '1':
            Add_New_Client(name , device , price)
        elif answer == '2':
            clientInfo = {
                'client name' : name,
                'devices' : device,
                'price' : price
                }
            print (f'name: {name}')
            print ('devices:', ','.join(device))
            print (f'Total Price: {price}')

            while True:
                print("\n1.Yes")
                print("2.No")
                ans = input (f'Are you sure that you want to add the client {name}?')
                if ans == '1':
                    data = import_data()
                    id = len(data) +1
                    data[id] = clientInfo
                    save_data(data)
                    print (f'\n{name} Added Successfully!')
                    print (f"{name}'s ID : {id}")
                    anyKey = input ("\nPlease press any key to continue. ")
                    main()
                elif ans == "2":
                    main()
                else:
                    print ("\nPlease type 1 or 2!")
            break
        else:
            print ('\nYou can only select 1 to add new device or 2 to go to the next screen!')

   
 #Next function : profit Tracker for 'Profit' Section.


def main():
    print ("1.Add New Client")
    print ("2.ID Search")
    print ("3.Profit")
    print ("4.Exit")
    
    choice = input("\nPlease select an option: ").strip()
    if choice == '1':
        print ('\n---Add New Client---')
        name = input ("Please Enter client's Name: ").strip()
        device = []
        price = 0
        Add_New_Client(name, device , price)


main()