file = open("fantasy-solution.pddl")

content = file.readlines()
# countFile = content.split("\n")

prompt = ""

count = 0

# .length of the file (total number of the lines)
for i in content:
    if i:
        count += 1

lines = []

# make an array for 2 - .length-1
i = 2
while i != count:
    lines.append(i)
    i += 1

for pos, lineNum in enumerate(content):
    if pos in lines:
        prompt = lineNum
        print(prompt) 

file.close()

#with an array instead

content = file.readlines()
# countFile = content.split("\n")

prompt = []

count = 0

# .length of the file (total number of the lines)
for i in content:
    if i:
        count += 1

lines = []

# make an array for 2 - .length-1
i = 2
while i != count:
    lines.append(i)
    i += 1

for pos, lineNum in enumerate(content):
    if pos in lines:
        prompt.append(lineNum)
        #print(prompt) 

file.close()