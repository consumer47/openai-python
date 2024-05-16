#!/usr/bin/env -S poetry run python

import asyncio
import json

from openai import AsyncOpenAI

# gets API Key from environment variable OPENAI_API_KEY
client = AsyncOpenAI()

# Load prompts from the JSON file
with open('openai-python/examples/prompts.json', 'r') as file:
    data = json.load(file)
    prompts_list = list(data["prompts"].items())

# Access the prompt by index, for example, index 1 for the second prompt
index = 1
active_prompt_key, active_prompt = prompts_list[index]

async def main() -> None:
    try:
        stream = await client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=active_prompt, 
            stream=True,
            max_tokens=1000  # You can adjust max_tokens as needed
        )

        # Explicitly consume the stream
        async for completion in stream:
            print(completion.choices[0].text, end="")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nStream ended.")

# Run the main function until it is finished
asyncio.run(main())
