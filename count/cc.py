



with open("secret.txt", "r") as f:
    s = f.read()

r = 0
for v in s.split(" "):
    print(v)
    print(len(v))
    r += len(v)
print(r)
