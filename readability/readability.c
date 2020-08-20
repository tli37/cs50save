
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>


int main(void)

{
    string A = get_string("Text: ");  //get text promt
    //printf(" %s\n", A); // print text promt old code, should i delete this?


    long int length= strlen(A);

    //printf("Length of string A = %ld\n", length); //string length old code, should i delete this?

    int count1=0;
    int count2=1;
    int count3=0;
    int i;

    for (i=0; i < length; i++)
    {
        int charcheck1 = A[i];
        int wordcheck1 = A[i - 1];


        if ((charcheck1 > 64 && charcheck1< 91)|| (charcheck1> 96 && charcheck1 < 123))  //character check
        {
            count1= count1 + 1;  // charcter count

            if (isblank(wordcheck1) || wordcheck1== 34)
            {
                count2=count2 +1; // word count
            }

        }
        if (charcheck1 == 63 || charcheck1 == 33 || charcheck1 == 46)
        {
            count3=count3 + 1;
        }


    }


   //printf("Total letters in count %i\n",count1); old code, should i delete this?
   //printf("Total Words in count %i\n", count2);
  //printf("Total Sentence(s) in count %i\n", count3);


    float index= 0;
    int index2= 0;
    float C1= count1; // float conversion
    float C2= count2; 
    float C3= count3;
    float L1= 0; // denominator
    float L2= 0;
    float S1= 0;
    float S2= 0;

    L1 = C2 / 100 ; // Words per 100 words
    L2 = C1 /L1 ; // Letters per 100 words
    S1 = C2 / 100 ;  // words per 100 words
    S2 = C3 /S1 ; //setences per 100 words

   // printf("grade1 %f\n",L1); old code, should i delete this?
   // printf("grade1 %f\n",L2);
   // printf("grade2 %f\n",S1);
   // printf("grade2 %f\n",S2);

    index = 0.0588 * L2 - 0.296 * S2 - 15.8 ;
    index2 = round(index);

    if (index2 < 1)
    {
        printf("Before Grade 1\n");

    }
    else if (index2 > 16)
        {
            printf("Grade 16+\n");

        }
        else
        {
            printf("Grade %i\n", index2);

        }


}


