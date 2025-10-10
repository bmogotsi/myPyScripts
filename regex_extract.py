import re

"""
    extracting data from a string, using regex pattern
         Extract  using start position and end position
         
"""

# string = "hello world, i am Ben Mogotsi, i live in South Africa"
string = "hello world, i am 1Ben9 Mogotsi, i live in South Africa"
# pattern = re.compile(r"\b\w{3}\b")
pattern = re.compile(r"\d\w{3}\d")
match = pattern.search(string)
print(match.group()) # Ben
print(match.start() ) # 18
print(match.end() ) # 21
print(match.endpos ) # 53 end position of the string
print(match.pos ) # 0 start position of the string
print(match.re) # <_sre.SRE_Pattern object; pattern='\\b\\w{3}\\b'>
print(match.string) # hello world, i am Ben Mogotsi, i live in South Africa
print(match.lastindex) # 1
print(match.lastgroup) # Ben
print(match.groups()) # ()
print(match.groupdict()) # {}
print(match.group(0)) # Ben
# print(match.group(1)) # None
print(match.groups()) # ()
print(match.span()) # (18, 21)
quit()
