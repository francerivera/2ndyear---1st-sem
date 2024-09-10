# def get_fare(vehicle, type_person):
#     fare_rates = {
#         "jeepney": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
#         "tricycle (special)": {"regular": 50.00, "student": 40.00, "senior citizen": 38.00},
#         "bus": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
#     }
    
#     return fare_rates.get(vehicle, {}).get(type_person, "invalid input")

# def main():
#     while True:
#         print("Select a vehicle type:\n(1) Jeepney\n(2) Tricycle (Special)\n(3) Bus\n(4) EXIT")
#         vehicle_choice = input("Enter your choice: ").lower()
        
#         if vehicle_choice == "1":
#             vehicle = "jeepney"
#         elif vehicle_choice == "2":
#             vehicle = "tricycle (special)"
#         elif vehicle_choice == "3":
#             vehicle = "bus"
#         elif vehicle_choice == "4":
#             break
#         else:
#             print("Invalid input. Please try again.")
#             continue
        
#         print("Select the type of person:\n(1) Regular\n(2) Student\n(3) Senior Citizen\n(4) EXIT")
#         person_choice = input("Enter your choice: ").lower()
        
#         if person_choice == "1":
#             type_person = "regular"
#         elif person_choice == "2":
#             type_person = "student"
#         elif person_choice == "3":
#             type_person = "senior citizen"
#         elif person_choice == "4":
#             break   
#         else:
#             print("Invalid input. Please try again.")
#             continue
        
#         fare = get_fare(vehicle, type_person)
        
#         if fare == "invalid input":
#             print("Invalid vehicle or type of person. Please try again.")
#         else:
#             print(f"The fare for a {type_person} on a {vehicle} is: PHP {fare:.2f}")

# main()

class FareCalculator:
    def __init__(self):
        self.fare_rates = {
            "jeepney": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
            "tricycle (special)": {"regular": 50.00, "student": 40.00, "senior citizen": 38.00},
            "bus": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
        }

    def get_fare(self, vehicle, person_type):
        return self.fare_rates.get(vehicle, {}).get(person_type, "invalid input")

    def select_vehicle(self):
        while True:
            print("Select a vehicle type:\n(1) Jeepney\n(2) Tricycle (Special)\n(3) Bus\n(4) EXIT")
            choice = input("Enter your choice: ").lower()

            if choice == "1":
                return "jeepney"
            elif choice == "2":
                return "tricycle (special)"
            elif choice == "3":
                return "bus"
            elif choice == "4":
                return None
            else:
                print("Invalid input. Please try again.")

    def select_person_type(self):
        while True:
            print("Select the type of person:\n(1) Regular\n(2) Student\n(3) Senior Citizen\n(4) EXIT")
            choice = input("Enter your choice: ").lower()

            if choice == "1":
                return "regular"
            elif choice == "2":
                return "student"
            elif choice == "3":
                return "senior citizen"
            elif choice == "4":
                return None
            else:
                print("Invalid input. Please try again.")

    def run(self):
        while True:
            vehicle = self.select_vehicle()
            if not vehicle:
                break

            person_type = self.select_person_type()
            if not person_type:
                break

            fare = self.get_fare(vehicle, person_type)
            if fare == "invalid input":
                print("Invalid vehicle or type of person. Please try again.")
            else:
                print(f"The fare for a {person_type} on a {vehicle} is: PHP {fare:.2f}")


fare_calculator = FareCalculator()
fare_calculator.run()




