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

postprompt = "Write the first chapter of a story, including dialogue and natural progression, based on the following: " 

story = ""
previousChapter = ""


completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are a story teller beginning a story."}] 
    + [{"role": "user", "content" : (postprompt + prompt[0])}]
    + [{"role": "assistant", "content": "Rory confesses exuberantly, \"I want to spend the rest of my life with you!\""}]
    + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
)

story = str(completion["choices"][0].message["content"])
previousChapter = str(completion["choices"][0].message["content"])

postprompt = "Take the following chapter and make the next chapter:\n" 

for i in range(1, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2700,
    messages = 
        [{"role": "system", "content": "You are a story teller continuing a story."}] 
        + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[i])}]
        + [{"role": "assistant", "content": "The current chapter is " + str(i)}] 
        + [{"role": "assistant", "content": "Rory travels to a perilous cave to prove his love!"}]
        + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
        + [{"role": "assistant", "content": "In a statement like (travel rory village cave), the meaning is: 'Rory travels from the village to the cave' ."}]
    )
    previousChapter = str(completion["choices"][0].message["content"])
    story += "\n Part: " + str(i) + "\n" + str(completion["choices"][0].message["content"])

postprompt = "Finish the story off based off of the following previous chapter:\n"

completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are a story teller ending a story."}] 
    + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[count-1])}]
    + [{"role": "assistant", "content": "The final chapter is " + str(count)}] 
    + [{"role": "assistant", "content": "After his ardurous journey, Rory returns home and marries Talia."}]
    + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
)

previousChapter = str(completion["choices"][0].message["content"])
story += "\n Part: " + str(i) + "\n" + str(completion["choices"][0].message["content"])




output = open("story.txt", "w")
stroutput = story
output.write(stroutput)
output.close()

print(completion["choices"][0].message["content"])
# print(completion["choices"][0].message["content"], file=output)
# print(completion.choices[0].message)
