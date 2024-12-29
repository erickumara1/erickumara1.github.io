#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "harness.h"
#include "queue.h"

queue_t *q_new(){
    queue_t *q = malloc(sizeof(queue_t));
    
    if(q){
        q->head = NULL;
        q->tail = NULL;
        q->size = 0;
    }
    return q;
}

void q_free(queue_t *q){
    if(q){
        list_ele_t * curr = q->head, * next = NULL;
        while(curr){
            free(curr->value);
            next = curr->next;
            free(curr);
            curr = next;
        }
        free(q);
    }
}

static int stringLength(char *s){
    int count = 0; 
    while(s[count]!='\0'){
        ++count;
    }
    return count+1;
}

bool q_insert_head(queue_t *q, char *s){
    if(!q){
        return false;
    }

    list_ele_t * new_head = malloc(sizeof(list_ele_t)); 
    if(!new_head){
        return false;
    }

    char *new_value = malloc(sizeof(char) * stringLength(s));

    if(!new_value){
        free(new_head);
        return false;
    }

    strcpy(new_value,s);

    new_head->value = new_value;
    new_head->next = q->head;
    q->head = new_head;

    if(!q->tail){
        q->tail = new_head;
    }
    
    ++q->size;
    return true;
}

bool q_insert_tail(queue_t *q, char *s){
    if(!q){
        return false;
    }

    list_ele_t *new_tail = malloc(sizeof(list_ele_t));
    if(!new_tail){
        return false;
    }

    char * new_value = malloc(sizeof(char) * stringLength(s));
    if(!new_value){
        free(new_tail);
        return false; 
    }

    strcpy(new_value,s);
    new_tail->value = new_value; 
    new_tail->next = NULL;

    if(!q->tail){
        q->tail = new_tail;
        q->head = new_tail;
    }
    else{
        q->tail->next = new_tail; 
        q->tail = new_tail;
    }

    ++q->size;

    return true;

}

int q_size(queue_t *q){
    if(!q || !q->head){
        return 0;
    }
    return q->size;
}

bool q_remove_head(queue_t *q, char *sp, size_t bufsize){
    if(!q || !q->head){
        return false;
    }

    list_ele_t *old_head = q->head, *new_head = q->head->next;

    if(sp){
        int i;
        for(i=0; i < bufsize-1 && *(old_head->value+i)!='\0';++i){
            *(sp+i) = *(old_head->value+i);
        }
        *(sp+i) = '\0';
    }

    free(old_head->value);
    free(old_head);

    q->head = new_head; 
    --q->size;
    return true;

}

void q_reverse(queue_t *q) {
    if(q && q->head){
        list_ele_t *old_head = q->head, *old_tail = q->tail;
        list_ele_t *curr = q->head, *prev = NULL, *next = NULL;
        // .....p1 -> p2 -> p3 ->.....
        //.....p1 <- p2 <- p3 ......
        while(curr){
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }

        q->tail = old_head;
        q->head = old_tail;

    }
}