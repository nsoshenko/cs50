from cs50 import SQL
import sys

# Check for proper usage
if len(sys.argv) != 2:
    print("Usage: python roster.py Gryffindor|Ravenclaw|Hufflepuff|Slytherin")
    sys.exit(1)
else:
    query = sys.argv[1]
    
db = SQL("sqlite:///students.db") # Open DB

# Execute query
roster = db.execute("SELECT * FROM students WHERE house=? ORDER BY last, first", query)

# Print results checking for middle name
for row in roster:
    if not row['middle']:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")

sys.exit(0)