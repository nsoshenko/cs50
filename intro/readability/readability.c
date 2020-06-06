#include <stdio.h>
#include <cs50.h>
#include <ctype.h> //may exclude in future using ASCII codes
#include <math.h>

int counters(string s);

int main(void)
{
    string text = get_string("Text: ");
    
    //check for cooperation
    if (text == NULL)
    {
        return 1;
    }
    
    //execute the readability algorithm
    int n = counters(text);
    
    //print the results of the algorithm
    if (n < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (n > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", n);
    }

    return 0;
}

//count letters, words and sentences
int counters(string s)
{
    int l_count = 0;
    int w_count = 1;
    int s_count = 0;
    for (int i = 0; s[i] != '\0'; i++)
    {
        if (isalpha(s[i]))
        {
            l_count++;
        }
        
        //count all words after spaces and " (the first word is already included)
        else if ((isspace(s[i]) || s[i] == '"') && isalpha(s[i + 1]))
        {
            w_count++;
        }
        
        //each sentence has a finish mark
        else if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            s_count++;
        }
    }
   
    //debug block ;)
    //printf("%i letters\n", l_count);
    //printf("%i words\n", w_count);
    //printf("%i sentences\n", s_count);
    
    //algorithm math
    float l = (float) l_count / w_count * 100;
    float se = (float) s_count / w_count * 100;
    //printf("%f\n", 0.0588 * l - 0.296 * se - 15.8);
    int index = round(0.0588 * l - 0.296 * se - 15.8);
    return index;
}
