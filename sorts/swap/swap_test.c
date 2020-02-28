#include <stdio.h>
#include <stdlib.h>
#include "swap.h"

int main(int argc, const char* argv[])
{
    if (argc != 3):
    {
        printf("Put 2 numbers to swap as command line arguments");
        return 1;
    }

    int x = atoi(argv[1]);
    int y = atoi(argv[2]);

    swap(&x, &y);

    printf("%i %i\n", x, y);
    return 0;
}
