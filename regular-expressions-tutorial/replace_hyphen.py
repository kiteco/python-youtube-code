import re

pattern = "(\d\d\d)\-(\d\d\d)-(\d\d\d\d)"

user_input = input()

new_user_input = re.sub(pattern,r"\1\2\3", user_input)

print(new_user_input)
