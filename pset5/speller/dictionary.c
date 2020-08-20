// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 101;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int walkcount=0;
    int index = hash(word);
    //printf("index of has : %i \n", index);

    node *cursor = table[hash(word)];

    while ( cursor != NULL)
    {
        if ( strcasecmp(cursor->word, word) == 0 )
        {
            //printf("walkcount succsess : %i \n", walkcount);
            //printf("succ word : %s \n", cursor->word);
            return true;
        }
        else
        {
            cursor = cursor->next;
            walkcount++;
        }


        if( cursor == NULL)
        {
             // printf("walkcount failed: %i \n", walkcount);
            return false;
        }

    }

    printf("walkcount failed: %i \n", walkcount);
    return false;
}

// Hashes word to a number

// source
//https://stackoverflow.com/questions/4384359/quick-way-to-implement-dictionary-in-c
// Section 6.6 of The C Programming Language
//changed to lowercase letters for hash, seemd to be bug with uppercase...

unsigned int hash(const char *word)
{

    unsigned hashval;
    char newword= tolower(*word);
    for (hashval = 0; newword != '\0'; newword++)
    {
        hashval = newword + 31 * hashval;
    }
    return (hashval % N);

}


int sizecount=0;
int open=0;

bool load(const char *dictionary)
{

    FILE* Text1 = fopen(dictionary, "r");
    char buff[LENGTH+1];

    if (Text1 ==  NULL )
    {
        open = 0;
        return false;
    }
    else
    {
        open = 1;
    }

    while( fscanf(Text1,"%s", buff) != EOF )
    {

        //printf("buffvector %s \n", buff);

        node *newN = malloc(sizeof(node));

        if (newN == NULL)
        {
            return false;
        }

        newN->next= NULL; //set to NUll to begin with,

        strcpy(newN->word, buff); //copy string

        newN->next = table[hash(buff)]; // set adress to old linked list

        // hashtable somewhere
        table[hash(buff)] = newN; // linked list adress to new node.

        sizecount++;
    }

   //  printf("sizecount is %i", sizecount);

    fclose(Text1);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{

    if (open == 1)
    {
        return sizecount;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tmp = NULL;
    node *cursor = NULL;

    for ( int i = 0 ; i <= N ; i++)
    {
        tmp = table[i];
        cursor = table[i];

        while ( cursor != NULL )
        {
            tmp=cursor;
            cursor = cursor->next;
            free(tmp);
        }

    }
    return true;
}
