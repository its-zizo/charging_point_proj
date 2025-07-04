import json
import datetime
import os

print ('مرحباً بك في نظام إدارة نقطة الشحن!')

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
         with open(fileName, 'w' , encoding='utf-8') as file:
             json.dump({},file , indent=4 , ensure_ascii=False)
    with open (fileName,'r' , encoding='utf-8') as file:
         return json.load(file)

#I'll complete this function ASAP.
    #Done

def save_data(data):
    """
    description : This function save client's data in json file.
    """
    fileName = File_Generator()
    with open(fileName , 'w' , encoding='utf-8') as file:
        json.dump(data ,file , indent=4 , ensure_ascii=False)


def Add_New_Client(name , device , price):
    """
    input : name: client's Name
    select: device
    output : client's ID , client's Name , devices , total Price
    """
    
    while True:
        print("1.جوال")
        print("2.بطارية حجم صغير")
        print("3.بطارية حجم وسط")
        print("4.بطارية حجم كبير")
        print("5.لابتوب")
        print("6.بوربانك")
        print ('7.إضافة جهاز غير معرَف')
        selection =   input('الرجاء اختيار رقم الجهاز المراد شحنه: ') 
        if selection == '6':
            device.append("بوربانك")
            price +=2
            break

        elif selection == '1' or selection == '2' or selection == '3' or selection =='4' or selection == '5':
            
                    while True:
                        print("\nهل مرفق شاحن مع الجهاز؟")
                        print('1.نعم')
                        print('2.لا')
                        ans =  input('الرجاء اختيار رقم: ') 
                        if ans == '1' :
                            if selection == '1':
                                device.append("جوال مع شاحن")
                                price +=1

                            elif selection == '2':
                                device.append("بطارية حجم صغير مع شاحن")
                                price +=2

                            elif selection == '5':
                                while True:
                                    print ("هل شاحنك 65 واط فأعلى؟")
                                    print('1.نعم')
                                    print('2.لا')
                                    isCharger = input ("الرجاء اختيار رقم: ")
                                    if isCharger == "1":
                                        device.append("لابتوب مع شاحن أعلى من 65 واط")
                                        price +=3
                                        break
                                    elif isCharger == '2':
                                        device.append("لابتوب مع شاحن أقل من 65 واط")
                                        price +=2
                                        break
                                    else:
                                        print ("ادخال خاطئ! الرجاء اختيار 1 او 2")

                            elif selection == '3':
                                device.append('بطارية حجم وسط مع شاحن')
                                price +=3
                            else:
                                device.append("بطارية حجم كبير مع شاحن")
                                price +=4
                            break
                        elif ans == '2':
                            if selection == '1':
                                device.append("جوال بدون شاحن")
                                price +=2
                            elif selection == '5':
                                device.append("لابتوب بدون شاحن")
                                price +=4
                            elif selection == '2':
                                device.append("بطارية حجم صغير بدون شاحن")
                                price +=4
                            elif selection == '3':
                                device.append('بطارية حجم متوسط بدون شاحن')
                                price +=5
                            else:
                                device.append("بطارية حجم كبير بدون شاحن")
                                price +=6
                            break
                                
                        else:
                            print ('\nادخال خاطئ! الرجاء اختيار رقم الخيار الصحيح')

                    break
        elif selection == '7':
            deviceName = input ("أدخل اسم الجهاز المراد شحنه: ")
            customPrice = int (input ('تكفلة الشحن: '))
            device.append(deviceName)
            price += customPrice
            break
                
        else:
            print("\nالرجاء ادخال رقم من 1-5!")

    while True:

        print("\n1.نعم")
        print("2.لا")
        answer = input('هل تريد اضافة جهاز اخر؟ ')
        if answer == '1':
            Add_New_Client(name , device , price)
        elif answer == '2':
            clientInfo = {
                'client name' : name,
                'devices' : device,
                'price' : price,
                'checkout' :False
                }
            print (f'\nالاسم: {name}')
            print ('الأجهزة:', ','.join(device))
            print (f'تكلفة الشحن: {price} شيكل')

            while True:
                print("\n1.نعم")
                print("2.لا")
                ans = input (f'هل أنت متأكد من اضافة {name} للنظام ؟ ')
                if ans == '1':
                    data = import_data()
                    id = len(data) +1
                    data[id] = clientInfo
                    save_data(data)
                    print (f'\nتم اضافة {name} بنجاح!')
                    print (f"الرقم التسلسلي الخاص بالزبون {name} هو  : {id}")
                    anyKey = input ("\nاضغط على أي مفتاح للذهاب للواجهة التالية.  ")
                    main()
                elif ans == "2":
                    main()
                else:
                    print ("\nادخال خاطئ الرجاء اختيار ")
            break
        else:
            print ('\nاختر 1 لاضافة جهاز اخر او 2 للذهاب للشاشة القادمة')

