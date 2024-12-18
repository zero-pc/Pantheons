import os
import re
import argparse

def delete_files_except_gitkeep(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip if the file is .gitkeep
        if filename == ".gitkeep":
            continue
        
        # Check if it's a file and delete it
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        # Optionally, handle directories (e.g., delete or skip)
        elif os.path.isdir(file_path):
            print(f"Skipped directory: {file_path}")

# Function to extract block
def extract_info(key, content):
    start_index = content.find(key + "={")
    if start_index == -1:
        print("none")
        return None

    brace_count = 0
    end_index = start_index + len(key) + 1
    while end_index < len(content):
        if content[end_index] == '{':
            brace_count += 1
        elif content[end_index] == '}':
            brace_count -= 1
        if brace_count == 0:
            break
        end_index += 1

    return content[start_index:end_index + 1] if brace_count == 0 else None

# Function to clean unwanted content
def clean_content(content):
    # Define regex patterns to clean
    patterns = [
        r'portrait_modifier_overrides\s*=\s*{[^}]*\s*}',  # remove override block
        r'override=\s*{[^}]*\s*}',  # remove override block
        r'id=[^\n]*',  # remove 'id' field
        r'random_seed=[^\n]*',  # remove 'random_seed' field
        r'entity=[^\n]*'  # remove 'entity' field
    ]

    # Ensure portrait_info section starts with "enabled=yes"
    content = re.sub(r'portrait_info={', "\n		enabled=yes\n		portrait_info={", content, flags=re.DOTALL)
    
    # Apply all regex patterns to clean the content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content

# Process files in the source folder
def process_source_files(source_folder,target_folder):
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)

        if os.path.isfile(source_file_path):
            with open(source_file_path, 'r', encoding='utf-8') as file:
                source_content = file.read()

            # Extract the data section
            data = extract_info("portrait_info", source_content)
            if data:
                # Lowercase the filename and create the placeholder
                lowercase_filename = os.path.splitext(filename)[0].lower()
                content = f"\n{lowercase_filename} = {{ {data} }}\n\n"

                # Write to the target folder
                target_file_path = os.path.join(target_folder, lowercase_filename)
                with open(target_file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

# Clean files in the target folder
def clean_target_files(target_folder):
    for filename in os.listdir(target_folder):
        target_file_path = os.path.join(target_folder, filename)
        
        if os.path.isfile(target_file_path):
            with open(target_file_path, 'r') as file:
                content = file.read()

            # Clean the content
            cleaned_content = clean_content(content)

            # Write the cleaned content back
            with open(target_file_path, 'w') as cleaned_file:
                cleaned_file.write(cleaned_content)

# Combine files into a single output file
def combine_files(input_folder, output_folder, output_filename):
    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, output_filename)
    with open(output_file_path, 'w+') as output_file:
        for filename in sorted(os.listdir(input_folder)):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as input_file:
                    content = input_file.read()
                    output_file.write(content)

    print(f"All files combined into: {output_file_path}")


# Main Processing Logic
def main():
    # Source and target paths
    source_folder = os.path.expanduser(r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III\Rulers")
    target_folder = os.path.expanduser(r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III\mod\Pantheons\build\dna_data")
    final_folder = os.path.expanduser(r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III\mod\Pantheons\common\dna_data")

    # Argument parser to take folder path as input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder_path", 
        type=str, 
        help="The path to the folder where where the gods files are"
    )
    # Parse the arguments
    args = parser.parse_args()

    if not args.folder_path:
        exit(0)

    source_folder += "\\"+args.folder_path
    target_folder += "\\"+args.folder_path

    delete_files_except_gitkeep(target_folder)
    # Execute the functions
    process_source_files(source_folder,target_folder)  # Extracts and writes to target folder
    clean_target_files(target_folder)  # Cleans the content in target files

    # Combine the cleaned files into the final output file
    output_filename = f"characters_{args.folder_path}_dna.txt"
    combine_files(target_folder, final_folder, output_filename)


# Run the main function
if __name__ == "__main__":
    main()