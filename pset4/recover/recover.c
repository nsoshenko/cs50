#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

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

    //Initialize names for output files
    char filename[8];
    int filename_counter = 0;

    //Allocate memory for read
    unsigned char(*buffer) = calloc(512, 1);
    if (buffer == NULL)
    {
        fprintf(stderr, "Not enough memory for reading.\n");
        fclose(inptr);
        return 1;
    }

    // Initialize a mock file (temporary workaround)
    FILE *outptr = fopen("foo", "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", filename);
        return 1;
    }
    fclose(outptr);

    //Start reading
    while (fread(buffer, 1, 512, inptr) == 512) //Check for the end of the file
    {
        // Look for beginning of a JPEG
        bool jpeg = false;
        if (buffer[0] == 0xff)
        {
            if (buffer[1] == 0xd8)
            {
                if (buffer[2] == 0xff)
                {
                    if ((buffer[3] & 0xf0) == 0xe0)
                    {
                        jpeg = true;
                    }
                }
            }
        }

        if (jpeg == true)
        {
            // Close previous file if JPEG is found
            if (filename_counter != 0)
            {
                fclose(outptr);
            }

            // Change filename
            sprintf(filename, "%03i.jpg", filename_counter);

            // Open a new JPEG file
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 1;
            }
            else
            {
                filename_counter++;
            }
        }

        if (filename_counter != 0)
        {
            // Write 512 bytes until new JPEG is found
            fwrite(buffer, 1, 512, outptr);
        }
    }

    // Free memory and close all files
    free(buffer);
    fclose(inptr);
    fclose(outptr);
}