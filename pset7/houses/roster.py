from cs50 import SQL
import sys

if len(sys.argv) != 2:
    print("Usage: python roster.py Gryffindor|Ravenclaw|Hufflepuff|Slytherin")
    sys.exit(1)
else:
    query = sys.argv[1]
    
db = SQL("sqlite:///students.db")

roster = db.execute("SELECT * FROM students WHERE house=? ORDER BY last, first", query)

for row in roster:
    if not row['middle']:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")

sys.exit(0)