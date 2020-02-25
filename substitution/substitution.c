#include <stdio.h>
#include <cs50.h>
#include <string.h>

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
    
    //check that all key symbols are letters
    for (int i = 0; k[i] != '\0'; i++)
    {
        if (k[i] < 65 || (k[i] > 90 && k[i] < 97) || k[i] > 122) 
        {
            printf("Usage: ./substitution key (26 letters)\n");
            return 1;
        }
        //else if (TBD: convert key to uppercase)
    }
    
    //main logic starts here
    string p = get_string("plaintext: ");
    printf("ciphertext: ");
    
    for (int i = 0; p[i] != '\0'; i++)
    {
        //check if iterable char is not a letter and skip
        if (p[i] < 65 || (p[i] > 90 && p[i] < 97) || p[i] > 122)
        {
            printf("%c", p[i]);
            continue;
        }
        
        //cipher for uppercase
        if (p[i] >= 65 && p[i] <= 90)
        {
            int position = (int) p[i] - 65;
            printf("%c", k[position]);
        }
        
        //cipher for lowercase
        if (p[i] >= 97 && p[i] <= 122)
        {
            int position = (int) p[i] - 97;
            printf("%c", k[position] );
        }
    }
    printf("\n");
    return 0;
}