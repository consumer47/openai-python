#!/usr/bin/env -S poetry run python

import asyncio
import json
from openai import AsyncOpenAI
from ContextCreator import ContextCreator
from arg_parser import parse_args

class CliManager:
    def __init__(self, client, init_prompt, file_paths=None, dir_path=None):
        self.client = client
        self.init_prompt = init_prompt
        self.context_creator = ContextCreator()
        self.conversation_context = [f"GPT: {init_prompt}\n"]

        # Process files and directories if provided
        if file_paths:
            for file_path in file_paths:
                self.context_creator.add_file(file_path)
        if dir_path:
            self.context_creator.add_folder(dir_path)

        # Add file and directory contents to the conversation context
        file_dir_contents = self.context_creator.get_contents()
        if file_dir_contents:
            self.conversation_context.append(file_dir_contents)

    async def send_prompt(self, prompt):
        try:
            response = await self.client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=1000  # You can adjust max_tokens as needed
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def run(self):
        # Display the initial prompt
        print(f"Initial prompt: {self.init_prompt}")
        
        # Send the initial prompt to the model and get the response
        init_response = await self.send_prompt(self.init_prompt)
        self.conversation_context.append(f"You: {init_response}\n")
        print(init_response)
        
        # Start the CLI after displaying the initial prompt
        print("Starting the GPT-powered CLI. Type 'exit' to quit.")
        print("You can start by typing your query below:")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting the CLI.")
                break
            
            # Append the user input to the context
            self.conversation_context.append(f"You: {user_input}\n")
            
            # Join the context and send it to the model
            full_context = "\n".join(self.conversation_context[-4:])  # Keep only the last 4 exchanges
            response = await self.send_prompt(full_context)
            
            # Append the model's response to the context
            self.conversation_context.append(f"GPT: {response}\n")
            
            if response:
                print(f"GPT: {response}")

# gets API Key from environment variable OPENAI_API_KEY
client = AsyncOpenAI()

# Parse command-line arguments
args = parse_args()

# Load prompts from the JSON file
with open('prompts.json', 'r') as file:
    data = json.load(file)

# Find the initial prompt based on the argument passed
init_prompt_key = args.init
init_prompt = data["prompts"].get(init_prompt_key, "Prompt not found.")

# Create an instance of CLIManager with the initial prompt, files, and directory
cli_manager = CliManager(client, init_prompt, file_paths=args.files, dir_path=args.dir)

# Run the CLIManager
asyncio.run(cli_manager.run())