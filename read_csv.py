import csv

with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)
    employee_salary=0
    for employee in reader:
        employee_salary = int(employee["salary"])
        new_salary = employee_salary + ( 0.10 * employee_salary )
        print(employee["name"] ,"old salary: ",employee_salary ,"new salary:", new_salary)
