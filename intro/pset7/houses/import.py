from cs50 import SQL
import csv
import sys

# Check for proper usage
if len(sys.argv) != 2:
    print("Usage: python import.py [filename.csv]")
    sys.exit(1)
else:
    filename = sys.argv[1]

db = SQL("sqlite:///students.db")

# Open csv file
with open(filename, "r") as data:
    
    # Create DictReader
    reader = csv.DictReader(data)
    
    # Parse csv and prepare for db
    for row in reader:
        
        temp = row['name'].split(" ")
        
        firstName = temp[0]
        middleName = temp[1] if len(temp) == 3 else None
        lastName = temp[2] if len(temp) == 3 else temp[1]
        
        # Insert row to db
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)", firstName, middleName, lastName, row['house'], row['birth'])
        db.execute("DELETE FROM students WHERE id > 40") # tool to clean up odd imports

sys.exit(0)