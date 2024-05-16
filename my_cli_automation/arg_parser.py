import argparse

# Define a list of models that can be reused elsewhere
models_available = [
    'gpt-3.5-turbo-instruct',  # Considered the 'weakest' model
    'gpt-3.5-turbo',
    'gpt-4o',
    'gpt-4-turbo',
    'gpt-4'
]

# Create a mapping of numbers to models
model_mapping = {str(index): model for index, model in enumerate(models_available)}

def parse_args():
    parser = argparse.ArgumentParser(description="Process file and directory paths.")
    parser.add_argument('-f', '--files', nargs='+', help='List of file paths', default=[])
    parser.add_argument('-d', '--dir', help='Directory path', default='.')
    parser.add_argument('-i', '--init', default='programming', help='Initial prompt key (default: programming)')
    parser.add_argument('-m', '--model', choices=list(model_mapping.keys()) + models_available, default='1', help='Language model to use (default: gpt-3.5-turbo-instruct)')

    args = parser.parse_args()
    # Map numerical input to corresponding model name
    args.model = model_mapping.get(args.model, args.model)
    return args