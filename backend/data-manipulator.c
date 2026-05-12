#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

int Calc_Age(const char *DOB);

float Weight_Lost(float *start_weight, float *end_weight);

float Percentage_Lost(float *weight_lost, float *start_weight);

void print_func_val_int(int *age);
void print_func_val_float(float *weight_lost, float *percentage_lost);

//Main method to define args and call functions
int main(int argc, char *argv[]){
    //checks for no commands
    if(argc == 1){
        fprintf(stderr, "ERROR: No commands provided\n");
        return 1;
    }
    
    //runs through all the arguments- the first element since it's the program name, and starting with 1 is how to skip it
    for(int i=1; i < argc;){
        char *command = argv[i];

        if(strcmp(command, "age") == 0){
            if(i+1 >= argc){
                fprintf(stderr, "ERROR: Missing date of birth\n");
                return 1;
            }
            char *date = argv[i+1];
            if(date[4] == '-' && date[7] == '-' && (int)strlen(date) == 10){
                int age = Calc_Age(date);
                if(age == -1){
                    fprintf(stderr, "ERROR: Invalid date of birth\n");
                    return 1;
                }
                print_func_val_int(&age);
                i+=2;
            }
            else{
                fprintf(stderr, "ERROR: Invalid date of birth\n");
                return 1;
            }
        }

        //if command equals weight_lost
        else if(strcmp(command, "weight_lost") == 0){
            //add bounds check for argv[i+1] for this else if and the next
            if(i+2 >= argc){
                fprintf(stderr, "ERROR: Missing starting or current weight\n");
                return 1;
            }
            //assigns start weight
            float start_weight = strtof(argv[i+1], NULL);
            //assigns end weight
            float end_weight = strtof(argv[i+2], NULL);
            //returns weight lost
            float weight_lost = Weight_Lost(&start_weight, &end_weight);
            i+=3;
            print_func_val_float(&weight_lost, NULL);
        }

        //if command = percentage lost
        else if(strcmp(command, "percentage_lost") == 0){
            if(i+2 >= argc){
                fprintf(stderr, "ERROR: Missing weight lost or starting weight\n");
                return 1;
            }
            //assigns the weight lost
            float weight_lost = strtof(argv[i+1], NULL);
            //assigns the start weight
            float start_weight = strtof(argv[i+2], NULL);
            //returns percentage lost
            float percentage_lost = Percentage_Lost(&weight_lost,    &start_weight);
            //prints percentage lost
            print_func_val_float(NULL, &percentage_lost);
            i+=3;
        }
        else{
            fprintf(stderr, "ERROR: Unknown command: %s\n", command);
            return 1;
        }
        
    }
    return 0;
}

int Calc_Age(const char *DOB){
/*This function follows these steps in order. 1, calculates the current year, month, and date and places them in there variables. 2, runs a for-loop and parses the string through*/

    //gets current time in seconds
    time_t seconds = time(NULL);
    //uses local time struct to calculate current time
    struct tm* current_time = localtime(&seconds);
    //gets current year
    int current_year = current_time->tm_year + 1900;
    //gets current month
    int current_month = current_time->tm_mon + 1;
    //gets current day
    int current_day = current_time->tm_mday;

    //extracts the birth(b) year, month, and day from the date given
    char b_year [5];
    char b_month [3];
    char b_day [3];
    //j for the loop to make sure the dates array num is not mixed up with the other array num
    int j = 0;
    for(int i=0; i < (int)strlen(DOB); i++){
        
        if(i < 4){
            b_year[j] = DOB[i];
            j++;
        }
        else if(i == 4){
            j = 0;  // reset for b_month
        }
        else if(i >= 5 && i < 7){
            b_month[j] = DOB[i];
            j++;
        }
        else if(i == 7){
            j = 0;  // reset for b_day
        }
        else if(i > 7){
            b_day[j] = DOB[i];
            j++;
        }
    }
    b_year[4] = '\0';
    b_month[2] = '\0';
    b_day[2] = '\0';
    //validate future date
    if(atoi(b_year) > current_year || 
      (atoi(b_year) == current_year && atoi(b_month) > current_month) ||
      (atoi(b_year) == current_year && atoi(b_month) == current_month && atoi(b_day) > current_day)){
        return -1;
    }

    //converts year string to integer
    int year_born = atoi(b_year);
    //calculates age
    int age = current_year - year_born;

    if(atoi(b_month) > current_month || (atoi(b_month) == current_month && atoi(b_day) > current_day)){
        age-=1;
    }
    return age;
}

float Weight_Lost(float *start_weight, float *end_weight){
    return *start_weight - *end_weight;
}

float Percentage_Lost(float *weight_lost, float *start_weight){
    if(*start_weight <= 0){
        return 0.0;
    }
    return (*weight_lost / *start_weight) * 100.0;
}

void print_func_val_int(int *age){
    // for age
    printf("%d\n", *age);
}
void print_func_val_float(float *weight_lost, float *percentage_lost){
    // for weight_lost
    if(weight_lost != NULL) printf("%.2f\n", *weight_lost);

    // for percentage_lost
    if(percentage_lost != NULL) printf("%.2f\n", *percentage_lost);
}
