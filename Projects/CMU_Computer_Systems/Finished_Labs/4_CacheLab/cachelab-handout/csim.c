#include <math.h>  // For pow(x,y)
#include <stdio.h>
#include <stdlib.h>  // For atoi()
#include "cachelab.h"
#include "getopt.h"  // For getopt()


// for reference: ./csim-ref -v -s 4 -E 1 -b 4 -t traces/yi.trace
void parse(int* s_ptr, int * S_ptr, int * E_ptr, int *b_ptr, int* B_ptr,
char ** file_path_ptr, int argc, char * argv[]){

    int opt;
    while((opt=getopt(argc,argv,"s:E:b:t:"))!=-1){
        switch (opt){
            case 's':
                *s_ptr = atoi(optarg);
                *S_ptr = pow(2,*s_ptr);
                break;
            case 'E':
                *E_ptr = atoi(optarg);
                break;
            case 'b':
                *b_ptr = atoi(optarg);
                *B_ptr = pow(2,*s_ptr);
                break;
            case 't':
                *file_path_ptr = optarg;
                break;
            default:
                printf("Error, incorrect program option");
                exit(1);
        }

    }

    if(*S_ptr <= 0 || *E_ptr <=0 || *B_ptr <=0 || file_path_ptr == NULL){
        printf("Error, invalid program option input");
        exit(1);
    }

}

typedef struct cache_line{
    int access_time; 
    int valid_bit;
    long long tag;
} cache_line_t;

typedef cache_line_t *cache_line_ptr;

cache_line_ptr * init_cache(int S, int E){
    int set, line;
    cache_line_ptr * cache; 

    cache =  malloc(S * E * sizeof(cache_line_ptr));
    cache_line_ptr curr_cache_line;

    for(set = 0; set < S; set++){
        for(line = 0; line < E; line++){
            *(cache+set*E+line) = malloc(sizeof(cache_line_t));
            curr_cache_line =  *(cache+set*E+line);
            curr_cache_line->valid_bit = 0;
        }
    }

    return cache;

}

FILE * openfile(char * file_path, char * mode){
    FILE * file = fopen(file_path,mode);
    if(!file){
        printf("Error opening file %s", file_path);
        exit(1);
    }
    return file;
}

int cache_hit(int set, int E, cache_line_ptr * cache, 
int tag_bits, int * hit_ptr, int time){
    int line;
    cache_line_ptr * start = cache + E * set;
    cache_line_ptr curr_cache_set_ptr;
    for(line = 0; line < E; line++){
        curr_cache_set_ptr = *(start+line);
        if(curr_cache_set_ptr->tag == tag_bits && curr_cache_set_ptr->valid_bit){
            ++(*hit_ptr);
            curr_cache_set_ptr->access_time = time;
            printf("hit");
            return 1;
        }
    }
    return 0;
}

int cache_empty(int set, int E, cache_line_ptr * cache, 
int tag_bits, int * miss_ptr, int time){
    int line;
    cache_line_ptr * start = cache + E * set;
    cache_line_ptr curr_cache_set_ptr;
    for(line = 0; line < E; line++){
        curr_cache_set_ptr = *(start + line);
        if(!curr_cache_set_ptr->valid_bit){
            ++*(miss_ptr);
            curr_cache_set_ptr->valid_bit = 1;
            curr_cache_set_ptr->access_time = time;
            curr_cache_set_ptr->tag = tag_bits;
            printf("miss");
            return 1;
        }
    }
    return 0;
}

cache_line_ptr find_replace(cache_line_ptr * start, int E, int time){
    int line;
    int min_time = time;
    cache_line_ptr min_ptr = NULL;
    for(line = 0; line < E; ++line){
        cache_line_ptr curr_ptr = *(start + line);
        if(curr_ptr->access_time < min_time){
            min_time = curr_ptr->access_time;
            min_ptr = curr_ptr;
        }
    }
    return min_ptr;
}
    

void replace(int set, int E, cache_line_ptr *cache,
             int tag_bits, int *miss_ptr, int *evict_ptr, int time) {
    cache_line_ptr * start = cache + set * E;
    cache_line_ptr min_ptr = find_replace(start, E, time);
    min_ptr->valid_bit = 1;
    min_ptr->access_time = time;
    min_ptr->tag = tag_bits;
    ++(*miss_ptr);
    ++(*evict_ptr);
    printf("miss evict");
}


int load_to_cache(int set, int E, cache_line_ptr * cache, int tag_bits,
int * hit_ptr, int * miss_ptr, int * evict_ptr, int time){
//check if hit
if(cache_hit(set,E,cache,tag_bits,hit_ptr,time)){
    return 0;
}
//check if empty
if(cache_empty(set,E,cache,tag_bits,miss_ptr,time)){
    return 1;
}
//check if evict
replace(set,E,cache,tag_bits,miss_ptr,evict_ptr,time);
return 2;
}

int main(int argc, char * argv[]){
    int s,S,E,b,B;
    char * file_path;
    int set;
    cache_line_ptr * cache;
    FILE * file;


    char * operation_ptr;
    char operation;
    long long address;  // long long used for 64-bit address
    int size;
    long long unsigned set_mask, set_bits, tag_bits;
    int hit,miss,evict,time;

    //parse to obtain size parameters
    s = S = E = b = B = 0;
    file_path = NULL;
    parse(&s,&S,&E,&b,&B,&file_path,argc,argv);
    printf("s= %d, E= %d, b= %d, filename=%s\n",s,E,b,file_path);

    //initializing cache
    cache = init_cache(S,E);

    //reading file
    file = openfile(file_path,"r");

    //analysis of line from file
    operation_ptr = malloc(2*sizeof(char));
    hit = miss = evict = time = 0;
    set_mask = ~((-1)<<s);
    while(fscanf(file, "%s %llx,%d\n", operation_ptr, &address, &size) != EOF){
        ++time;
        operation = *operation_ptr;
        set_bits = (address >> b) & set_mask;
        tag_bits = (address >> (b+s));

        set = set_bits;
        if (operation == 'L') {
            load_to_cache(set, E, cache, tag_bits, &hit, &miss, &evict, time);
        } else if (operation == 'S') {
            load_to_cache(set, E, cache, tag_bits, &hit, &miss, &evict, time);
        } else if (operation == 'M') {
            load_to_cache(set, E, cache, tag_bits, &hit, &miss, &evict, time);

            // The writing operation would always head for "M"
            ++hit;
            printf("hit ");
        }
    }
    printSummary(hit, miss, evict);
    return 0;
}