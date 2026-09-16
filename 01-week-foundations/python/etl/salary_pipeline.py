import csv

# File paths
input_file = "01-week-foundations/data/raw/employees.csv"
output_file = "01-week-foundations/data/processed/employees_updated.csv"

# Extract: Read employee data
with open(input_file, "r") as input_file_data:
    reader = csv.DictReader(input_file_data)

    # Load: Create a new CSV file
    with open(output_file, "w", newline="") as output_file_data:
        fieldnames = ["name", "age", "department", "salary"]

        writer = csv.DictWriter(
            output_file_data,
            fieldnames=fieldnames
        )

        writer.writeheader()

        # Transform: Increase each employee's salary by 10%
        for employee in reader:
            old_salary = int(employee["salary"])
            new_salary = int(old_salary * 1.10)

            employee["salary"] = new_salary

            writer.writerow(employee)

print("Salary ETL pipeline completed.")
print("Updated data saved to:", output_file)