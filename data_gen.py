import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Define headers
headers = [
    'Name', 'Employee Number', 'Position', 'Department', 'Division',
    'Station', 'Clock-in Time', 'Clock-out Time', 'Absences', 'Leave Days',
    'Approved Overtime Hours', 'Pending Overtime Hours', 'Work Categories',
    'Approval Status'
]

# List of possible values for certain fields
positions = ['Manager', 'Analyst', 'Engineer', 'Coordinator', 'Assistant']
departments = ['HR', 'Finance', 'IT', 'Operations', 'Sales', 'Marketing']
divisions = ['North', 'South', 'East', 'West']
stations = ['Station A', 'Station B', 'Station C', 'Station D']
work_categories = ['Regular', 'Overtime', 'Special Project']
approval_statuses = ['Approved', 'Pending', 'Rejected']

# Generate dummy data
data = []
for _ in range(500):
    row = {
        'Name': fake.name(),
        'Employee Number': fake.unique.random_int(min=1000, max=9999),
        'Position': random.choice(positions),
        'Department': random.choice(departments),
        'Division': random.choice(divisions),
        'Station': random.choice(stations),
        'Clock-in Time': fake.time(),
        'Clock-out Time': fake.time(),
        'Absences': random.randint(0, 5),
        'Leave Days': random.randint(0, 15),
        'Approved Overtime Hours': round(random.uniform(0, 10), 2),
        'Pending Overtime Hours': round(random.uniform(0, 5), 2),
        'Work Categories': random.choice(work_categories),
        'Approval Status': random.choice(approval_statuses)
    }
    data.append(row)

# Create a DataFrame
df = pd.DataFrame(data, columns=headers)

# Write to Excel file
df.to_excel('oracle_apex_attendance_overtime_report.xlsx', index=False)

print("Excel sheet 'oracle_apex_attendance_overtime_report.xlsx' generated successfully.")
