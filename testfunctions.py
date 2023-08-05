#########################
# function to be tested
'''
The rank_scores function takes in a score and converts it to a rank, using a complicated structure of if/else statements.
'''
# specifications 
'''
score              rank
100000 or higher   10
90000 or higher     9
75000 to 89999      8
50000 to 74999      7
25000 to 49999      6
10000 to 24999      5
5000 to 9999        4
1000 to 4999        3
500 to 999          2
1 to 499            1
0                   0
negative            -1
'''
#########################


def rank_scores(score):
  try:
    score = int(score)
  except: 
    raise ValueError("Score not an integer value")
  rank = 0
  if score >= 50000:
    if score >= 100000: 
      rank = 10
    elif score >= 90000:
      rank = 9
    elif score >= 75000: 
      rank = 8
    else: 
      rank = 7
  elif score >= 5000: 
    if rank >= 25000: 
      rank = 6
    elif rank >= 10000: 
      rank = 5
    else:
      rank = 4
  elif score >= 1:
    if score >= 5000: 
      rank = 3 
    elif score >= 1000: 
      rank = 2
    else: 
      rank = 1 
  elif score <= 0: 
    if score == 0:
      rank = 0
    else: 
      rank = -1
  return rank

# pause waits for a key to be pressed before continuing with the next line of the program
def pause():
  input("\npress enter to continue\n\n")