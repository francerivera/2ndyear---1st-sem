def get_fare(vehicle, type_person):
    fare_rates = {
        "jeepney": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
        "tricycle (special)": {"regular": 50.00, "student": 40.00, "senior citizen": 38.00},
        "bus": {"regular": 12.00, "student": 10.00, "senior citizen": 9.50},
    }
    
    return fare_rates.get(vehicle, {}).get(type_person, "invalid input")

def main():
    while True:
        print("Select a vehicle type:\n(1) Jeepney\n(2) Tricycle (Special)\n(3) Bus\n(4) EXIT")
        vehicle_choice = input("Enter your choice: ").lower()
        
        if vehicle_choice == "1":
            vehicle = "jeepney"
        elif vehicle_choice == "2":
            vehicle = "tricycle (special)"
        elif vehicle_choice == "3":
            vehicle = "bus"
        elif vehicle_choice == "4":
            break
        else:
            print("Invalid input. Please try again.")
            continue
        
        print("Select the type of person:\n(1) Regular\n(2) Student\n(3) Senior Citizen\n(4) EXIT")
        person_choice = input("Enter your choice: ").lower()
        
        if person_choice == "1":
            type_person = "regular"
        elif person_choice == "2":
            type_person = "student"
        elif person_choice == "3":
            type_person = "senior citizen"
        elif person_choice == "4":
            break   
        else:
            print("Invalid input. Please try again.")
            continue
        
        fare = get_fare(vehicle, type_person)
        
        if fare == "invalid input":
            print("Invalid vehicle or type of person. Please try again.")
        else:
            print(f"The fare for a {type_person} on a {vehicle} is: PHP {fare:.2f}")


main()
