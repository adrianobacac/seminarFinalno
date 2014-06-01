#include "header.h"
#include "structs.h"

void freeChildren(Node *base){
	int i;

	if(base->childrenCount==0){
        if(base->content!=NULL){
            free(base->content);
        }
        free(base->name);
		return;
	}
	for(i=0;i<base->childrenCount;i++){
		freeChildren(base->children[i]);

		free(base->children[i]);
	}
    free(base->children);
    if((base->content)!=NULL){

        free(base->content);
    }
    free(base->name);
	return;
}

void freeAll(acalgo *base){
    int i;
    printf("OSLOBADAM MEMORIJU\n");

    for(i=0; i<base->wordsCount;i++){  //tu mozda mogu spojit u jedno, probaj.. kasnije.. mozda..
        free(base->pos[i]);
}
    for(i=0; i<base->wordsCount;i++){
        free(base->words[i]);
    }
    free(base->words);



    free(base->pos);
    free(base->posCount);
    freeChildren(base->root);
	free(base->root);

}
