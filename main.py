import json
import datetime
import os
from collections import defaultdict

class ChargingPointSystem:
    def _init_(self):
        self.data_dir = "data"
        self.receipts_dir = "receipts"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.receipts_dir, exist_ok=True)
        
        # Device configuration with prices
        self.device_types = {
            '1': {'name': 'Mobile', 'with_charger': 5, 'without_charger': 7},
            '2': {'name': 'Small Battery', 'with_charger': 7, 'without_charger': 10},
            '3': {'name': 'Medium Battery', 'with_charger': 10, 'without_charger': 15},
            '4': {'name': 'Large Battery', 'with_charger': 15, 'without_charger': 20},
            '5': {'name': 'Laptop', '65w+': 20, '65w-': 15, 'without_charger': 25},
            '6': {'name': 'PowerBank', 'price': 10},
            '7': {'name': 'Other Device', 'custom': True}
        }

    def run(self):
        """Main application entry point"""
        print("Welcome to Charging Point Management System!")
        while True:
            self.show_main_menu()
            choice = self.get_valid_input("Select option (1-4): ", ['1', '2', '3', '4'])
            
            if choice == '1':
                self.add_client()
            elif choice == '2':
                self.find_client()
            elif choice == '3':
                self.daily_profit()
            elif choice == '4':
                if self.confirm_action("Are you sure you want to exit?"):
                    print("Goodbye!")
                    break

    def show_main_menu(self):
        """Display the main menu"""
        print("\nMain Menu:")
        print("1. Add New Client")
        print("2. Find Client")
        print("3. Daily Profit Report")
        print("4. Exit")

    def add_client(self):
        """Add a new client with devices"""
        print("\n--- Add New Client ---")
        name = self.get_valid_input("Client name: ", min_length=1)
        if not name:
            return

        devices = []
        total_price = 0
        
        while True:
            device, price = self.select_device()
            devices.append(device)
            total_price += price
            
            if not self.confirm_action("Add another device?"):
                break
        
        client_data = {
            'name': name,
            'devices': devices,
            'price': total_price,
            'checkout': False,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.confirm_action(f"Confirm adding client {name}?"):
            client_id = self.save_client(client_data)
            print(f"\nClient added successfully! ID: {client_id}")
            print(f"Total: {total_price} NIS")
            self.generate_receipt(client_id, client_data)
            input("\nPress Enter to continue...")

    def select_device(self):
        """Select a device and calculate its price"""
        print("\nSelect device type:")
        for num, device in self.device_types.items():
            print(f"{num}. {device['name']}")
        
        choice = self.get_valid_input("Enter device number (1-7): ", list(self.device_types.keys()))
        device_info = self.device_types[choice]
        
        if choice == '5':  # Laptop
            return self.handle_laptop(device_info)
        elif choice == '6':  # PowerBank
            return (device_info['name'], device_info['price'])
        elif choice == '7':  # Other device
            return self.handle_custom_device()
        else:
            return self.handle_standard_device(device_info)

    def handle_laptop(self, device_info):
        """Special handling for laptops"""
        if self.confirm_action("With charger?"):
            wattage = self.confirm_action("65W+ charger?", yes_label="Yes", no_label="No")
            device_name = f"{device_info['name']} with {'65W+' if wattage else '65W-'} charger"
            price = device_info['65w+'] if wattage else device_info['65w-']
        else:
            device_name = f"{device_info['name']} without charger"
            price = device_info['without_charger']
        return (device_name, price)

    def handle_standard_device(self, device_info):
        """Handle standard devices"""
        if self.confirm_action("With charger?"):
            device_name = f"{device_info['name']} with charger"
            price = device_info['with_charger']
        else:
            device_name = f"{device_info['name']} without charger"
            price = device_info['without_charger']
        return (device_name, price)

    def handle_custom_device(self):
        """Handle custom device entry"""
        device_name = self.get_valid_input("Device name: ", min_length=1)
        price = float(self.get_valid_input("Charging price: ", is_numeric=True))
        return (device_name, price)

    def find_client(self):
        """Find and display client information"""
        print("\n--- Find Client ---")
        client_id = input("Enter client ID: ").strip()
        data = self.load_data()
        
        if client_id not in data:
            print("Client not found!")
            input("\nPress Enter to continue...")
            return

        client = data[client_id]
        self.display_client_info(client_id, client)
        
        if not client['checkout']:
            if self.confirm_action("Mark as delivered?"):
                client['checkout'] = True
                self.save_data(data)
                print("Status updated to delivered!")
        
        input("\nPress Enter to continue...")

    def display_client_info(self, client_id, client):
        """Display client information"""
        print(f"\nClient ID: {client_id}")
        print(f"Name: {client['name']}")
        print(f"Devices: {', '.join(client['devices'])}")
        print(f"Total: {client['price']} NIS")
        print(f"Status: {'Delivered' if client['checkout'] else 'Pending'}")

    def daily_profit(self):
        """Display daily profit report"""
        print("\n--- Daily Profit Report ---")
        data = self.load_data()
        
        total = 0
        pending = 0
        device_counts = defaultdict(int)

        for client in data.values():
            if client['checkout']:
                total += client['price']
            else:
                pending += client['price']
            
            for device in client['devices']:
                device_counts[device] += 1

        print(f"Total Profit: {total} NIS")
        print(f"Pending Amount: {pending} NIS")
        
        print("\nDevices Charged Today:")
        for device, count in device_counts.items():
            print(f"- {device}: {count}")
        
        input("\nPress Enter to continue...")

    # Data persistence methods
    def load_data(self):
        """Load data from JSON file"""
        file_path = self.get_data_file_path()
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

    def save_data(self, data):
        """Save data to JSON file"""
        try:
            with open(self.get_data_file_path(), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def save_client(self, client_data):
        """Save client data and return ID"""
        data = self.load_data()
        client_id = str(len(data) + 1)
        data[client_id] = client_data
        self.save_data(data)
        return client_id

    def generate_receipt(self, client_id, client_data):
        """Generate receipt for client"""
        receipt_content = f"""
        ==============================
        CHARGING POINT RECEIPT
        ==============================
        Client ID: {client_id}
        Name: {client_data['name']}
        Date: {client_data['timestamp']}
        
        Devices:
        {''.join(f'- {device}\n' for device in client_data['devices'])}
        
        Total Amount: {client_data['price']} NIS
        Status: {'Delivered' if client_data['checkout'] else 'Pending'}
        ==============================
        Thank you for your business!
        ==============================
        """
        
        receipt_file = os.path.join(self.receipts_dir, f"receipt_{client_id}.txt")
        with open(receipt_file, 'w', encoding='utf-8') as f:
            f.write(receipt_content)

    # Utility methods
    def get_data_file_path(self):
        """Get path to today's data file"""
        today = datetime.date.today().isoformat()
        return os.path.join(self.data_dir, f"clients_{today}.json")

    def get_valid_input(self, prompt, valid_choices=None, min_length=0, is_numeric=False):
        """Get validated user input"""
        while True:
            user_input = input(prompt).strip()
            
            if min_length and len(user_input) < min_length:
                print(f"Input must be at least {min_length} characters")
                continue
                
            if valid_choices and user_input not in valid_choices:
                print(f"Please enter one of: {', '.join(valid_choices)}")
                continue
                
            if is_numeric and not user_input.replace('.', '').isdigit():
                print("Please enter a valid number")
                continue
                
            return user_input

    def confirm_action(self, message, yes_label="Yes", no_label="No"):
        """Get confirmation from user"""
        response = self.get_valid_input(
            f"{message} ({yes_label[0].lower()}/{no_label[0].lower()}): ",
            [yes_label[0].lower(), no_label[0].lower()]
        )
        return response == yes_label[0].lower()

if _name_ == "_main_":
    system = ChargingPointSystem()
    system.run()
