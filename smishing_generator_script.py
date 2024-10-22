import argparse
from openai import OpenAI
import json
import random
import os

# Variables to control how the pipeline is run
ITERATIONS = 5  # Number of iterations message generation is run
MESSAGE_SIZE = 10  # Number of messages to generate at each iteration
SAMPLE_SIZE = 15  # Number of random examples to look at each iteration
SCHEMA_UPDATE_FREQUENCY = 10  # Number of iterations before schema is updated

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:2213/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Read the content of the text file, saving the messages as strings in the phishing_example_lines list
with open("./seed/phishtank_samples.txt", "r") as file:
    phishing_example_lines = file.readlines()

with open("./seed/methods.json", "r") as file:
    methods_json = file.read()

with open("./seed/techniques.json", "r") as file:
    techniques_json = file.read()


def create_json_schema():
    # if exsiting json schema file exists
    if os.path.exists("defualt_schema.json"):
        # Open the JSON file and load its content
        with open('default_schema.json', 'r') as json_file:
            json_schema = json.load(json_file)
            json_string = json.dumps(json_schema)
            return json_string

    # Use the files to create a json schema 
    chat_response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'''I want you to create a json schema that describes a given sms phishing message. 
        Do not add unnecessary fields in the schema. Add fields for the message itself, the method used, and the persuasion technique used. 
        I want you to reply with the schema as a JSON and nothing else. \n
        Here are the phishing techniques: {techniques_json}.\n
        Here are the methods that could be used for persuasion: {methods_json}. \n'''}
    ],
    temperature=0.7, 
    top_p=0.9
    )

    return chat_response.choices[0].message.content


# Updates the methods json string
def update_methods_json():
    chat_response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'''I will provide you with a JSON string that contains the sms phishing methods.
        Your job is to return a JSON string with the same schema, only with more elements in the JSON array. Return only the JSON. Here is the JSON: {methods_json}'''}
    ],
    temperature=0.7, 
    top_p=0.9
    )

    return chat_response.choices[0].message.content


# Updates the techniques json
def update_techniques_json():
    chat_response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'''I will provide you with a JSON string that contains persuasion techniques for sms phishing.
        Your job is to return a JSON string with the same schema, only with more elements in the JSON array. Return only the JSON. Here is the JSON: {techniques_json}'''}
    ],
    temperature=0.7, 
    top_p=0.9
)

    return chat_response.choices[0].message.content


# Variables to control how the pipeline is run
ITERATIONS = 5  # Number of iterations message generation is run
MESSAGE_SIZE = 10  # Number of messages to generate at each iteration
SAMPLE_SIZE = 15  # Number of random examples to look at each iteration
SCHEMA_UPDATE_FREQUENCY = 10  # Number of iterations before schema is updated

# Entry point of the script
if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple argument parser example")

    # Add arguments
    parser.add_argument("--iterations", type=str, help="Number of iterations message generation is run",
                        default=5)
    parser.add_argument("--messages_num", type=int, help="Your age")
    parser.add_argument("--verbose", action="store_true", help="Increase output verbosity")


    # json_array to store all messages
    json_array = json.loads('[]')

    for i in range(ITERATIONS):
        # The examples to use in current iteration
        random_examples_list = random.sample(phishing_example_lines, SAMPLE_SIZE)
        smishing_examples = "\n".join(random_examples_list)

        # Get json schema
        json_schema = create_json_schema()
        
        # Uncomment and define update_json_schema if you need schema updates
        # if i % SCHEMA_UPDATE_FREQUENCY == 0:
        #     json_schema = update_json_schema(json_schema)

        chat_messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert data generator. Follow the user's instructions "
                    "precisely to create unique, original, and diverse JSON data."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Using the following JSON schema: {{json_schema}}, create 10 unique "
                    f"and original datapoints, outputting only a JSON array, with no other "
                    f"output. It is important it is in JSON format.\n\n"
                    f"Consider the patterns and structures shown in these examples: "
                    f"{{smishing_examples}}, but do not copy them directly. Instead, generate "
                    f"new datapoints that adhere to the schema but differ significantly in "
                    f"the details, such as names, numbers, or links, or any specific values.\n\n"
                    f"Ensure that each generated datapoint introduces unique elements and "
                    f"variations, while still following the underlying structure and intent "
                    f"of the given examples. Aim for creativity and diversity, avoiding "
                    f"repetition, and enhancing originality while maintaining validity "
                    f"according to the schema."
                )
            }
        ]

        # Use the variables selected above to make a call to the LLM API
        chat_response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=chat_messages,
            temperature=0.7,
            top_p=0.8
        )

        json_array += json.loads(chat_response.choices[0].message.content)


        if (i == ITERATIONS/2):
            techniques_json = update_techniques_json()
            methods_json = update_methods_json()
            print("Update methods and techniques json")
    
    # Save the data to a .json file
    with open('output.json', 'w') as json_file:
        json.dump(json_array, json_file, indent=4)
