#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            //printf("Rank %i: %i\n", rank + 1, i);  //Debug block
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i; j < candidate_count; j++)
        {
            int delta = preferences[i][j] - preferences[j][i];
            if (delta == 0)
                continue;
            else if (delta > 0)
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }

    for (int i = 0; i < pair_count; i++)
    {
        printf("Unsorted pair %i: %s[%i]-%s[%i]\n", i + 1, candidates[pairs[i].winner], pairs[i].winner, candidates[pairs[i].loser], pairs[i].loser);
    }

    return;
}

//Function needed for further sort_pairs
void swap(int *x, int *y)
{
    printf("Before swap: %i-%i\n", *x, *y);

    int temp = *x;
    *x = *y;
    *y = temp;

    printf("Swap result: %i-%i\n", *x, *y);
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int strength[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        strength[i] = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
        printf("Strength of pair %s-%s: %i\n", candidates[pairs[i].winner], candidates[pairs[i].loser], strength[i]);
    }

    for (int i = pair_count - 1; i > 0; i--)
    {
        for (int j = 0; j < i; j++)
        {
            if (strength[j] < strength[j + 1])
            {
                printf("Need swap\n");
                swap(&strength[j], &strength[j + 1]);
                swap(&pairs[j].winner, &pairs[j + 1].winner);
                swap(&pairs[j].loser, &pairs[j + 1].loser);
            }
        }
    }

    for (int i = 0; i < pair_count; i++)
    {
        printf("Sorted pair %i: %s-%s\n", i + 1, candidates[pairs[i].winner], candidates[pairs[i].loser]);
    }
}

//Function to detect cycles in adjacency matrix for lock_pairs
bool is_cycle(int vertice, int root)
{
    if (locked[vertice][root] == true)
            return true;
            
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[vertice][i] == true)
            {
                if (is_cycle(i, root))
                    return true;
            }
    }
    
    return false;
}


// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    //bool stack[candidate_count];

    for (int i = 0; i < candidate_count; i++)
    {
        //if (stack[pairs[i].winner] && stack[pairs[i].loser])
        if (is_cycle(pairs[i].loser, pairs[i].winner))
        {
            printf("Potential cycle in pair %i\n", i + 1);
            continue;
        }
        else
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
            //stack[pairs[i].winner] = true;
            //stack[pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    bool inner_break;

    for (int j = 0; j < candidate_count; j++)
    {
        inner_break = false;

        for (int i = 0; i < candidate_count; i++)
        {
            if (locked[i][j] == true)
            {
                inner_break = true;
                break;
            }
        }
        if (inner_break == true)
            continue;

        printf("%s\n", candidates[j]);
    }
    return;
}

