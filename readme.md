# README
A basic command line utility to generate cover letters using OpenAI's gpt 3 API. Has the ability to generate a simple cover letter based ona  given resume and job description, as well as basic ai based editing capabilities (more advanced editing option TBA).

# How to use (Linux)
1. Download the project with: ```git clone https://github.com/Tsuchijo/CoverLetterGenerator.git```
2. enter the directory with ```cd CoverLetterGenerator``` then create a file named ```.env```
3. Sign into your OpenAI account then generate an API key: https://platform.openai.com/account/api-keys
4. In the ```.env``` file paste in ```OPENAI_API_KEY=<OpenAI api key>```, inputting your OpenAI API key where the brackets are (without the brackets)
5. Activate the environment by running the comman ```source envAI/bin/activate```
6. Go to the resume directory with ```cd resume``` and create a text file named ```resume.txt``` with the plain text version of your resume
7. Finally, run the python script with ```python CoverLetterGen.py```
