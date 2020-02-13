import re
pattern = "[a-zA-Z0-9]+@[a-zA-z]+\.(com|edu|net)"

user_input = input()
if(re.search(pattern, user_input)):
    print("valid email")
else:
    print("invalid email")
