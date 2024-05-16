#!/usr/bin/env -S poetry run python

import asyncio
import json
from openai import AsyncOpenAI
from ContextCreator import ContextCreator
from arg_parser import parse_args

# gets API Key from environment variable OPENAI_API_KEY
client = AsyncOpenAI()

# Parse command-line arguments
args = parse_args()

# Create a ContextCreator instance
context_creator = ContextCreator()

# If files or directories are provided, read them into the context
if args.files:
    for file_path in args.files:
        context_creator.add_file(file_path)

if args.dir:
    context_creator.add_folder(args.dir)

# Load prompts from the JSON file
with open('prompts.json', 'r') as file:
    data = json.load(file)
    prompts_list = list(data["prompts"].items())

# Find the initial prompt based on the argument passed
init_prompt_key = args.init
init_prompt = data["prompts"].get(init_prompt_key, "Prompt not found.")

async def send_prompt(prompt):
    try:
        response = await client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1000  # You can adjust max_tokens as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def main() -> None:
    # Display the initial prompt
    print(f"Initial prompt: {init_prompt}")
    
    # Start the CLI after displaying the initial prompt
    print("Starting the GPT-powered CLI. Type 'exit' to quit.")
    print("You can start by typing your query below:")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting the CLI.")
            break
        
        response = await send_prompt(user_input)
        if response:
            print(f"GPT: {response}")

# Run the main function until it is finished
asyncio.run(main())