#!/usr/bin/env -S poetry run python

import asyncio
import json

from openai import AsyncOpenAI

# gets API Key from environment variable OPENAI_API_KEY
client = AsyncOpenAI()

# Load prompts from the JSON file
with open('openai-python/my_cli_automation/prompts.json', 'r') as file:
    data = json.load(file)
    prompts_list = list(data["prompts"].items())

# Access the prompt by index, for example, index 1 for the second prompt
index = 1
active_prompt_key, active_prompt = prompts_list[index]

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