import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = f"{dir_path}/data/transcripts.txt"
fileObject = open(data_path, "r")
text = fileObject.read()
convos = text.split("\n\n\n\n")

prompt_seq = ["Summarize this text message conversation between BOT and USER:",
              "Convert this text from third to first person:",
              "Convert from first person to second person:"]

res_dict = {}

for i, convo in enumerate(convos):
    data = convo
    res_dict[i] = {"data": data}
    print(f"------------ Convo Number #{i+1} ------------")
    for j, prompt in enumerate(prompt_seq):
        response = openai.Completion.create(model="text-davinci-002",
                                            prompt=f"{prompt}\n\n{data}",
                                            temperature=0.7,
                                            max_tokens=256,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0)
        
        data = response.choices[0].text.replace('\n', '')
        res_dict[i][j] = {}
        res_dict[i][j]["prompt"] = prompt
        res_dict[i][j]["result"] = data
        print(f"{prompt}")
        print(f"{data}")
        
# Directly from dictionary
with open('json_data.json', 'w') as outfile:
    json.dump(res_dict, outfile)