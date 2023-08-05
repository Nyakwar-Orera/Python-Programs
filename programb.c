#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void getComment(size_t len, char *src){
  size_t size;
  size = len - 2;
  printf("Received string: %s\n", src);
  char *comment = (char*)malloc(size+1);
  memcpy(comment, src, size);
  puts("String copied successfully\n");
}

int main(int argc, char *argv[]){
  
  if (argc < 2){
    puts("No arguments. Include length and message as command line arguments.");
    return -1;
  }

  int len = atoi(argv[1]);
  char* msg = argv[2];
  getComment(len, msg);


  return 0;
}