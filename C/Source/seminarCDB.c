#include "header.h"

#include "free.h"
#include "queue.h"
#include "memory.h"



Node *generateNode(Node **children, int childrenCount, Node *fail, char *content, char *name, char value){
	Node *pom=malloc(sizeof(Node));
	pom->children=children;
	pom->childrenCount=childrenCount;
	pom->fail=fail;
	pom->content=content;
	pom->name=name;
	pom->value=value;
	return pom;
}
void initAcalgo(acalgo *base){
	char * name = malloc(sizeof(char)*5);
	strcpy(name, "root");
	base->root=generateNode(NULL, 0, NULL, NULL, name, 0);
	base->root->fail=base->root;
	base->state=base->root;
	base->wordsCount=0;
	base->words=NULL;
	base->pos=NULL;
	base->posCount=NULL;
}
Node *selectChild(Node *parent, char index){
	int i;
	for(i=0; i < parent->childrenCount; i++){
		if (parent->children[i]->value==index){
			return parent->children[i];
		}
	}
	return NULL;
}

int checkChild(Node parent, char index){
	int i;
	for(i=0; i<parent.childrenCount;i++){

		if(parent.children[i]->value==index){

			return 1;
		}
	}
	return 0;
}
void addChild(Node *parent, char value, char *name){

	parent->children=realloc(parent->children, sizeof(parent->children)*(parent->childrenCount)+sizeof(Node));

	parent->childrenCount++;
	parent->children[parent->childrenCount-1]=generateNode(NULL,0, NULL, NULL, name, value);

}
int findNodeIndex(Node noder, char c){
	int i;
	for(i=0; i<noder.childrenCount; i++){
		if(noder.children[i]->value==c){
			return i;
		}
	}
	return -1;
}
void addContent(Node *noder, char *word){
	char *content=malloc(sizeof(char)*strlen(word)+1);
	strcpy(content, word);

	noder->content=content;

}

void addWordSearch(acalgo *base, char *word){
    base->wordsCount++;

	base->words=(char **)realloc((void*)base->words, sizeof(base->words)*(base->wordsCount));
    base->pos=(int**)realloc(base->pos, sizeof(base->pos)*base->wordsCount);

	base->words[base->wordsCount-1]=malloc(sizeof(char)*(strlen(word)+1));

	strcpy(base->words[base->wordsCount-1],word);

    base->pos[base->wordsCount-1]=malloc(sizeof(int));
    base->posCount=realloc(base->posCount, sizeof(int*)*(base->wordsCount));
    base->posCount[base->wordsCount-1]=0;
   }

int findWordIndex(acalgo *base, char *word){
	int i;
	for(i=0; i<base->wordsCount; i++){
		if(strcmp(base->words[i], word)==0){
			return i;
		}
	}
	return -1;
}
void addWordPos(acalgo *base,char *word ,int poz){
	int index=findWordIndex(base, word);
	base->posCount[index]++;

	base->pos[index]=realloc(base->pos[index], base->posCount[index]*sizeof(int));
	base->pos[index][base->posCount[index]-1]=poz;
}
void addWord(acalgo *base, char *word){
	int i;
	char c, *name;
	Node *noder=(base->root);

	addWordSearch(base, word);

	for(i=0; i<strlen(word); i++){

		if(isalpha(word[i])){
			c=islower(word[i])?word[i]:word[i]+32;
		}
		if(checkChild(*noder, c)==0){
            name=malloc(sizeof(char)*(i+1+1));

			strncpy(name, word,i+1);
			name[i+1]='\0';
			addChild(noder, c, name);

		}
		noder=(noder->children[findNodeIndex(*noder, c)]);
		if(i==strlen(word)-1){
			addContent(noder, word);
		}
	}
}
void addFails(Queue *queue, acalgo *base){
	int i;
	int j;
	int skip=0;
	Node *noder;
    Node *pom;

	for(i=0; i<base->root->childrenCount; i++){

		base->root->children[i]->fail=base->root;

		put(queue, (base->root->children[i]));
	}
	while(get(queue, &noder)){
		for(i=0;i<noder->childrenCount;i++){
			pom=noder->fail;
            skip=0;
			while(checkChild(*pom, noder->children[i]->value)==0){
				if(pom==pom->fail){
					noder->children[i]->fail=pom;
					skip=1;
					break;
				}
				pom=pom->fail;
			}if(skip==0){
				for(j=0; j<pom->childrenCount;j++){
					if(pom->children[j]->value==noder->children[i]->value && pom->children[j]!=noder->children[i]){

						noder->children[i]->fail=pom->children[j];
						break;
					}
				}
			}
			put(queue, (noder->children[i]));
		}

	}
}
Node *nextState(acalgo *base, char c){
	Node *current = base->state;
	while(!checkChild(*current, c)){
		current=current->fail;
		if(checkChild(*current, c)){
            return current->children[findNodeIndex(*current,c)];
		}
		if(current==(current->fail)){
			return current;
		}
	}
	return current->children[findNodeIndex(*current,c)];
}

void checkState(acalgo *base, int pos){
	Node *current = base->state;
	while(current!=base->root){
		if(current->content!=NULL){

			addWordPos(base,current->content , pos-strlen(current->content)+1);
		}
		current=current->fail;
	}
}
void readFile(acalgo *base, char *path){
	FILE *f;
	char c;
	if((f=fopen(path,"r"))==NULL){
        printf("\nNemam sta za procitat!\n");
		return;
	}
	while((c=fgetc(f))!=EOF){
		if(isalpha(c)){
			c=islower(c)?c:c+32;
		}
		base->state=nextState(base,c);
		checkState(base, ftell(f));
	}
	fclose(f);
}




void printEndGame(acalgo *base){
    int i,j;
    printf("\n\n");
    for(i=0; i<base->wordsCount;i++){

        printf("%s <%d>\n", base->words[i], base->posCount[i]);

        for(j=0; j<base->posCount[i];j++){
            if(j!=0){

            printf(", ");
            }
            printf("%d", base->pos[i][j]);
        }printf("\n");
    }
}

int main(){

	Queue queue;
	acalgo base;
    char ulaz[100];
	char path[100];
	initQueue(&queue);
	initAcalgo(&base);
    printf("START\n");
    printf("Dodaj podnizove koji se traze:\n(\\ za izlaz, max broj znakova: 100)\n");
    while(scanf("%s",ulaz)){
		if(strcmp(ulaz, "\\")==0) break;
    	addWord(&base, ulaz);
    }
	printf("\n\n");
	addFails(&queue, &base);
	fflush(stdin);
	printf("Putanja datoteke (max 100): ");

	scanf("%s",&path);
	readFile(&base, path);

    printEndGame(&base);
    freeAll(&base);

	return 0;
}



