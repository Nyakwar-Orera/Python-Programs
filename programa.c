//#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char* argv[]) {

  if (argc == 0){
    puts("No arguments provided.\nCall program with command line argument for message string.");
    return -1;
  }

  int i = 0;
  char buff[16];
  char *arg1 = argv[1];

  while (arg1[i] != '\0'){
    buff[i] = arg1[i];
    i++;
  }

  buff[i]='\0';
  printf("buff = %s\n", buff);
  
  return 0;

}