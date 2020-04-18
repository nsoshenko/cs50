import sys

def main():

    # Check for proper usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py [database] [sequence]")
        sys.exit(1)
    else:
        database = sys.argv[1]
        sequence = sys.argv[2]

    # Open database
    file = open(database, "r")
    if not file:
        print(f"Could not open {database}.")
        sys.exit(1)

    # Load database in dictionary
    db = {}
    for line in file:
        temp = line.rstrip("\n").rsplit(",")
        db[temp[0]] = temp[1:]
    # print(f"{db['name'][0]}")
    file.close()

    # Open sequence sample and read it to memory
    file = open(sequence, "r")
    if not file:
        print(f"Could not open {sequence}.")
        sys.exit(1)
    sample = file.read()
    file.close()

    # Process the sample
    results = []
    for s in db['name']:
        max_count = 0
        for i in range(len(sample) - len(s) + 1):
            count = 0
            start = i
            end = i + len(s)
            while sample[start:end] == s and end < len(sample):
                count += 1
                start += len(s)
                end += len(s)
            max_count = max(count, max_count)
        results.append(str(max_count))

    # Check for matches in database
    for person in db:
        # print(f"{person}, {db[person]}")
        # print(f"{results}")
        if db[person] == results:
            print(f"{person}")
            sys.exit(0)

    # If nothing found in db
    print("No match")
    sys.exit(0)


main()