def Find_My_Clients():
    data = import_data()
    id =input ("الرجاء ادخال الرقم التسلسلي الخاص بالزبون: ")

    if id in data.keys():
        print ('تم ايجاد الزبون!')
        clientInfo = list (data[id].values())
        print (f'\nالاسم: {clientInfo[0]}')
        print ('الأجهزة:', ','.join(clientInfo[1]))
        print (f'اجمالي التكلفة: {clientInfo[2]} شيكل')

        if clientInfo[-1] == False:
            while True:
                print ('\n---المحاسبة---')
                print("\n1.تم التسليم.")
                print("2.انتقل للشاشة السابقة.")
                print("3.الرجوع للقائمة الرئيسية.")
                ans = input ("اختر رقم الخيار :")
                if ans == '1':
                    fileName = File_Generator()
                    data[id].pop('checkout')
                    data[id]['checkout'] = True
                    save_data(data)
                    print ('تمت عملية التسليم بنجاح!')
                    main()
                elif ans == '2':
                    Find_My_Clients()
                elif ans == '3':
                    main()
                else:
                    print ("الرجاء اختيار 1 او 2 فقط.")
        else:
            print ('\nتم التسليم بالفعل!')
            input('أدخل أي رقم للرجوع: ')
            main()
    else:
        print ("USER NOT FOUND! , Please check user ID and try again")
        input('press any key to go back: ')
        main()

 #Next function : profit Tracker for 'Profit' Section.
    #Done.
def profit_Tracker():
    data = import_data()
    totalProfit = 0
    pending = 0

    for value in  list(data.values()):
        if value['checkout'] == True:
            totalProfit += value['price']
        else:
            pending += value['price']
        
    print (f'الربح الكلي = {totalProfit} شيكل')
    print (f'الربح المعلَق= {pending} شيكل')
    input('\n أدخل أي رقم للرجوع للقائمة الرئيسية')
    main()


def main():
    print ("\n1.إضافة زبون جديد")
    print ("2.البحث عبر الرقم التسلسلي")
    print ("3.الربح اليومي")
    print ("4.خروج")
    
    choice = input("\nالرجاء كتابة رقم الخيار: ").strip()
    if choice == '1':
        print ('\n---إضافة زبون---')
        name = input ("الرجاء ادخال اسم الزبون: ").strip()
        device = []
        price = 0
        Add_New_Client(name, device , price)

    elif choice == '2':
        print ('\n---البحث---')
        Find_My_Clients()

    elif choice == '3':
        print ("\n---ربح اليوم---")
        profit_Tracker()

    elif choice == '4':
        while True:
            print ("1.نعم")
            print ("2.لا")
            ans = input ('هل أنت متأكد؟')
        
            if ans == '1':
                print ("مع السلامة!")
                quit()
            elif ans == '2':
                main()
            else:
                print ("ادخال خاطئ!")
    else:
        print ("ادخال خاطئ!")
        main()

main()
