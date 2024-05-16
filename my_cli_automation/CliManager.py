#!/usr/bin/env -S poetry run python
import os
import json
import asyncio      
from typing import List, Optional
from openai import AsyncOpenAI
from ContextCreator import ContextCreator
from arg_parser import parse_args

class CliManager:
    def __init__(
        self,
        client: AsyncOpenAI,
        init_prompt: str,
        model: str,
        file_paths: Optional[List[str]] = None,
        dir_path: Optional[str] = None
    ) -> None:
        self.client: AsyncOpenAI = client
        self.init_prompt: str = init_prompt
        self.model: str = model
        self.context_creator: ContextCreator = ContextCreator()
        self.conversation_context: List[str] = [f"You: {init_prompt}\n"]

        # Process files and directories if provided
        if file_paths:
            for file_path in file_paths:
                self.context_creator.add_file(file_path)
        if dir_path:
            self.context_creator.add_folder(dir_path)

        # Add file and directory contents to the conversation context
        file_dir_contents: str = self.context_creator.get_contents()
        if file_dir_contents:
            self.conversation_context.append(file_dir_contents)

    async def send_prompt(self, context: List[str], context_len: int=4) -> Optional[str]:
        prompt = "\n".join(context[-context_len:]) 
        
        # Use the chat completions endpoint for all models
        response = await self.client.chat.completions.create(
            model=self.model,
            # prompt=prompt,
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            #  stream=True
        )
        return response.choices[0].message.content

    async def run(self) -> None:
        # Display the initial prompt
        print(f"Initial prompt: {self.init_prompt}")
        # Send the initial prompt to the model and get the response
        init_response: Optional[str] = await (self.send_prompt(self.conversation_context))
        if init_response:
            self.conversation_context.append(f"You: {init_response}\n")
            print(init_response)
        # Start the CLI after displaying the initial prompt
        print("Starting the GPT-powered CLI. Type 'exit' to quit.")
        print("You can start by typing your query below:")
        while True:
            user_input: str = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting the CLI.")
                break
            # Append the user input to the context
            self.conversation_context.append(f"You: {user_input}\n")
            response: Optional[str] = await self.send_prompt(self.conversation_context[-4:])
            # Append the model's response to the context
            if response:
                self.conversation_context.append(f"GPT: {response}\n")
                print(f"GPT: {response}")
                print("")

# gets API Key from environment variable OPENAI_API_KEY
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Parse command-line arguments
args = parse_args()

# Load prompts from the JSON file
with open('prompts.json', 'r') as file:
    data: dict = json.load(file)

# Find the initial prompt based on the argument passed
init_prompt_key: str = args.init
init_prompt: str = data["prompts"].get(init_prompt_key, "Prompt not found.")

# Create an instance of CLIManager with the initial prompt, files, and directory
cli_manager = CliManager(client, init_prompt, model=args.model, file_paths=args.files, dir_path=args.dir)

# Run the CLIManager
asyncio.run(cli_manager.run())