import pickle

class Employee:
    def __init__(self, id, name, role, salary):
        self.id = id
        self.name = name
        self.role = role
        self.__salary = salary

    def display_info(self):
        print(f"""ID: {self.id}
Name: {self.name}
Role: {self.role}
Salary: {self.__salary}""")
    
    def update_attribute(self, attribute_name, new_value):
        if attribute_name == "salary":
            try:
                new_value = float(new_value)
                if new_value <= 0:
                    print("ERROR: Salary must be greater than 0.")
                    return False
                self.__salary = new_value
                return True
            except ValueError:
                print("ERROR: Salary must be a valid number.")
                return False
        if attribute_name == "name":
            self.name = new_value
        else:
            self.role = new_value
        return True

def new_employee(arr, id, name, role, salary):
    employee_data = Employee(id, name, role, salary)
    arr.append(employee_data)

def binary_search(arr, target_id):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid].id == target_id:
            return mid
        elif arr[mid].id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def save_data(employees, id_counter, filename="database.pkl"):
    state = {"employees": employees, "id_counter": id_counter}
    with open(filename, "wb") as f:
        pickle.dump(state, f)

def load_data(filename="database.pkl"):
    try:
        with open(filename, "rb") as f:
            state = pickle.load(f)
            return state["employees"], state["id_counter"]
    except FileNotFoundError:
        return [], 0

employees, id_counter = load_data()
while True:
    try:
        print("""
1. Display all employees
2. Add new employee
3. Search for employee
4. Update employee attribute
5. Remove employee record
6. Exit""")
        menu = int(input("Choose (1-6): "))
        
        if menu == 1:
            if len(employees) == 0:
                print("The employee database is currently empty.")
            else:
                for x in employees:
                    x.display_info()
                    print("")

        elif menu == 2:
            id_counter += 1
            assigned_id = id_counter
            print(f"System assigned ID: {assigned_id}")
            name = input("Enter Employee Name: ").strip()
            role = input("Enter Employee Role: ").strip()
            while True:
                try:
                    salary = float(input("Enter Starting Salary: "))
                    if salary > 0:
                        break
                    print("Salary must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a numerical value for salary.")
            new_employee(employees, assigned_id, name, role, salary)
            save_data(employees, id_counter)
            print("Employee successfully added and saved.")

        elif menu == 3:
            if len(employees) == 0:
                print("Database is empty. Nothing to search.")
            else:
                target = int(input("Enter Employee ID to search: "))
                index = binary_search(employees, target)
                if index != -1:
                    match = employees[index]
                    print(f"RECORD FOUND at array index position {index}:")
                    match.display_info()
                else:
                    print(f"Record with ID {target} could not be located.")
        
        elif menu == 4:
            target = int(input("Enter Employee ID to update: "))
            index = binary_search(employees, target)
            if index != -1:
                emp = employees[index]
                attr = input("Which attribute? (name / role / salary): ").strip().lower()
                while attr != "name" and attr != "role" and attr != "salary":
                    print("Attribute not found.")
                    attr = input("Which attribute? (name / role / salary): ").strip().lower()
                new_val = input(f"Enter new value for {attr}: ").strip()
                if emp.update_attribute(attr, new_val):
                    save_data(employees, id_counter)
                    print(f"Update successfully saved.")
            else:
                print("Employee not found.")
        
        elif menu == 5:
            target = int(input("Enter Employee ID to delete: "))
            index = binary_search(employees, target)
            choice = input("Are you sure? (Y/N): ").upper()
            if index != -1 and choice == "Y":
                employees.pop(index)
                save_data(employees, id_counter)
            else:
                print("Action cancelled or ID not found.")
                
        elif menu == 6:
            save_data(employees, id_counter)
            print("Database successfully saved.")
            break

        else:
            print("Invalid option.")
    
    except ValueError:
        print("Please ensure you enter numeric numbers for selections and IDs.")
    except Exception as e:
        print("ERROR:", e)