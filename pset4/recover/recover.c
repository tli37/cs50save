#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{


    if ( argc < 2 || argc > 2)
    {
        printf("Usage: ./recover image \n");
        return 1;
    }


    FILE* f = fopen(argv[1], "r");

    BYTE buff[512];
    BYTE buffwrite[512];
    char writechar[512];
    
 
    int jpegcounter=0;
    
    int stop=0;
    int j =0;
    int fileopen=0;
    FILE* img = NULL;

    
    while ( stop == 0 )
    {
        
        fread(buff, sizeof(BYTE), 512, f);
        
        if (feof(f))
       {
           
           stop = 1;
           fileopen = 0;
          
       }
        
       if (buff[0]== 0xff && buff[1]== 0xd8 && buff[2] == 0xff && (buff[3] & 0xf0) == 0xe0 )
       {
            
            if (fileopen == 1)
            {
                fclose(img);
            }
            
            sprintf(writechar,"%03i.jpg", (jpegcounter));
            
            img = fopen(writechar, "w");
            
            fwrite(buff, sizeof(BYTE), 512, img);
            
            jpegcounter++;
            fileopen= 1;
        
       }
       else if (fileopen == 1)
       {
            fwrite(buff, sizeof(BYTE), 512, img);
       }
       
    }
    
    fclose(img);
    return 0;
}
