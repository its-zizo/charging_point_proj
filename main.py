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

    def file_generator(self, date_str=None):
        if date_str:
            return f'data/clients_{date_str}.json'
        today = datetime.date.today()
        os.makedirs('data', exist_ok=True)
        return f'data/clients_{today}.json'

    def import_data(self, date_str=None):
        file_name = self.file_generator(date_str)
        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def save_data(self, data, date_str=None):
        with open(self.file_generator(date_str), 'w', encoding='utf-8') as file:
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

    def add_loss(self):
        date_str = input("Enter date for the loss (YYYY-MM-DD) or leave empty for today: ").strip()
        if not date_str:
            date_str = str(datetime.date.today())

        file_path = self.file_generator(date_str)
        data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}

        description = input("Enter loss description: ").strip()
        while True:
            try:
                cost = float(input("Enter repair cost: "))
                break
            except ValueError:
                print("Invalid number. Try again.")

        data['_loss'] = {
            'description': description,
            'cost': cost
        }

        self.save_data(data, date_str)
        print(f"Loss recorded for {date_str}. Cost: {cost} ₪")

    def get_daily_profit(self, date_str=None):
        if not date_str:
            date_str = str(datetime.date.today())

        file_path = self.file_generator(date_str)
        if not os.path.exists(file_path):
            print("No data found for this date.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        total = sum(client['price'] for key, client in data.items() if key != '_loss')
        loss = data.get('_loss', {}).get('cost', 0)
        net_profit = total - loss

        print(f"\nProfit Summary for {date_str}:")
        print(f"  Total income : {total} ₪")
        print(f"  Loss recorded: {loss} ₪")
        print(f"  Net profit   : {net_profit} ₪")

    def monthly_profit(self):
        year = input("Enter year (YYYY): ").strip()
        month = input("Enter month (MM): ").strip()

        if not (year.isdigit() and month.isdigit()):
            print("Invalid input.")
            return

        total_income = 0
        total_loss = 0

        for filename in os.listdir('data'):
            if filename.startswith(f'clients_{year}-{month}'):
                with open(f'data/{filename}', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    daily_income = sum(client['price'] for key, client in data.items() if key != '_loss')
                    loss = data.get('_loss', {}).get('cost', 0)
                    total_income += daily_income
                    total_loss += loss

        net_profit = total_income - total_loss

        print(f"\nMonthly Profit Summary for {year}-{month}:")
        print(f"  Total income : {total_income} ₪")
        print(f"  Total losses : {total_loss} ₪")
        print(f"  Net profit   : {net_profit} ₪")

    def run(self):
        while True:
            print("\nMain Menu:")
            print("1. Add New Client")
            print("2. Find/Checkout Client")
            print("3. Daily Profit (Today)")
            print("4. Monthly Profit")
            print("5. Record Loss")
            print("6. Daily Profit for Specific Date")
            print("7. Exit")

            choice = input("Select option (1-7): ")

            if choice == '1':
                self.add_client()
            elif choice == '2':
                print("Find Client functionality")
            elif choice == '3':
                self.get_daily_profit()
            elif choice == '4':
                self.monthly_profit()
            elif choice == '5':
                self.add_loss()
            elif choice == '6':
                date_str = input("Enter date (YYYY-MM-DD): ").strip()
                self.get_daily_profit(date_str)
            elif choice == '7':
                sys.exit()
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    system = ChargingSystem()
    system.run()