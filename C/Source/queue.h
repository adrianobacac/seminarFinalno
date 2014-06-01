#include "header.h"


void initQueue(Queue *queue){
	queue->start=NULL;
	queue->end=NULL;
}

int put(Queue *queue, Node *node ){
	Atom *news=malloc(sizeof(Atom));

	news->content=node;
	if(queue->start==NULL){
		news->next=NULL;
		queue->start=queue->end=news;
	}else{
		news->next=queue->start;
		queue->start=news;
	}

	return 1;
}

int get(Queue *queue, Node **ret){
	if(queue->end==NULL){
		return 0;
	}
	*ret=queue->end->content;
    free(queue->end);
	if(queue->end==queue->start){
		queue->start=queue->end=NULL;
	}else{
		Atom *pom;
		for(pom=queue->start;pom->next!=queue->end;pom=pom->next);
        queue->end=pom;
	}
	return 1;
}


