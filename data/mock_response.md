Certainly! Below you'll find a Python script using the 'markdown' module to read a Markdown file and render it to HTML. In case you haven't already, you'll first need to install the 'markdown' module. You can do this through your terminal or command prompt using pip:

```
pip install markdown
```

Once you have the module installed, here's a script that accomplishes the task:

```python
import markdown
import sys

def markdown_to_html(markdown_filepath, html_output_path):
    """
    This function converts a markdown file to an HTML file.

    Parameters:
    markdown_filepath (str): The path to the markdown file.
    html_output_path (str): The path where the HTML file will be saved.
    """

    # Attempt to read the Markdown file
    try:
        with open(markdown_filepath, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
    except FileNotFoundError:
        print(f"The markdown file at {markdown_filepath} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the markdown file: {e}")
        sys.exit(1)
    
    # Convert markdown content to HTML
    html_content = markdown.markdown(md_content)

    # Attempt to write the HTML content to a file
    try:
        with open(html_output_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        print(f"HTML file has been created at: {html_output_path}")
    except Exception as e:
        print(f"An error occurred while writing the HTML file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Check if the script was called with the required arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_markdown_file.md> <output_html_file.html>")
        sys.exit(1)

    input_markdown_file = sys.argv[1]
    output_html_file = sys.argv[2]
    
    markdown_to_html(input_markdown_file, output_html_file)
```
This script takes in two arguments: the path to the input Markdown file and the path where you want the resulting HTML file to be saved. To run the script, you'd use a command like the following in your terminal or command prompt:

```
python script.py example.md output.html
```

Replace 'script.py' with whatever you name the provided script file, 'example.md' with the path to your Markdown file, and 'output.html' with your desired output HTML file path. The script will read the Markdown content from the specified file, convert it to HTML using the 'markdown' library, and then write that HTML content to the designated output file.