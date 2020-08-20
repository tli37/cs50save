
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>



int main(int argc, string argv[])

{

    int k;
    
    if (argc==2)
    {
        k = atoi(argv[1]);
        char* haha = argv[1];
        
        for(int i = 0; haha[i] != '\0'; ++i)   //digit checking routine
        {
             if(isdigit(haha[i])==0)
             {
                printf("Usage: ./caesar key \n");
                return 1;
                
            }
        }
        
          string text = get_string("plaintext: ");
        printf("ciphertext: ");

        for(int l =0; text[l] != '\0'; ++l)  //char switch loop
    {
        
        
        if(isalpha(text[l])) //is it alpha check
        {
            
            
            
            if(isupper(text[l])) // is it upper check
            {
               text[l]=text[l]-65; 
               text[l]=(text[l]+k)%26;
               text[l]=text[l]+65;
               
            }
            else if(islower(text[l])) // is it lower check
            {
                text[l]=text[l]-97; 
               text[l]=(text[l]+k)%26;
               text[l]=text[l]+97;
            }
            
            
            
        }
        
        printf("%c", text[l]);
    }
    printf("\n");
        
    }


    if((argc>2 || argc<2)) //if more or less than 2 entries in commandline
    {
        printf("Usage: ./caesar key \n" );
        return 1;
        
    }



}

