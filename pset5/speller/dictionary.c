// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
extern int strcasecmp (const char *s1,  const char *s2);

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Word counter
int counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //printf("Check does smth\n");
    int index = hash(word);
    
    for (node *cursor = table[index]->next; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //printf("Hash does smth\n");
    //printf("First letter in ASCII is %i.\n", index);
    int index = 0;

    if (isalpha(word[0]))
    {
        index = (int) word[0];
        if (index >= 65 && index <= 90)
        {
            index = index - 65;
        }
        else if (index >= 97 && index <= 122)
        {
            index = index - 97;
        }
    }

    return index;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //printf("Load does smth\n");

    // Open file
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        return false;
    }

    // Allocate buffer for word reading
    char *word = malloc(LENGTH+1);
    if (word == NULL)
    {
        return false;
    }

    // Allocate memory for hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = malloc(sizeof(node));
    }

    // Read all lines until the end of file (assume line == word)
    while (fscanf(inptr, "%s", word) != EOF)
    {
        // Allocate new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // Copy word from buffer to a node
        strcpy(n->word, word);
        //printf("Word %s is copied.\n", n->word);

        // Find a bucket to add node
        int index = hash(n->word);
        //printf ("Returned index is %i.\n", index);

        // Add node to a list
        if (table[index]->next == NULL)
        {
            table[index]->next = n;
        }
        else
        {
            n->next = table[index]->next;
            table[index]->next = n;
        }
        counter++;
    }
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    //printf("Size return is %i.\n", counter);
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp = malloc(sizeof(node));
    if (tmp == NULL)
    {
        return false;
    }
    for (int i = 0; i < N; i++)
    {
        for (node *cursor = table[i]; cursor != NULL; cursor = cursor->next)
        {
            if (!*cursor->word)
            {
                tmp = cursor;
            }
            else
            {
                free(tmp);
                tmp = cursor;
            }
            //printf("Unload word is %s.\n", cursor->word);
        }
    }
    free(tmp);
    return true;
}
