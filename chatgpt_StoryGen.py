import openai
import json
from fpdf import FPDF



file = open("western-solution.pddl")

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

#count *= 2

postprompt = "Write the first chapter of a story, including dialogue and natural progression, based on the following: " 

story = ""
previousChapter = ""

assistantPhrases = []

count = len(prompt)

#Make the assistant
for i in range(0, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.1, #degree of randomness between 0 and 2
    max_tokens = 3000,
    messages = 
        [{"role": "system", "content": "You are rephrasing a string of words."}] 
        + [{"role": "user", "content" : ("Take the following phrase and make it into a coherent sentence: " + prompt[i] + " Provide only the resulting sentence.")}]
        + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
    )
    assistantPhrases.append(str(completion["choices"][0].message["content"]))


#First Chapter
completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are a story teller beginning a story."}] 
    + [{"role": "user", "content" : (postprompt + prompt[0])}]
    + [{"role": "assistant", "content": assistantPhrases[0]}]
)

story = str(completion["choices"][0].message["content"])
previousChapter = str(completion["choices"][0].message["content"])

postprompt = "Take the following chapter and make the next chapter, and include dialogue and natural progression:\n" 

#Chapters 2 - (End - 1)
for i in range(1, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2700,
    messages = 
        [{"role": "system", "content": "You are a story teller continuing a story."}] 
        + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[i])}]
        + [{"role": "assistant", "content": "The current chapter is " + str(i)}] 
        + [{"role": "assistant", "content": assistantPhrases[i]}]
    )
    previousChapter = str(completion["choices"][0].message["content"])
    story += "\n Part: " + str(i) + "\n" + str(completion["choices"][0].message["content"])

postprompt = "Finish the story off based off of the following previous chapter and include dialogue if necessary to lead to a smooth ending:\n"

#Final Chapter
completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are a story teller ending a story."}] 
    + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[count-1])}]
    + [{"role": "assistant", "content": "The final chapter is " + str(count)}] 
    + [{"role": "assistant", "content": assistantPhrases[count-1]}]
)

previousChapter = str(completion["choices"][0].message["content"])
story += "\n\n" + str(completion["choices"][0].message["content"])




output = open("story.txt", "w")
stroutput = story
output.write(stroutput)
output.close()

pdf = FPDF()

pdf.add_page()
pdf.set_font("Arial", size = 15)
f = open("story.txt", "r")
for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
pdf.output("story.pdf")   



print(str(assistantPhrases) + "\n")
print(story)
# print(completion["choices"][0].message["content"], file=output)
# print(completion.choices[0].message)
