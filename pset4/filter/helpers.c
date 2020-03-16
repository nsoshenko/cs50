#include <math.h>
#include <stdio.h>
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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int MAX = 255; //threshold number in hexadecimal

    //Prepare structure for 3 colors, but which can be bigger than 255 before normalization
    typedef struct
    {
        int red;
        int green;
        int blue;
    }
    PIXEL;

    RGBTRIPLE edges[height][width]; //modified image
    int gx_kernel[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}}; //Sobel kernel for x axis
    int gy_kernel[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}}; //Sobel kernel for y axis

    for (int i = 0; i < height; i++) //take row
    {
        for (int j = 0; j < width; j++) //take pixel
        {
            //Prepare variables for single pixel calculation
            PIXEL gx = {0, 0, 0};
            PIXEL gy = {0, 0, 0};
            PIXEL mod; //for modified result before normalization
            PIXEL source[3][3]; //draw small 3x3 image for kernel multiplication

            //Fill small 3x3 image with default black pixels
            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    source[k][l].red = 0;
                    source[k][l].green = 0;
                    source[k][l].blue = 0;
                }
            }

            //Prepare some variables for boundaries
            int lower_height, lower_width, upper_height, upper_width, source_k, source_l;

            //Set "mini-image" height boudaries
            if (i == 0)
            {
                lower_height = i;
                upper_height = i + 2;
                source_k = 1;
            }
            else if (i == height - 1)
            {
                lower_height = i - 1;
                upper_height = i + 1;
                source_k = 0;
            }
            else
            {
                lower_height = i - 1;
                upper_height = i + 2;
                source_k = 0;
            }

            for (int k = lower_height; k < upper_height; k++) //take "mini-image" row
            {
                //Set "mini-image" width boundaries
                if (j == 0)
                {
                    lower_width = j;
                    upper_width = j + 2;
                    source_l = 1;
                }
                else if (j == width - 1)
                {
                    lower_width = j - 1;
                    upper_width = j + 1;
                    source_l = 0;
                }
                else
                {
                    lower_width = j - 1;
                    upper_width = j + 2;
                    source_l = 0;
                }

                for (int l = lower_width; l < upper_width; l++) //take "mini-image" pixel
                {
                    source[source_k][source_l].red = image[k][l].rgbtRed;
                    source[source_k][source_l].green = image[k][l].rgbtGreen;
                    source[source_k][source_l].blue = image[k][l].rgbtBlue;
                    source_l++;
                }
                source_k++;
            }

            //Gx and Gy calculations aka convolution
            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    gx.red = gx.red + (source[k][l].red * gx_kernel[k][l]);
                    gy.red = gy.red + (source[k][l].red * gy_kernel[k][l]);

                    gx.green = gx.green + (source[k][l].green * gx_kernel[k][l]);
                    gy.green = gy.green + (source[k][l].green * gy_kernel[k][l]);

                    gx.blue = gx.blue + (source[k][l].blue * gx_kernel[k][l]);
                    gy.blue = gy.blue + (source[k][l].blue * gy_kernel[k][l]);
                }
            }

            //Calculate Sobel operator from Gx and Gy
            mod.red = round(sqrt(pow(gx.red, 2) + pow(gy.red, 2)));
            mod.green = round(sqrt(pow(gx.green, 2) + pow(gy.green, 2)));
            mod.blue = round(sqrt(pow(gx.blue, 2) + pow(gy.blue, 2)));

            //Normalize colors to the cap
            if (mod.red > MAX)
                mod.red = MAX;
            if (mod.green > MAX)
                mod.green = MAX;
            if (mod.blue > MAX)
                mod.blue = MAX;

            //Modify new image with modified pixel
            edges[i][j].rgbtRed = mod.red;
            edges[i][j].rgbtGreen = mod.green;
            edges[i][j].rgbtBlue = mod.blue;
        }
    }

    //Replace initial image with the modified one
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = edges[i][j];
        }
    }

    return;
}