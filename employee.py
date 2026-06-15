import pickle

class Employee:
    def __init__(self, id, name, role, salary, status="active"):
        self.id = id
        self.name = name
        self.role = role
        self.__salary = salary
        self.status = status

    def display_info(self):
        print(f"""ID: {self.id}
Name: {self.name}
Role: {self.role}
Salary: {self.__salary}
Status: {self.status}""")

    def get_salary(self):
        return self.__salary

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
        elif attribute_name == "name":
            self.name = new_value
        elif attribute_name == "role":
            self.role = new_value
        else:
            print("Attribute not found.")
            return False
        return True

def new_employee(arr, id, name, role, salary):
    employee_data = Employee(id, name, role, salary)
    arr.append(employee_data)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j].id > arr[j + 1].id:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def display_former(employees):
    inactive = [e for e in employees if e.status == "inactive"]
    if not inactive:
        print("No former employees on record.")
        return False
    print("\nFormer employees:")
    for e in inactive:
        e.display_info()
        print("")
    return True

def reemploy(employees):
    if not display_former(employees):
        return
    target = int(input("Enter ID of employee to reemploy: "))
    index = binary_search(employees, target)
    if index != -1 and employees[index].status == "inactive":
        emp = employees[index]
        print(f"\nReemploying: {emp.name} | Previous role: {emp.role} | Previous salary: {emp.get_salary()}")
        update_role = input("Update role? (Y/N): ").upper()
        if update_role == "Y":
            new_role = input("Enter new role: ").strip()
            emp.update_attribute("role", new_role)
        update_salary = input("Update salary? (Y/N): ").upper()
        if update_salary == "Y":
            new_salary = input("Enter new salary: ").strip()
            emp.update_attribute("salary", new_salary)
        emp.status = "active"
        print(f"{emp.name} has been successfully reemployed.")
    else:
        print("Former employee not found.")

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
6. Reemploy former employee
7. Display former employees
8. Exit""")
        menu = int(input("Choose (1-8): "))

        if menu == 1:
            active = [e for e in employees if e.status == "active"]
            if not active:
                print("The employee database is currently empty.")
            else:
                for x in active:
                    x.display_info()
                    print("")

        elif menu == 2:
            id_counter += 1
            assigned_id = id_counter
            print(f"System assigned ID: {assigned_id}")
            name = input("Enter employee name: ").strip()
            role = input("Enter employee role: ").strip()
            while True:
                try:
                    salary = float(input("Enter starting salary: "))
                    if salary > 0:
                        break
                    print("Salary must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a numerical value for salary.")
            new_employee(employees, assigned_id, name, role, salary)
            bubble_sort(employees)
            save_data(employees, id_counter)
            print("Employee successfully added and saved.")

        elif menu == 3:
            active = [e for e in employees if e.status == "active"]
            if not active:
                print("The employee database is currently empty.")
            else:
                target = int(input("Enter Employee ID to search: "))
                index = binary_search(employees, target)
                if index != -1 and employees[index].status == "active":
                    print(f"Found at array index {index}:")
                    employees[index].display_info()
                else:
                    print(f"Record with ID {target} could not be located.")

        elif menu == 4:
            target = int(input("Enter Employee ID to update: "))
            index = binary_search(employees, target)
            if index != -1 and employees[index].status == "active":
                emp = employees[index]
                attr = input("Which attribute? (name / role / salary): ").strip().lower()
                while attr not in ("name", "role", "salary"):
                    print("Attribute not found.")
                    attr = input("Which attribute? (name / role / salary): ").strip().lower()
                new_val = input(f"Enter new value for {attr}: ").strip()
                if emp.update_attribute(attr, new_val):
                    save_data(employees, id_counter)
                    print("Update successfully saved.")
            else:
                print("Employee not found.")

        elif menu == 5:
            target = int(input("Enter employee ID to remove: "))
            index = binary_search(employees, target)
            if index != -1 and employees[index].status == "active":
                choice = input("Are you sure? (Y/N): ").upper()
                if choice == "Y":
                    employees[index].status = "inactive"
                    save_data(employees, id_counter)
                    print("Employee record removed.")
                else:
                    print("Action cancelled.")
            else:
                print("Employee not found.")

        elif menu == 6:
            reemploy(employees)
            save_data(employees, id_counter)

        elif menu == 7:
            display_former(employees)

        elif menu == 8:
            save_data(employees, id_counter)
            print("Database successfully saved.")
            break

        else:
            print("Invalid option.")

    except ValueError:
        print("Please ensure you enter numbers for selections and IDs.")
    except Exception as e:
        print("ERROR:", e)
