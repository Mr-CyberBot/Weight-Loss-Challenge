//Contestant data
//#include "data-manipulator"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define string_length 20

// defines struct contestantDat
struct contestantDat{
char name[string_length];
//int date;
char date[string_length];
int age;
float weight;
float height;
}

resize array

// allocates an array of 10 integers
struct contestantDat *arr = (struct contestantDat*) malloc(10 * sizeof(struct contestantDat));


//checks if mem allocation failed
if (arr == NULL){
  printf("memory allocation failed\n");
  return 1;
}

int resizer = 10;
struct conteestantDat customer[10]
for(int i=0; i < ; i++){
  //creates customer record for tracking specific user data
  customer

  //adding user data
  

  //to resize the array if array is full of users
  if(i == (1-resizer)){
    Resize(arr, 
  }

  //implement exit code for submit button to close the gui and save data to file
}
