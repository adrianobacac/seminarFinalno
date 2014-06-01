#include <time.h>
#include <stdio.h>
#include <stdlib.h>



int main(int argc, char *argv[]){
	
	int lenght;
	FILE *f;
	if(!(argc==0 && sscanf(argv[1], "%d", &lenght)==1)){
		do{
		fflush(stdin);
		printf("Duljina niza: ");
		}while(scanf("%d", &lenght)==0);
	}	
	
	srand(time(NULL));
	f=fopen("input.txt", "w");
	while(lenght){
		
		switch (rand()%4){
			case 0:
				fputc('C',f);
				break;
			case 1:
				fputc('G',f);
				break;
			case 2:
				fputc('T',f);
				break;
			case 3:
				fputc('A',f);
				break;
		}
		lenght--;
	}
	fclose(f);
	return 0;
}