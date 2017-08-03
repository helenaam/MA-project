#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main(int argc, char* argv[]){
  if(argc <= 2){
    printf("Usage: ./format pt1 pt2 pt3 ...\nType 'x' for an empty data point\n");
    return -1;
  } else{
    int i;
    for(i = 1; i < argc; i++){
      if(strcmp(argv[i], "x")){
	printf("%s\n", argv[i]);
      } else{
	printf("\n");
      }
    }
  }
  return 0;
}
