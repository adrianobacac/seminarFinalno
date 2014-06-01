
typedef struct nod{
	struct nod **children;
	int childrenCount;
	struct nod *fail;
	char * content;
	char * name;
	char value;
    int debth;
}Node;

typedef struct{
	Node *root;
	Node *state;
	char **words;
	int **pos;
	int wordsCount;
	int *posCount;
}acalgo;

typedef struct at{
	struct at *next;
	Node *content;
}Atom;

typedef struct{
	Atom *start;
	Atom *end;
}Queue;

