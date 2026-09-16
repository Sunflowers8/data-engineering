import csv

# Path to the raw employee dataset
input_file = "01-week-foundations/data/raw/employees.csv"

with open(input_file, "r") as file:
    reader = csv.DictReader(file)

    for employee in reader:
        employee_salary = int(employee["salary"])

        # Calculate a 10% salary increase
        new_salary = employee_salary + (0.10 * employee_salary)

        print(
            employee["name"],
            "old salary:",
            employee_salary,
            "new salary:",
            new_salary
        )
