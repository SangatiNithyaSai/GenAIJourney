import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text="Hey threr! My name is Nithya Sai"
tokens=enc.encode(text)
#Tokens: [25216, 11622, 259, 0, 3673, 1308, 382, 478, 437, 2090, 98894]
print("Tokens:",tokens)

decoded=enc.decode([25216, 11622, 259, 0, 3673, 1308, 382, 478, 437, 2090, 98894])
print("Decoded:",decoded)
