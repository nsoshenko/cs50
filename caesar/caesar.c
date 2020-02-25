#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //check for only one argument (key)
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //check that all key symbols are decimal numbers
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (argv[1][i] < 48 || argv[1][i] > 57) //0-9 according to ASCII chart
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    //normalizing the key (only 26 letters in the alphabet)
    int key = atoi(argv[1]);
    if (key > 26)
    {
        key = key % 26;
    }
    //printf("Key: %i\n", key);

    //main logic
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

        //applying the cipher
        int c = (int) p[i] + key;

        //wrap around the alphabet keeping the case
        if ((p[i] <= 90 && c > 90) || (p[i] >= 97 && c > 122))
        {
            c = c - 26;
        }
        printf("%c", (char) c);
    }
    printf("\n");
    return 0;
}
