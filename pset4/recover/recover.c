#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check for proper usage
    if (argc != 2)
        {
            fprintf(stderr, "Usage: ./recover [raw file name]\n");
            return 1;
        }

    // Remember filename
    char *infile = argv[1];

    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // Look for beginning of a JPEG

    // Open a new JPEG file
    FILE *outptr = fopen("foo", w);
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", "foo");
        return 1;
    }

    // Write 512 bytes until new JPEG is found

    // Stop at end of file

}
