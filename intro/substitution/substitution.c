#include <stdio.h>
#include <cs50.h> //for string type
#include <string.h> //for strlen
#include <ctype.h> //for toupper, tolower
#include <stdlib.h> //for malloc, free

int main(int argc, string argv[])
{
    //check for only one argument (key)
    if (argc != 2 || strlen(argv[1]) != 26)
    {
        printf("Usage: ./substitution key (26 letters)\n");
        return 1;
    }
    
    //shorten the name of the variable (not the best way, probably)
    string k = argv[1];
    
    //needed for validation 2
    string checker = malloc(27);
    
    //Validation 1: check that all key symbols are letters and prepare the second validation
    for (int i = 0; k[i] != '\0'; i++)
    {
        if (!isalpha(k[i])) 
        {
            printf("Key must contain only alphabetic characters\n");
            return 1;
        }
        
        //Validation 2: check symbol for the uniqueness
        for (int j = 0; j < strlen(checker); j++)
        {
            if (k[i] == checker[j])
            {
                printf("Key must contain all alphabetical characters exactly once\n");
                return 1;
            }
        }
        checker[i] = k[i];
    }
    free(checker); //free memory
    
    
    //main logic starts here
    string p = get_string("plaintext: ");
    printf("ciphertext: ");
    
    for (int i = 0; p[i] != '\0'; i++)
    {
        //check if iterable char is not a letter and skip
        if (!isalpha(p[i]))
        {
            printf("%c", p[i]);
            continue;
        }
        
        //cipher for uppercase
        if (isupper(p[i]))
        {
            int position = (int) p[i] - 65; //ASCII table is used
            printf("%c", toupper(k[position]));
        }
        
        //cipher for lowercase
        if (islower(p[i]))
        {
            int position = (int) p[i] - 97; //ASCII table is used
            printf("%c", tolower(k[position]));
        }
    }
    printf("\n");
    return 0;
}



