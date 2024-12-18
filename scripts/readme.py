import os

def merge_markdown_files(input_folder, output_file):
    # Get a list of all .md files in the folder
    markdown_files = [f for f in os.listdir(input_folder) if f.endswith(".md")]
    
    # Ensure README.md is the first file
    if "README.md" in markdown_files:
        markdown_files.remove("README.md")
        markdown_files.insert(0, "README.md")

    # Open the output file for writing
    with open(output_file, "w") as output:
        for md_file in markdown_files:
            file_path = os.path.join(input_folder, md_file)

            # Read and write the content of the file
            with open(file_path, "r") as input_file:
                content = input_file.read()
                output.write(content)
                output.write("\n\n---\n\n")  # Divider between files

    print(f"Merged {len(markdown_files)} markdown files into {output_file}")



# Main function
def main():
    # Directory where the CK3 mod files are located
    mod_directory = r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III\MOD\Pantheons"
    mod_directory = os.path.expanduser(mod_directory) 

    # Directory containing the .md files
    docs_folder = mod_directory+"\docs"
    output_file = mod_directory+"\README.md"

    merge_markdown_files(docs_folder, output_file)

if __name__ == "__main__":
    main()
