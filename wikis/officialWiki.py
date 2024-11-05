import random
import gzip
from openai import OpenAI
import os

notherpage = "yes"
scale = -1
about = "nothing"
total_lines = 85608856

api_key = os.getenv("OPENAI_API_KEY")

# Load environment variables manually

def load_env_variables():
    with open('.env', 'r') as env_file:
        for line in env_file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"')

load_env_variables()

def get_random_wiki_url():
    line_number = random.randrange(0, total_lines)
    with gzip.open('/Users/chaappe/dev/quest2/chores/wikis.gz', 'rt') as file:
        for current_line_number, line in enumerate(file):
            if current_line_number >= line_number:
                if "https://" in line:
                    start_index = line.find("<link>") + len("<link>")
                    end_index = line.find("</link>")
                    url = line[start_index:end_index]
                    if not url.startswith("https://"):
                        start_index = line.find("<url>") + len("<url>")
                        end_index = line.find("</url>")
                        url = line[start_index:end_index]
                    return url

while notherpage == "yes":

     # Step thorugh the file untill you find the line number and it contains https:/
    if  scale == -1:  
        line = get_random_wiki_url()
        print("\n\n" + line + "\n\n")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    scale = int(scale)
    if scale >= 6:
        scale = str(scale)
        if about != "nothing":
        #talk to chat gpt and find a similer wiki ling, show it the line and ask it to find a similar one
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "give me a similar wiki link/url about" + about ,
                    }
                ],
                model="gpt-3.5-turbo",
            ) 
            # prints the response
            print(chat_completion.choices[0].message.content)
    
    #if the scale is lower then 5 get a random page
        scale = int(scale)
        #between 0 and 5
    if 0 <= scale <= 5:
        line = get_random_wiki_url()
        print("\n\n" + line + "\n\n")
                
    # Then ask if I want to see another page
    scale = input("How much did you like the page? (1-10)")
    notherpage = input("Do you want to see another page? (yes/no)")
    about = input("what was it about?")

    if notherpage == "no":
        break