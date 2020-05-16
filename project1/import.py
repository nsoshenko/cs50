import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")
reader = csv.reader(file)
print("Starting import")
for isbn, title, author, year in reader:
  db.execute("INSERT INTO books (title, author, year, isbn) VALUES (:title, :author, :year, :isbn)",
                   {"title": title, "author": author, "year": year, "isbn": isbn})
  print(f"{title} is prepared")
db.commit()
print("Import is finished")
