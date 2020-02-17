#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>

int counters(string text);

int main(void)
{
    string text = get_string("Text: ");
    if (text == NULL)
    {
        return 1;
    }
    //printf("%s\n", text);
    int n = counters(text);
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
        else if (isspace(s[i]) && isalpha(s[i + 1]))
        {
            w_count++;
        }
        else if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            s_count++;
        }
    }
    //printf("%i letters\n", l_count);
    //printf("%i words\n", w_count);
    //printf("%i sentences\n", s_count);
    float l = (float) l_count / w_count * 100;
    //printf("%f", l);
    float se = (float) s_count / w_count * 100;
    printf("%f", 0.0588 * l - 0.296 * se - 15.8);
    int index = round(0.0588 * l - 0.296 * se - 15.8);
    return index;
}
