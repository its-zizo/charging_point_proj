import json
import datetime
import os

# def File_Generator ():
"""
    this function create new json file every day
"""
#     todayS = str (datetime.date.today())
#     fileName = f'data/clients_{todayS}.json'
#     return fileName

# def import_data():
"""
    this function import json file data
"""
#     fileName = File_Generator()
#     if not os.path.exists(fileName):
#         with open(fileName, 'w') as file:
#             json.dump({},file , indent=4)
#     with open (fileName,'r') as file:
#         return json.load(file)

#I'll complete this function ASAP.

 # def save_data(data):
"""
    this function save client data in json file
"""
 #     fileName = File_Generator():
 #     with open(fileName , 'w') as file:
 #         json.dump()


def Add_New_Client():
    #Test - I'll Add them later to another function 
    name = input ("Please Enter client's Name: ")
    device = []
    price = 0

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
                        print("is your device with charger?")
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
                            print ('Please Select 1 or 2!')

                    break
                
        else:
            print("Please Type a 1-5 number!")
        #Next step in this func: do you want to add another device?
#function Test
    print (name)
    print (device)
    print (price)
    userInfo = {
        'clientName': name ,
        "devices":device,
        'price':price
    }
    print(userInfo)

print (Add_New_Client())