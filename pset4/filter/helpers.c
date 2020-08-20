#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int B;
    int G;
    int R;
    int sum;
   
    float avg;
    int avg2;

    for( int i = 0 ; i < height; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            B = image[i][j].rgbtBlue;
            G = image[i][j].rgbtGreen;
            R = image[i][j].rgbtRed;
            
            sum= B + G + R;

            avg2 = round((sum/3.0));    //average

            image[i][j].rgbtBlue = avg2;   //insert avg to array
            image[i][j].rgbtGreen = avg2;
            image[i][j].rgbtRed = avg2;
        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int B;
    int G;
    int R;
    RGBTRIPLE copy[height][width];

    for( int i = 0; i < height  ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            B = image[i][j].rgbtBlue;
            G = image[i][j].rgbtGreen;
            R = image[i][j].rgbtRed;

            // take values and copy to other array
            copy[i][width-1-j].rgbtBlue = B;
            copy[i][width-1-j].rgbtGreen = G;
            copy[i][width-1-j].rgbtRed = R;
        }
    }

    //copy to new image

    for( int i = 0; i < height  ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue ;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen ;
            image[i][j].rgbtRed =  copy[i][j].rgbtRed ;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // average r,g,b for 9 pixels


    float iguessineedtobeafloat;
    int Bavg2;
    int Gavg2;
    int Ravg2;

    RGBTRIPLE copy[height][width];


    for( int i = 0; i < height ; i++)
    {
        for (int j = 0; j < width ; j++)
        {

           // 4 up to 9 neighbouring cell addition
           int cellscount = 0; int sumBlue = 0; int sumGreen = 0; int sumRed = 0;

           for (int ii = -1; ii < 2; ii++)
           {
               for (int jj = -1;  jj < 2; jj++)
               {

                   if ( (i + ii) > -1 && (i +ii)< height   &&
                   (j + jj) > -1 && (j + jj) < width  )
                   {
                        sumBlue = sumBlue + image[i + ii][j + jj].rgbtBlue ;
                        sumGreen = sumGreen + image[i + ii][j + jj].rgbtGreen;
                        sumRed = sumRed + image[i + ii][j + jj].rgbtRed;
                        cellscount++;
                   }
               }
           }
        
            iguessineedtobeafloat = cellscount; // round is the new curvy i guess
            Bavg2 = round(sumBlue / iguessineedtobeafloat);
            Gavg2 = round(sumGreen / iguessineedtobeafloat);
            Ravg2 = round(sumRed / iguessineedtobeafloat);

            copy[i][j].rgbtBlue = Bavg2 ;  //copy to coopy array
            copy[i][j].rgbtGreen = Gavg2 ;
            copy[i][j].rgbtRed = Ravg2 ;
            
        }
    }

    //coppy back to array

    for( int i = 0; i < height  ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue ;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen ;
            image[i][j].rgbtRed =  copy[i][j].rgbtRed ;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    
    int Bavg;
    int Gavg;
    int Ravg;
    
    int Bavgy;
    int Gavgy;
    int Ravgy;
    
    
    
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    RGBTRIPLE copy[height][width];


    for( int i = 0; i < height ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
           // 4 up to 9 neighbouring cell addition
           int sumBluex = 0; int sumGreenx = 0; int sumRedx = 0;
           int sumBluey = 0; int sumGreeny = 0; int sumRedy = 0;
           
           for (int ii = -1; ii < 2; ii++)
           {
               for (int jj = -1;  jj < 2; jj++)
               {
                   if ( (i + ii) > -1 && (i +ii)< height   &&
                   (j + jj) > -1 && (j + jj) < width  )
                   {
                        sumBluex = sumBluex + gx[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtBlue ;
                        sumGreenx = sumGreenx + gx[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtGreen;
                        sumRedx = sumRedx + gx[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtRed;
                        
                        sumBluey = sumBluey + gy[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtBlue ;
                        sumGreeny = sumGreeny + gy[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtGreen;
                        sumRedy = sumRedy + gy[ii + 1][jj + 1] * image[i + ii][j + jj].rgbtRed;
                        
                   }
               }
           }
           
           // squaring
            sumBluex = sumBluex * sumBluex;  
            sumGreenx = sumGreenx * sumGreenx;
            sumRedx = sumRedx * sumRedx;
            sumBluey = sumBluey * sumBluey;  
            sumGreeny = sumGreeny * sumGreeny;
            sumRedy = sumRedy * sumRedy;
        
            
            Bavg = round(sqrt(sumBluex + sumBluey ));
            Gavg = round(sqrt(sumGreenx + sumGreeny ));
            Ravg = round(sqrt(sumRedx + sumRedy ));
            
            if (Bavg > 255)
            {
                Bavg = 255;
            }
            if (Gavg > 255)
            {
                Gavg = 255;
            }
            if (Ravg > 255)
            {
                Ravg = 255;
            }
            

            copy[i][j].rgbtBlue = Bavg ;  //copy to coopy array
            copy[i][j].rgbtGreen = Gavg ;
            copy[i][j].rgbtRed = Ravg ;
            
        }
    }
    
    //copy from copy to image
    
    for( int i = 0; i < height  ; i++)
    {
        for (int j = 0; j < width ; j++)
        {
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue ;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen ;
            image[i][j].rgbtRed =  copy[i][j].rgbtRed ;
        }
    }

    
    return;
}
