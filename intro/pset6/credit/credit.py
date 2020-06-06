from cs50 import get_string

card = get_string("Number: ") # get card number
reversed_card = card[len(card)::-1] # reverse card number for an algorithm

checksum = 0

# Luhn's algorithm
for c in range(len(card)):
    if c % 2 == 0:
        checksum += int(reversed_card[c], 10)
    else:
        temp = int(reversed_card[c], 10) * 2
        checksum += temp // 10 + temp % 10
        
# Validation
if checksum % 10 == 0:
    if len(card) == 15 and int(card[0], 10) == 3 and int(card[1], 10) in [4, 7]:
        print("AMEX")
    elif len(card) == 16 and int(card[0], 10) == 5 and int(card[1], 10) in [1, 2, 3, 4, 5]:
        print("MASTERCARD")
    elif (len(card) == 13 or len(card) == 16) and int(card[0], 10) == 4:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")