import random

def fuzzer(max_length=100, char_start=32, char_range=32):
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    if out == '':
      out = chr(char_start + char_range)
    if len(out) > 1:
      out = out.lstrip('0')
    return out

def heartbeat(reply, length, memory):
    length = int(length)
    memory = reply + memory[len(reply):]
    s = ""
    for i in range(length):
        s += memory[i]
    return s

