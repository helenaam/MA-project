#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

_Bool load(const char* filename){
  //Open input file, make sure it is not null
  FILE* input;
  input = fopen(filename, "r");
  if(input == NULL){
    printf("Can't open %s\n", filename);
    return false;
  }
  return true;
}

//Return the next entry
char* nextEntry(FILE* inputStream){
  char c;
  int entry_length = 1;
  if(!feof(inputStream)){
    //Move past any whitespace between current pos and beginning of next command
    c = fgetc(inputStream);
    while(c == '\n' || c == ' ' || c == '\t'){
      c = fgetc(inputStream);
    }
    //Return null if reached end of file
    if(feof(inputStream)){
      return NULL;
    }
    //Find length of entry by counting characters until newline
    while(c != '\n' && c != EOF){
      entry_length++;
      c = fgetc(inputStream);
    }
    //Store entry into string (citation)
    char* citation = malloc((entry_length + 1) * sizeof(char));
    fseek(inputStream, -entry_length, SEEK_CUR);
    fgets(citation, entry_length, inputStream);
    return citation;
  }
  return NULL;
}

int main(int argc, char* argv[]){
  if(argc != 2){
    printf("Usage: ./a.out input_file\n");
    return -1;
  }
  if(argc == 2){
    //Open input file, make sure it is not null
    FILE* inputFile = fopen(argv[1], "r");
    if(!inputFile){
      printf("Could not open %s\n", argv[1]);
    }
    //Evaluate each message until end of file                                                
    while(!feof(inputFile)){
      char* citation = nextEntry(inputFile);
      if(citation != NULL && !strncmp(citation, "*", 1)){
	printf("\n%s\n", citation);
      }
    }
    printf("\n");
    return 0;
  }
}
