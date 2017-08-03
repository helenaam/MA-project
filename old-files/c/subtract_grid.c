#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main(int argc, char* argv[]){
  if(argc <= 2){
    printf("Usage: ./subtract r row1 row2 row3 ... c col1 col2 col3 ...\nType 'x' for an empty row/column\n");
    return -1;
  } else{
    int i = 2;
    int j;
    float diff;
    /*
    for(i = 1; i < argc; i++){
      printf("%s\t", argv[i]);
    }
    for(i = 1; i < argc; i++){
      printf("\n%s\t", argv[i]);
      for(j = 1; j < argc; j++){
	if(strcmp("x", argv[i]) && strcmp("x", argv[j])){
	  diff = strtof(argv[i], NULL) - strtof(argv[j], NULL);
	  if(diff == 0){
	    printf("0\t");
	  } else{
	    printf("%.2f\t", diff);
	  }
	} else{
	  printf("x\t");
	}
      }
      printf("\n");
    }
    printf("\n\n");
    */
    if(strcmp(argv[1], "r") && strcmp(argv[1], "c")){
      printf("Usage: ./a.out r row1 row2 row3 ... c col1 col2 col3 ...\nType 'x' for an empty row/column\n");
    } else if(!strcmp(argv[1], "c")){ //I think this one doesn't work right now
      printf("\n\n\t");
      //set up the columns
      while(strcmp(argv[i], "r")){
	printf("%s\t", argv[i]);
	i++;
      }
      int k;
      for(k = i+1; k < argc; k++){
	printf("\n%s\t", argv[k]);
	for(j = 2; j < i; j++){
	  if(strcmp("x", argv[i]) && strcmp("x", argv[j])){
	    diff = strtof(argv[i], NULL) - strtof(argv[j], NULL);
	    if(diff == 0){
	      printf("0\t");
	    } else{
	      printf("%.2f\t", diff);
	    }
	  } else{
	    printf("x\t");
	  }
	  printf("\n");
	}
      }
      printf("\n");
    } else{ //This one works
      printf("\n\n");
      //move the index to the start of the list of columns
      while(strcmp(argv[i], "c")){
	i++;
      }
      //set up the columns
      for(j = i+1; j < argc; j++){
	//printf("%s\t", argv[j]);
      }
      int k;
      for(j = 2; j < i; j++){
	//printf("\n%s\t", argv[j]);
	for(k = i+1; k < argc; k++){
	  if(strcmp("x", argv[k]) && strcmp("x", argv[j])){
	    diff = strtof(argv[j], NULL) - strtof(argv[k], NULL);
	    if(diff == 0){
	      printf("0\t");
	    } else{
	      printf("%.2f\t", diff);
	    }
	  } else{
	    printf("x\t");
	  }
	}
	printf("\n");
      }
    }
  }
  return 0;
}
