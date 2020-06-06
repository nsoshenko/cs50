from cs50 import get_int

while True:
    height = get_int("Number between 1 and 8 inclusive: ")
    if height > 0 and height < 9:
        break
        
i = 1
while i <= height:
    print(" " * (height-i), end="")
    print("#" * i, end="  ")
    print("#" * i)
    i += 1