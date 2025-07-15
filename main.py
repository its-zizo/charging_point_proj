import json
import datetime
import os
import sys


class ChargingSystem:
    def __init__(self):
        print('Welcome to Charging Point Management System!')
        self.device_types = {
            '1': {'name': 'Mobile', 'with_charger': 1, 'without_charger': 2},
            '2': {'name': 'Small Battery', 'with_charger': 2, 'without_charger': 4},
            '3': {'name': 'Medium Battery', 'with_charger': 3, 'without_charger': 5},
            '4': {'name': 'Large Battery', 'with_charger': 4, 'without_charger': 6},
            '5': {'name': 'Laptop', '65w+': 3, '65w-': 2, 'without_charger': 4},
            '6': {'name': 'PowerBank', 'price': 2},
            '7': {'name': 'Custom Device', 'custom': True}
        }

    def file_generator(self):
        today = datetime.date.today()
        os.makedirs('data', exist_ok=True)
        return f'data/clients_{today}.json'

    def import_data(self):
        file_name = self.file_generator()
        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def save_data(self, data):
        with open(self.file_generator(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select_device(self):
        print("\nSelect device type:")
        for num, device in self.device_types.items():
            print(f"{num}. {device['name']}")

        while True:
            choice = input("Enter device number (1-7): ")
            if choice in self.device_types:
                return choice
            print("Invalid choice! Please select 1-7")

    def add_client(self):
        while True:
            name = input("Please enter client name: ").strip()
            if name:
                break
            print("Name cannot be empty!")

        devices = []
        total_price = 0

        while True:
            device_choice = self.select_device()
            device_info = self.device_types[device_choice]

            if device_choice == '6':
                devices.append("PowerBank")
                total_price += device_info['price']
            elif device_choice == '7':
                device_name = input("Enter device name: ")
                while True:
                    try:
                        price = int(input("Enter charging price: "))
                        break
                    except ValueError:
                        print("Invalid price! Please enter a number.")
                devices.append(device_name)
                total_price += price
            else:
                has_charger = input("With charger? (1.Yes 2.No): ")
                if has_charger == '1':
                    if device_choice == '5':
                        wattage = input("65W+ charger? (1.Yes 2.No): ")
                        if wattage == '1':
                            devices.append("Laptop with 65W+ charger")
                            total_price += device_info['65w+']
                        else:
                            devices.append("Laptop with under 65W charger")
                            total_price += device_info['65w-']
                    else:
                        devices.append(f"{device_info['name']} with charger")
                        total_price += device_info['with_charger']
                else:
                    devices.append(f"{device_info['name']} without charger")
                    total_price += device_info['without_charger']

            another = input("Add another device? (1.Yes 2.No): ")
            if another != '1':
                break

        client_data = {
            'name': name,
            'devices': devices,
            'price': total_price,
            'checkout': False,
            'timestamp': datetime.datetime.now().isoformat()
        }

        print(f"\nClient Summary:")
        print(f"Name: {name}")
        print("Devices:")
        for device in devices:
            print(f"- {device}")
        print(f"Total Price: {total_price}")

        confirm = input("Confirm adding client? (1.Yes 2.No): ")
        if confirm == '1':
            data = self.import_data()
            client_id = str(len(data) + 1)
            data[client_id] = client_data
            self.save_data(data)
            print(f"Client added successfully! ID: {client_id}")
            print(f"Total amount: {total_price} AED")
        else:
            print("\nClient addition canceled.")

    def run(self):
        while True:
            print("\nMain Menu:")
            print("1. Add New Client")
            print("2. Find/Checkout Client")
            print("3. Daily Profit")
            print("4. Exit")

            choice = input("Select option (1-4): ")

            if choice == '1':
                self.add_client()
            elif choice == '2':
                print("Find Client functionality")
            elif choice == '3':
                print("Daily Profit functionality")
            elif choice == '4':
                sys.exit()
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    system = ChargingSystem()
    system.run()
