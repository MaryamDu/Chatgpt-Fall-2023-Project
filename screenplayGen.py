import openai
import json
from fpdf import FPDF



file = open("Steps.txt")

content = file.readlines()
# countFile = content.split("\n")

prompt = []
setup = []

count = 0

# .length of the file (total number of the lines)
for i in content:
    if i:
        count += 1

lines = []
setup_lines = []

# make an array for 2 - .length-1
i = 2
while i != count:
    lines.append(i)
    i += 1

i = 0
while i <= 2:
    setup_lines.append(i)
    i+=1 

for pos, lineNum in enumerate(content):
    if pos in lines:
        prompt.append(lineNum)
        #print(prompt) 

for pos, lineNum in enumerate(content):
    if pos in setup_lines:
        setup.append(lineNum)
        #print(setup) 

file.close()

postprompt = "Write the first chapter of a story, including dialogue and natural progression, based on the following: " 

story = ""
previousChapter = ""
chapters = []

assistantPhrases = []

count = len(prompt)

#Set up the scene


#Make the assistant
#for i in range(0, count):
#    completion = openai.ChatCompletion.create(
#    model = "gpt-3.5-turbo",
#    temperature = 0.1, #degree of randomness between 0 and 2
#    max_tokens = 3000,
#    messages = 
#        [{"role": "system", "content": "You are rephrasing a string of words."}] 
#        + [{"role": "user", "content" : ("Take the following phrase and make it into a coherent and elaborate sentence: " + prompt[i] + " Provide only the resulting sentence.")}]
#        + [{"role": "assistant", "content": "In a statement like (accept talia rory village), the meaning is: 'Talia accepts Rory's proposal in the village' "}]
#    )
#    assistantPhrases.append(str(completion["choices"][0].message["content"]))

characterList = ""

completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are making a list of characters for a screenplay."}] 
    + [{"role": "user", "content" : "Make a list of character names for a screenplay, ranging from the protagonist, antagonist, mentor, and any other key chatacters."}]
    + [{"role": "assistant", "content": "The format should be similar to the following: John - main character."}]
    + [{"role": "assistant", "content": "The genre is " + setup[0]}]
)

characterList = str(completion["choices"][0].message["content"])


for i in range(0, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.1, #degree of randomness between 0 and 2
    max_tokens = 3000,
    messages = 
        [{"role": "system", "content": "You are elaborating on the steps of the Hero's Journey to turn it into steps in a screenplay."}] 
        + [{"role": "user", "content" : ("Take the following step of the Hero's Journey and elaborate on it by making it into the brief steps of a screenplay: " + prompt[i] + " Provide only the resulting elaboration.")}]
        + [{"role": "assistant", "content": "Use the following list of characters and their roles appropiately: " + characterList}]
    )
    assistantPhrases.append(str(completion["choices"][0].message["content"]))

#First Chapter
completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are beginning a screenplay"}] 
    + [{"role": "user", "content" : (postprompt + prompt[0])}]
    + [{"role": "assistant", "content": assistantPhrases[0]}]
    + [{"role": "assistant", "content": "The genre is " + setup[0]}]
)

story = str(completion["choices"][0].message["content"])
previousChapter = str(completion["choices"][0].message["content"])
chapters.append(previousChapter)

postprompt = "Take the following introduction and continue the screenplay, and include dialogue and natural progression:\n" 

#Chapters 2 - (End - 1)
for i in range(1, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are continuing a screenplay."}] 
        + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[i])}]
        #+ [{"role": "assistant", "content": "The current chapter is " + str(i)}] 
        + [{"role": "assistant", "content": assistantPhrases[i]}]
        + [{"role": "assistant", "content": "The genre is " + setup[0]}]
    )
    previousChapter = str(completion["choices"][0].message["content"])
    story += "\n" + str(completion["choices"][0].message["content"])
    chapters.append(previousChapter)

postprompt = "Finish the screnplay off based off of the following previous content and include dialogue if necessary to lead to a smooth ending:\n"

#Final Chapter
completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.2, #degree of randomness between 0 and 2
  max_tokens = 3000,
  messages = 
    [{"role": "system", "content": "You are ending a screenplay."}] 
    + [{"role": "user", "content" : (postprompt + previousChapter + " \nUtilize the following steps as a basis as well: " + prompt[count-1])}]
    #+ [{"role": "assistant", "content": "The final chapter is " + str(count)}] 
    + [{"role": "assistant", "content": assistantPhrases[count-1]}]
    + [{"role": "assistant", "content": "The genre is " + setup[0]}]
)

previousChapter = str(completion["choices"][0].message["content"])
story += "\n\n" + str(completion["choices"][0].message["content"])
chapters.append(previousChapter)

remadeStory = ""
summary = []

#Summarize
for i in range(0, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are summarizing a screenplay."}] 
        + [{"role": "user", "content" : ("Create a short summary of the following section of a screenplay: " + chapters[i])}]
        + [{"role": "assistant", "content" : "The summary should only be a few sentences long."}]
    )
    summary.append( str(completion["choices"][0].message["content"]))

remadeStory += chapters[0]

