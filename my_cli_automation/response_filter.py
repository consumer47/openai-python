import os

# Define the base path for temporary files
temp_file_path = "./temp_files"

# Ensure the temp_file_path directory exists
os.makedirs(temp_file_path, exist_ok=True)

# Define filters for different types of code blocks or content
filters = {
    "python": {
        "start_string": "```python",
        "end_string": "```",
        "file_ending": ".py",
        "file_counter": 0
    }
    # You can add more filters for different languages or content types
}

def store_filtered_data(filtered_out_string: str, filter_type: str='python') -> str:
    # Increment the file counter to avoid conflicts
    filters[filter_type]["file_counter"] += 1
    file_counter = filters[filter_type]["file_counter"]
    
    # Create the file path with the appropriate file ending and counter
    file_path = os.path.join(temp_file_path, f"filtered_{file_counter}{filters[filter_type]['file_ending']}")
    
    # Store the filtered out string into the file
    with open(file_path, 'w') as file:
        file.write(filtered_out_string)
    
    # Return the file path for replacement
    replacement = f"File_path: {file_path}"
    return replacement

def filter_response(response: str, filter_type: str='python') -> str:
    # Extract the start and end strings for the filter type
    start_string = filters[filter_type]["start_string"]
    end_string = filters[filter_type]["end_string"]
    
    # Initialize an empty string to hold the filtered response
    filtered_response = ""
    
    # Split the response into parts based on the start string
    parts = response.split(start_string)
    for i, part in enumerate(parts):
        if i == 0:
            # The first part does not contain the filtered content
            filtered_response += part
        else:
            # The subsequent parts may contain the filtered content
            if end_string in part:
                # Split the part to separate the filtered content
                filtered_content, remainder = part.split(end_string, 1)
                # Store the filtered content in a file and get the file path
                file_path = store_filtered_data(filtered_content, filter_type)
                # Append the file path and the remainder of the response
                filtered_response += file_path + remainder
            else:
                # If there's no end string, append the part as is
                filtered_response += start_string + part

    return filtered_response.strip()  # Remove any leading/trailing whitespace

# TODO: Implement a cleanup function if needed
def cleanup_temp_files():
    # Remove all files in the temp_file_path directory
    for filename in os.listdir(temp_file_path):
        file_path = os.path.join(temp_file_path, filename)
        os.remove(file_path)