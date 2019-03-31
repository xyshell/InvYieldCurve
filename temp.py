
with open('i.txt', 'w') as f:
    f.write('0')
x = 1
with open('i.txt', 'r') as f:
    i = int(f.read())
with open('i.txt', 'w') as f:
    f.write(str(i))