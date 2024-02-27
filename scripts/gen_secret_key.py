import secrets
import os

# Generate a secret key
secret_key = secrets.token_hex(16)

# Define the directory and filename where the secret key will be stored
directory = os.path.expanduser('~/.gptclient')  # Expand the user's home directory
filename = 'secret_key.txt'
full_path = os.path.join(directory, filename)

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Write the secret key to the file
with open(full_path, 'w') as file:
    file.write(secret_key)

# Print the path, normalized and with forward slashes
normalized_path = os.path.normpath(full_path).replace("\\", "/")
print(f'Your secret key has been written to {normalized_path}')

