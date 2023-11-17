import openai
import json

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
        prompt = "Continue the chapter based off the previous one where " + lineNum
        #print(prompt) 

file.close()

#count *= 2

postprompt = "Write a full length chapter based story, including dialogue and natural progression, starting from the first chapter to chapter number " + str(count) + "based on the following steps where each line is a new chapter: " #+ prompt


completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are a romance and adventure story teller."}] 
    + [{"role": "user", "content" : postprompt}]
    + [{"role": "user", "content": line} for line in prompt]
    + [{"role": "assistant", "content": "Rory confesses exuberantly, \"I want to spend the rest of my life with you!\""}]
    + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
    + [{"role": "assistant", "content": "In a statement like (travel rory village cave), the meaning is: 'Rory travels from the village to the cave' ."}]
    )

output = open("story.txt", "w")
stroutput = str(completion["choices"][0].message["content"])
output.write(stroutput)
output.close()

print(completion["choices"][0].message["content"])
# print(completion["choices"][0].message["content"], file=output)
# print(completion.choices[0].message)
