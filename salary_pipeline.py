import csv
with open("employees.csv", "r") as input_files:
    reader = csv.DictReader(input_files)
    


    with open("employees_updated.csv", "w" , newline="") as outful_files:
        fieldnames = ["name", "age", "department", "salary"]

        writer = csv.DictWriter(outful_files, fieldnames=fieldnames)
        writer.writeheader()
        for employee in reader:
                employee["salary"] = int(int(employee["salary"]) * 1.10)
                writer.writerow(employee)