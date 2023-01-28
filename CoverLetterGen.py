from dotenv import load_dotenv
load_dotenv()

import os
import openai
from Loader import Loader

openai.api_key = os.getenv("OPENAI_API_KEY")

description_path = "description/job_desc"
prompt_path = "prompt"
prompt = open(prompt_path, "r")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Function to read multiple lines from user
def multi_read(statement):
    print(statement + "(Ctrl-D or Ctrl-Z ( windows ) to save)")
    lines = ""
    while True:
        try:
            line = input()
        except EOFError:
            return lines
        lines = lines + (line)

def generate_prompt():
    if(not os.path.exists("skills/summary")):
        print("no resume given!")
        format_resume(input("input resume text:"))
    description = open(description_path, "r").read()
    summary = open("skills/summary", "r")

    return prompt.readline() + summary.read() + prompt.readline() + description

def generate_letter():
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(),
        temperature=0.9,
        max_tokens=1800
    )

def format_resume(resume):
    summary = open("skills/summary", "w")
    loader = Loader("Saving resume...", "Finished", 0.05).start()
    summary_text = openai.Completion.create(
            model="text-davinci-003",
            prompt= "format this resume to be easier to read and remove extraneous information: " + resume,
            temperature=0.7,
            max_tokens=1200,
    ).choices[0].text
    loader.stop()
    summary.write(summary_text)

def read_input():
    loader = Loader("Generating Cover Letter...", "Finished", 0.05).start()
    letter = generate_letter()
    loader.stop()
    clear()
    print(letter.choices[0].text)
    while True:
        response = input(":")
        if response == 'quit':
            print('quitting...')
            exit(1)
        else:
            loader = Loader("Editing...", "Finished", 0.05).start()
            letter = openai.Completion.create(
                model="text-davinci-003",
                prompt= "rewrite these cover letter taking into account this feedback, then repeat the complete copy: "+ response + '\n' + letter.choices[0].text,
                temperature=0.7,
                max_tokens= letter.usage.completion_tokens + 100 + (int)(len(response) / 6),
            ).choices[0].text
            loader.stop()            
            clear()
            print(letter)

def main():
    clear()
    response = input("New Resume (y/N):")
    clear()
    if(response == 'y'):
        resume_text = multi_read("input resume text: ")
        format_resume(resume_text)
    clear()
    desc_text = multi_read("input job description:")
    open(description_path, "w").write(desc_text)
    clear()
    read_input()

if __name__ == "__main__":
    main()
