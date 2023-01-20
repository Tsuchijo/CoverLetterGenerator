from dotenv import load_dotenv
load_dotenv()

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

resume_path = "skills/resume"
description_path = "description/job_desc"
prompt_path = "prompt"
description = open(description_path, "r")
prompt = open(prompt_path, "r")

def generate_prompt():
    if(not os.path.exists("skills/summary")):
        format_resume()
    summary = open("skills/summary", "r")

    return prompt.readline() + summary.read() + prompt.readline() + description.read()

def generate_letter():
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(),
        temperature=0.9,
        max_tokens=1800
    ).choices[0].text

def format_resume():
    summary = open("skills/summary", "w")
    resume = open("skills/resume", "r")
    summary_text = openai.Completion.create(
            model="text-davinci-003",
            prompt= "format this resume to be easier to read and remove extraneous information" + resume.read(),
            temperature=0.7,
            max_tokens=1200,
    ).choices[0].text
    summary.write(summary_text)

def read_input():
    letter = generate_letter()
    print(letter)
    while True:
        response = input(":")
        if response == 'quit':
            break
        letter = openai.Completion.create(
            model="text-davinci-003",
            prompt= "rewrite thise cover letter taking into account this feedback"+ response + '\n' + letter,
            temperature=0.7,
            max_tokens=1200,
        ).choices[0].text
        print(letter)

read_input()

