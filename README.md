# Module 5 Lab - Fuzzing Intro

Instructions for the lab tasks are below.

fuzzer and heartbeat functions for this part of the lab are defined in the fuzzinglab.py file in this replit. 

C programs programa.c and programb.c are included as files in this replit. These can be compiled here by switching to the Shell window at the right side of the screen and entering the compiler instructions in Part 3 below.  

## Part 1

### How to use given fuzzer function  

The fuzzer function generates a random string of characters that can be customized by the user.  

**fuzzer(max_length, char_start, char_range)**  

- *max_length* is maximum length of fuzzer output    

Characters in the output can be from a range of characters in the ascii table.  

- *char_start* is the starting character
- *char_range* is the number of characters following that starting character.  

These two parameters need to be the decimal representation of the character. Check the asciitable linked here for the decimal values of characters: [AsciiTable.com](https://www.asciitable.com/)
 

### Task 1
Use loop to generate and print 20 fuzzer outputs of only digits with max length 5  
### Task 2 
Use loop to generate and print 20 fuzzer outputs of only capital (uppercase) letter output with max length 20


## Part 2
Use fuzzer input to test heartbeat function 
### how to use given heartbeat function  

heartbeat(reply, length, memory)  

The heartbeat function takes in a reply, length, and memory, and returns what should be the reply.  

- reply is a user provided string  
- length is an integer value  
- memory is a string that represents the computer memory (this is the secrets string created in main.py)  

For example, `heartbeat("bird", 4, memory=secrets)` should return a value of `bird`  

### Task 1
Use a loop to call the given heartbeat function 150 times, using the given fuzzer function for the reply and the length values.  
- For *reply*, use the given fuzzer function to generate fuzzing input of max length 250, using lowercase characters only  
- For *length*, use the given fuzzer function to generate fuzzing input of max length 3, using numeric characters only  
- Keep memory=secrets for the third parameter.
- If the string returned includes the uninitialized memory marker or the word 'secret', display an error message
- This can use an assert statement like the example we did in class, or you can check the string and display your own error message

## Part 3

### Overview

This part of the lab uses the C program programa.c program that is included in this replit. You can compile the C programs by switching to the Shell window at the right.   

### Task 1: First compile as usual.  
`clang -g -o programa programa.c`

### Task 2: Run the program 
- This program expects a command line argument of a message string. The message can be one word or multiple words. Enclose a message with multiple words with quote marks ''. For example,
`./programa hello` or `./programa 'hello world'`  
- Test messages of different lengths on the command line to see if you can cause a buffer overflow.   

### Task 3: Compile with address sanitizer option turned on.  
`clang -g -o programa -fsanitize=address programa.c`

### Task 4: Run the program again. 
- Try similar input as before. Check for output from the sanitizer that identifies the overflow issue.  


## Part 4

### Overview 

This part of the lab uses the C program programb.c program that's included in this replit. You can compile the C programs by switching to the Shell window at the right.   

### Task 1: First compile as usual.  
`clang -g -o programb programb.c`

### Task 2: Run the program 
- This program expects command line arguments of a length and a message string. Enclose a message with multiple words with quote marks ''. For example, `./programb 8 'hello !'`  
- Test length values with different integer values to see if you can cause a memory error (segmentation fault).   

### Task 3: Compile with sanitizer option turned on.  
clang -g -o programb -fsanitize=signed-integer-overflow programb.c

### Task 4: Run the program again. 
- Try similar input as before. Check for output from the sanitizer that identifies integer, memory, or undefined behavior issues.  


----

Code adapted from fuzzingbook.org and shared under the same license conditions. [License](https://github.com/uds-se/fuzzingbook/blob/master/LICENSE.md)