#Rewrite
for i in range(1, count):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are remaking a screenplay."}] 
        + [{"role": "user", "content" : ("Rewrite the following section of a screenplay: " + chapters[i])}]
        + [{"role": "assistant", "content": "Keep in mind that the previous chapter was this: " + summary[i-1]}]
    )
    remadeStory += "\n\n" + str(completion["choices"][0].message["content"])


#Character Identification
characters_CH = []
characters = ""

#Chapter by Chapter
for i in range(0, count-1):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are identifying important characters in a screenplay and identifying aspects that a reader should know."}] 
        + [{"role": "user", "content" : ("State the important characters of the following section and aspects about them that a reader should know: " + chapters[i])}]
        + [{"role": "assistant", "content": "Important characters are individuals with names, not groups of people."}]
    )
    characters_CH.append( str(completion["choices"][0].message["content"]))

#Story as a whole
completion = openai.ChatCompletion.create(
model = "gpt-3.5-turbo",
temperature = 0.2, #degree of randomness between 0 and 2
max_tokens = 2500,
messages = 
    [{"role": "system", "content": "You are identifying important characters in a screenplay and identifying aspects that a reader should know."}] 
    + [{"role": "user", "content" : ("State the important characters in this screenplay and aspects about them that a reader should know: " + remadeStory)}]
    + [{"role": "assistant", "content": "Important characters are individuals with names, not groups of people."}]
)
characters = ( str(completion["choices"][0].message["content"]))

characterRelations = ""

#Story relations
completion = openai.ChatCompletion.create(
model = "gpt-3.5-turbo",
temperature = 0.2, #degree of randomness between 0 and 2
max_tokens = 2500,
messages = 
    [{"role": "system", "content": "You are identifying important characters and their relationships to each other in a screenplay."}] 
    + [{"role": "user", "content" : ("State the important characters in this screenplay and their relationship to one another: " + remadeStory)}]
    + [{"role": "assistant", "content": "Exclude characters that aren't individuals, that is don't include groups of people or unnamed characters. "}]
)
characterRelations = ( str(completion["choices"][0].message["content"]))


characterStory = ""

#Rewrite
for i in range(0, count-1):
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are remaking a screenplay based on characters and their relationships to each other."}] 
        + [{"role": "user", "content" : ("Rewrite the following section: " + chapters[i] + "\nBased on the following characters featured in this chapter: " + characters_CH[i] + "\nProvide only the resulting section of the screenplay.")}]
        + [{"role": "assistant", "content": "Keep in mind that these are the characters seen throughout the screenplay: " + characters}]
        + [{"role": "assistant", "content": "Keep in mind that these are the relationships between the characters: " + characterRelations}]
    )
    characterStory += "\n\n" + str(completion["choices"][0].message["content"])

summary2 = ""
summary3 = ""

#Summarize the other remakes
completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are summarizing a screenplay."}] 
        + [{"role": "user", "content" : ("Create a detailed summary of the following screenplay: " + remadeStory)}]
        + [{"role": "assistant", "content" : "The summary should be long."}]
    )
summary2 = ( str(completion["choices"][0].message["content"]))


completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.2, #degree of randomness between 0 and 2
    max_tokens = 2500,
    messages = 
        [{"role": "system", "content": "You are summarizing a screenplay."}] 
        + [{"role": "user", "content" : ("Create a detailed summary of the following screenplay: " + characterStory)}]
        + [{"role": "assistant", "content" : "The summary should be long."}]
)
summary3 = ( str(completion["choices"][0].message["content"]))

characterStoryUpdate = ""

#Story relations after everything
completion = openai.ChatCompletion.create(
model = "gpt-3.5-turbo",
temperature = 0.2, #degree of randomness between 0 and 2
max_tokens = 2500,
messages = 
    [{"role": "system", "content": "You are identifying important characters and their relationships to each other in a screenplay."}] 
    + [{"role": "user", "content" : ("State the important characters in this screenplay and their relationship to one another: " + characterStory)}]
    + [{"role": "assistant", "content": "Important characters are individuals with names, not groups of people."}]
)
characterStoryUpdate = ( str(completion["choices"][0].message["content"]))




output = open("story.txt", "w")
stroutput = "Character List\n\n" + characterList + "\n\nAssistant Phrases\n\n" + str(assistantPhrases) + "\n\nSummary\n\n" + str(summary) + "\n\nChapter By Chapter Characters\n\n" + str(characters_CH) + "\n\nCharacters as a Whole\n\n" + characters + "\n\nCharacter Relationships\n\n" + characterRelations + "\n\nFirst Draft\n\n" + story + "\n\nRemade Story Summary\n\n" + summary2 + "\n\nRemade Story\n\n" + remadeStory + "\n\nCharacter Remade Story Summary\n\n" + summary3 + "\n\nCharacters Rehash\n\n" + characterStoryUpdate + "\n\nRemade Story with Characters\n\n" + characterStory 
output.write(stroutput)
output.close()


#print(str(assistantPhrases) + "\nSummary" + str(summary) + "\nChapter By Chapter Characters" + str(characters_CH) + "\nCharacters as a Whole" + characters)
# print(completion["choices"][0].message["content"], file=output)
# print(completion.choices[0].message)
