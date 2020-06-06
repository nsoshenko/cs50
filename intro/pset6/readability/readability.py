from cs50 import get_string
from sys import exit

def main():
    text = get_string("Text: ")
    if not text:
        print("No text")
        exit(1)

    index = coleman_liau(text) # algorithm execution

    # Classification of texts
    if index < 1: print("Before Grade 1")
    elif index > 16: print("Grade 16+")
    else: print(f"Grade {index}")
    exit(0)

def coleman_liau(text):
    letters, words, sentences = 0, 1, 0
    for char in text:
        if char.isalpha(): letters += 1
        elif char.isspace(): words += 1
        elif char in [".", "!", "?"]: sentences += 1
    # print(f"Letters: {letters}, Words: {words}, Sentences: {sentences}")
    
    l = (letters / words) * 100
    s = (sentences / words) * 100
    index = round(0.0588 * l - 0.296 * s - 15.8)
    return index
    
main()