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
    int MAX = 255;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            
            if (sepiaRed > MAX)
                sepiaRed = MAX;
            if (sepiaGreen > MAX)
                sepiaGreen = MAX;
            if (sepiaBlue > MAX)
                sepiaBlue = MAX;
            
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
            int rgbtRed = 0;
            int rgbtGreen = 0;
            int rgbtBlue = 0;
            float count = 0.0;
            int k, l, n, m;
            
            if (i == 0)
            {
                k = i;
                n = i + 2;
            }
            else if (i == height - 1)
            {
                k = i - 1;
                n = i + 1; 
            }
            else
            {
                k = i - 1;
                n = i + 2;
            }
            
            if (j == 0)
            {
                l = j;
                m = j + 2;
            }
            else if (j == width - 1)
            {
                l = j - 1;
                m = j + 1; 
            }
            else
            {
                l = j - 1;
                m = j + 2;
            }
                
            for (int x = k; x < n; x++)
            {
                for (int y = l; y < m; y++)
                {
                    rgbtRed = rgbtRed + image[x][y].rgbtRed;
                    rgbtGreen = rgbtGreen + image[x][y].rgbtGreen;
                    rgbtBlue = rgbtBlue + image[x][y].rgbtBlue;
                    count = count + 1.0;
                }
            }
        
            blurred[i][j].rgbtRed = round(rgbtRed / count);
            blurred[i][j].rgbtGreen = round(rgbtGreen / count);
            blurred[i][j].rgbtBlue = round(rgbtBlue / count);
        }
    }
    return;
}
