from fuzzinglab import fuzzer, heartbeat

# Lab Task 1

# Task 1.1
for _ in range(20):
  output = fuzzer(5, 48, 10)  # Generate fuzzer output with digits
  print(output)

# Task 1.2
for _ in range(20):
  output = fuzzer(20, 65, 26)  # Generate fuzzer output with uppercase letters
  print(output)

# Lab Task 2
'''#############################'''
'''Values for secret data in memory initialized below -- this is required for 3b and should not be changed'''
secrets = ("<space for reply>" + fuzzer(100) + "<secret-certificate>" +
           fuzzer(100) + "<secret-key>" + fuzzer(100) + "<other-secrets>")
uninitialized_memory_marker = "!SECRET!"
while len(secrets) < 2048:
  secrets += uninitialized_memory_marker
'''##############################'''

# Task 3: Add your code for Task 3
