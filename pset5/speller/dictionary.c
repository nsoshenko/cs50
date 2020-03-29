// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h> // for strcpy
#include <ctype.h> // for isalpha
extern int strcasecmp (const char *s1,  const char *s2); //case insensitive comparison

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26*26*26; //assumtion of optimal buckets number

// Hash table
node *table[N];

// Word counter
int counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Calculate bucket of the word
    int index = hash(word);

    // Compare word with all in the bucket
    node *cursor = table[index]->next;
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Lower words to make hash function case insensitive
    char *lower_word = malloc(strlen(word) + 1);
    if (lower_word == NULL)
    {
        return false;
    }

    // Hash function from https://computinglife.wordpress.com/2008/11/20/why-do-hash-functions-use-prime-numbers/
    unsigned long index = 7;
    
    for (int i = 0; (i < strlen(word) && i < 20); i++)
    {
        lower_word[i] = tolower(word[i]);
        index = index * 31 + lower_word[i];
    }
    index = index % N; // reduce hash to be inside of number of buckets
    
    free(lower_word);
    return index;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
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
        table[i] = calloc(1, sizeof(node)); // calloc instead of malloc to inititalize
    }

    // Read all lines until the end of file (assume line == word)
    while (fscanf(inptr, "%s", word) != EOF)
    {
        // Allocate new node
        node *n = calloc(1, sizeof(node)); // calloc to initialize
        if (n == NULL)
        {
            return false;
        }

        // Copy word from buffer to a node
        strcpy(n->word, word);

        // Calculate a bucket to add node
        int index = hash(n->word);

        // Add node to the beginning of the list
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
    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return counter; // calculated in load function
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp; // temporary pointer to free

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i]; // cursor points at the beginning of the bucket
        while (cursor != NULL) // iterate through the bucket
        {
            tmp = cursor; // tmp points at the same element as cursor
            cursor = cursor->next; // cursor points at next element
            free(tmp); // free previous element
        }
    }

    return true;
}