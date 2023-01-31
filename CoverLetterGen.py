from dotenv import load_dotenv
load_dotenv()

import os
import openai
from Loader import Loader

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_path = "prompt"
prompt = open(prompt_path, "r")
resume_path = "resume/resume.txt"
output_path = "output/"

## Function to clear terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

## Function to read multiple lines from user
# @param statement: statement to print before reading
def multi_read(statement):
    print(statement + "(Ctrl-D or Ctrl-Z ( windows ) to save)")
    lines = ""
    while True:
        try:
            line = input()
        except EOFError:
            return lines
        lines = lines + (line)

## Function to generate prompt for cover letter
# @param description: job description to use as prompt
def generate_prompt(description):
    #check if resume exists
    # if not, prompt user to input one
    if(not os.path.exists(resume_path)):
        print("no resume detected, add a resume to the resume folder or input text!")
        format_resume(multi_read("input resume text:"))
    resume = open(resume_path, "r")
    return prompt.readline() + resume.read() + prompt.readline() + description

## Function to generate cover letter
# @param description: job description to use as prompt
def generate_letter(description):
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(description),
        temperature=0.9,
        max_tokens=1800
    )

## Formats and saves the resume to the resume folder
# @param resume: resume text to format
def format_resume(resume):
    summary = open(resume_path, "w")
    summary.write(resume)

def save_file(file_name, text):
    with open(output_path + file_name + '.txt', 'w') as f:
        f.write(text)

## Function to read input from user and edit letter
# @param description: job description to use as prompt
def read_input(description):
    #start generating cover letter
    loader = Loader("Generating Cover Letter...", "Finished", 0.05).start()
    letter = generate_letter(description)
    loader.stop()
    clear()
    #print letter
    print(letter.choices[0].text)

    ## loop reading user input to edit letter
    #quit to exit
    #all other input is used to edit letter as queries to OpenAI
    #@TODO: add more options
    #      render, save, etc
    while True:
        saved = False
        response = input(":")
        if response == 'quit':
            #check if they have saved before quitting
            if(not saved):
                if(input("save before quitting? (y/n)") == 'y'):
                    save_name = input("save as:")
                    save_file(save_name, letter.choices[0].text)
            print('quitting...')
            exit(1)
        if response == 'save':
            print('saving...')
            #ask for file name
            save_name = input("save as:")
            save_file(save_name, letter.choices[0].text)
            print('saved!')
            saved = True
        else:
            loader = Loader("Editing...", "Finished", 0.05).start()
            letter = openai.Edit.create(
                model="text-davinci-edit-001",
                input= letter.choices[0].text,
                instructions= response,
                temperature=0.7,
                max_tokens= letter.usage.completion_tokens + 100, 
            ).choices[0].text
            loader.stop()            
            clear()
            print(letter)

def main():
    clear()
    #prompts user to input job description 
    desc_text = multi_read("input job description:")
    clear()
    read_input(desc_text)

if __name__ == "__main__":
    main()
