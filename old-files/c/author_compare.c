#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int count_auth(const char* reference){
  int count = 0;
  int num_commas = 0;
  char curr = reference[0];
  int i = 0;
  while(curr != '('){
    if(curr == ',' && (reference[i+2] != 'J' || reference[i+3] != 'r' || reference[i+4] != '.')){
      num_commas++;
    }
    i++;
    curr = reference[i];
    if(num_commas == 2){
      count++;
      num_commas = 0;
    }
  }
  count++;
  return count;
}

/* Returns the maximum number of letters in an author of the given reference */
int max_letters(const char* reference){
  return 50;
}

/* Returns a list of all the authors in the given reference */
char** get_authors(const char* reference){
  //Allocate memory
  int num = count_auth(reference);
  char** authors = calloc(num, sizeof(char*));
  int i;
  for(i = 0; i < num; i++){
    authors[i] = calloc(max_letters(reference), sizeof(char));
  }
  int pos = 0;
  int row;
  int col = 0;
  int commas;
  char c = reference[pos];
  //Move past the * at the beginning of the reference
  if(c == '*'){
    pos++;
    c = reference[pos];
  }
  for(row = 0; row < num; row++){
    commas = 0;
    col = 0;
    //Store characters into author until second comma is reached
    while(commas < 2){
      authors[row][col] = c;
      col++;
      pos++;
      c = reference[pos];
      if(c == ','){
	commas++;
      } else if(c == '('){
	//Get rid of space at the end of the last author
	authors[row][col - 1] = '\0';
	break;
      }
    }
    //Skip over comma and space between authors
    pos += 2;
    c = reference[pos];
    //Remove ampersand if present
    if(c == '&'){
      pos += 2;
      c = reference[pos];
    }
    authors[row][col] = '\0';
    //Remove ellipsis if present
    if(authors[row][0] == '.' && authors[row][2] == '.' && authors[row][4] == '.'){
      for(i = 6; i <= col; i++){
	authors[row][i-6] = authors[row][i];
      }
    }
    //If " Jr." is after the comma, put this at the end of the author
    if(c == 'J' && reference[pos + 1] == 'r' && reference[pos + 2] == '.'){
      authors[row][col] = ',';
      authors[row][col + 1] = ' ';
      authors[row][col + 2] = 'J';
      authors[row][col + 3] = 'r';
      authors[row][col + 4] = '.';
      authors[row][col + 5] = '\0';
      pos += 5;
      c = reference[pos];
      if(c == '('){
	
      }
    }
  }
  return authors;
}

/* Compares every author in reference1 to every author in reference2
 * and returns the number of authors they have in common */
int compare(const char* ref1, const char* ref2){
  char** auth1 = get_authors(ref1);
  char** auth2 = get_authors(ref2);
  int i;
  int j;
  int common = 0;
  for(i = 0; i < count_auth(ref1); i++){
    for(j = 0; j < count_auth(ref2); j++){
      if(!strcmp(auth1[i], auth2[j])){
	common++;
      }
    }
  }
  /*
  for(i = 0; i < count_auth(ref1); i++){
    free(auth1[i]);
  }
  for(j = 0; j < count_auth(ref2); j++){
    free(auth2[i]);
  }
  free(auth1);
  free(auth2);
  */
  return common;
}

/* Returns the total number of distinct authors in the two references */
int get_total_authors(const char* ref1, const char* ref2){
  return count_auth(ref1) + count_auth(ref2) - compare(ref1, ref2);
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
    char* citation = calloc((entry_length + 1), sizeof(char));
    fseek(inputStream, -entry_length, SEEK_CUR);
    fgets(citation, entry_length, inputStream);
    return citation;
  }
  return NULL;
}

int main(int argc, char* argv[]){
  if(argc < 2 || argc > 3){
    printf("Usage: %s input_file [-c]\n", argv[0]);
    return -1;
  }
  if(argc == 2 || argc == 3){
    //Open input file, make sure it is not null
    FILE* inputFile = fopen(argv[1], "r");
    if(!inputFile){
      printf("Could not open %s\n", argv[1]);
      return -1;
    }
    //Count references in the file
    int numRef = 0;
    char c = getc(inputFile);
     while(c != EOF){
       if(c == '\n'){
	 numRef++;
       }
       c = getc(inputFile);
     }
     numRef /= 2;
     //numRef++;
     //Go back to beginning of file
     fseek(inputFile, 0, SEEK_SET);
     //Store references into array
     char** references = calloc(numRef, sizeof(char));
     int i;
     for(i = 0; i < numRef; i++){
       references[i] = calloc(strlen(nextEntry(inputFile)) + 1, sizeof(char));
     }
     fseek(inputFile, 0, SEEK_SET);
     for(i = 0; i < numRef; i++){
       references[i] = nextEntry(inputFile);
     }
     //Compare each pair of references
     int j;
     if(argc > 2 && !strcmp(argv[2], "-c")){
       int common;
       int total;
       for(i = 0; i < numRef; i++){
	 for(j = 0; j < i; j ++){
	   printf("\t");
	 }
	 for(j = i + 1; j < numRef; j++){
	   common = compare(references[i], references[j]);
	   total = get_total_authors(references[i], references[j]);
	   printf("%.2f\t", (float)common/total);
	 }
	 printf("\n");
       }
       return 0;
     }
     printf("\n------------------\n\n");
     for(i = 0; i < numRef; i++){
       char** authors = get_authors(references[i]);
       int num_authors = count_auth(references[i]);
       printf("%s\t%s\n", authors[0], authors[num_authors - 1]);
       for(j = 0; j < num_authors; j++){
	 free(authors[j]);
       }
       free(authors);
     }
     
     for(i = 0; i < numRef; i++){
       free(references[i]);
     }     
     //free(references);
     return 0;
  }
}
