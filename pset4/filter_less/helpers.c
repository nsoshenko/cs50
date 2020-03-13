#include <math.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int MAX = 255; //max number in hexadecimal

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculate new colors
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            //Normalize colors to the cap
            if (sepiaRed > MAX)
                sepiaRed = MAX;
            if (sepiaGreen > MAX)
                sepiaGreen = MAX;
            if (sepiaBlue > MAX)
                sepiaBlue = MAX;

            //Replace colors with new ones
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reflected_row[width];

    for (int i = 0; i < height; i++)
    {
        //Generate reflection in a new row
        for (int j = 0; j < width; j++)
        {
            reflected_row[width - (j + 1)] = image[i][j];
        }

        //Replace existing row with its reflection
        for (int j = 0; j < width; j++)
        {
            image[i][j] = reflected_row[j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurred[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Prepare variables for single pixel blurring
            int avRed = 0;
            int avGreen = 0;
            int avBlue = 0;
            float count = 0.0;
            int lower_height, lower_width, upper_height, upper_width;

            //Set "mini-image" height boudaries
            if (i == 0)
            {
                lower_height = i;
                upper_height = i + 2;
            }
            else if (i == height - 1)
            {
                lower_height = i - 1;
                upper_height = i + 1;
            }
            else
            {
                lower_height = i - 1;
                upper_height = i + 2;
            }

            //Set "mini-image" width boundaries
            if (j == 0)
            {
                lower_width = j;
                upper_width = j + 2;
            }
            else if (j == width - 1)
            {
                lower_width = j - 1;
                upper_width = j + 1;
            }
            else
            {
                lower_width = j - 1;
                upper_width = j + 2;
            }

            //Loop through the "mini-image" of adjacent pixels
            for (int k = lower_height; k < upper_height; k++)
            {
                for (int l = lower_width; l < upper_width; l++)
                {
                    avRed = avRed + image[k][l].rgbtRed;
                    avGreen = avGreen + image[k][l].rgbtGreen;
                    avBlue = avBlue + image[k][l].rgbtBlue;
                    count = count + 1.0;
                }
            }

            //Create blurred pixel on a new image instance
            blurred[i][j].rgbtRed = round(avRed / count);
            blurred[i][j].rgbtGreen = round(avGreen / count);
            blurred[i][j].rgbtBlue = round(avBlue / count);
        }
    }

    //Replace initial image with the blurred one
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurred[i][j];
        }
    }
    return;
}
