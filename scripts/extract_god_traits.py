import os
import re
import argparse

# Parentage mapping for characters

extra_fields={}
parentage={}

parentage["Greek_gods"] = {
    "amphitrite": {"mother": "gaia", "father": "uranus"},
    "aphrodite": {"mother": "none", "father": "zeus"},
    "apollo": {"mother": "leto", "father": "zeus"},
    "ares": {"mother": "hera", "father": "zeus"},
    "artemis": {"mother": "leto", "father": "zeus"},
    "athena": {"mother": "metis", "father": "zeus"},
    "cronus": {"mother": "gaia", "father": "uranus"},
    "demeter": {"mother": "rhea", "father": "cronus"},
    "gaia": {"mother": "none", "father": "none"},
    "hades": {"mother": "rhea", "father": "cronus"},
    "hephaestus": {"mother": "hera", "father": "none"},
    "hera": {"mother": "rhea", "father": "cronus"},
    "hermes": {"mother": "maia", "father": "zeus"},
    "persephone": {"mother": "demeter", "father": "zeus"},
    "poseidon": {"mother": "rhea", "father": "cronus"},
    "uranus": {"mother": "none", "father": "none"},
    "zeus": {"mother": "rhea", "father": "cronus"}
} 
extra_fields["Greek_gods"] = (
                f"\n\tdynasty=greek_gods_dynasty"
                f"\n\tdynasty_house=greek_gods_dynasty"
                f"\n\tculture=\"greek\""
                f"\n\treligion=\"hellenic_pagan\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            )

parentage["Egypt_gods"] = {
    "ra": {"mother": "none", "father": "none"},
    "neith": {"mother": "none", "father": "none"},
    "osiris": {"mother": "nut", "father": "geb"},
    "isis": {"mother": "nut", "father": "geb"},
    "set": {"mother": "nut", "father": "geb"},
    "nephthys": {"mother": "nut", "father": "geb"},
    "horus": {"mother": "isis", "father": "osiris"},
    "anubis": {"mother": "nephthys", "father": "set"},
    "geb": {"mother": "shu", "father": "tefnut"},
    "nut": {"mother": "shu", "father": "tefnut"},
    "shu": {"mother": "none", "father": "ra"},
    "tefnut": {"mother": "none", "father": "ra"},
    "bastet": {"mother": "isis", "father": "ra"},
    "sekhmet": {"mother": "none", "father": "ra"},
    "thoth": {"mother": "none", "father": "none"},
    "sobek": {"mother": "neith", "father": "set"},
    "maat": {"mother": "hathor", "father": "ra"},
    "hathor": {"mother": "none", "father": "ra"},
    "amun": {"mother": "none", "father": "none"},
    "mut": {"mother": "none", "father": "none"},
    "khonsu": {"mother": "mut", "father": "amun"}
}
extra_fields["Egypt_gods"] = (
                f"\n\tdynasty=egypt_gods_dynasty"
                f"\n\tdynasty_house=egypt_gods_dynasty"
                f"\n\tculture=\"egyptian\""
                f"\n\treligion=\"kushitism_pagan\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            ) 

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


# Function to extract block content by key
def extract_info(key, content):
    start_index = content.find(f"{key}={{")
    if start_index == -1:
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

    return content[start_index + len(key) + 1:end_index] if brace_count == 0 else None

# Method to replace multiple tabs with a single tab
def replace_multiple_tabs_with_one(content):
   # Step 1: Replace spaces with tabs
    content = content.replace(' ', '\t')
    # Step 2: Replace multiple consecutive tabs with a single tab
    cleaned_content = re.sub(r'\t+', '\t', content)
    return cleaned_content

# Function to process skills and traits in the content
def process_skills(match):
    skills = list(map(int, match.group(1).split()))
    skill_names = ["diplomacy", "martial", "stewardship", "intrigue", "learning", "prowess"]
    return "\n	".join(f"{name}={value}" for name, value in zip(skill_names, skills))

def process_traits(match):
    traits = match.group(1).split()
    return "\n	".join(f"trait={trait}" for trait in sorted(traits))

# Function to clean unwanted content
def clean_content(content):
    # Define regex patterns to clean
    patterns = [
        r'culture=[^\n]*',  # remove override block
        r'faith=[^\n]*',  # remove override block
    ]
    # Apply all regex patterns to clean the content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content

# Function to add additional fields to blocks (e.g., DNA, culture, faith)
def add_stuff_blocks(content, stuff):
    block_pattern = r"(\w+)\s*=\s*\{([\s\S]*?)}"
    def add_stuff_field(match):
        block_name = match.group(1)
        block_content = match.group(2).strip()
        return f"{block_name} = {{\n	{stuff}={block_name}\n      {block_content}\n}}"
    return re.sub(block_pattern, add_stuff_field, content)

# Function to process a file, extracting skills, traits, and adding parentage fields
def process_file(input_file, output_file, parentage=None, add_fields=None,extra_fields=None):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(r"skill=\{([\s\d]+)\}", process_skills, content)
    content = re.sub(r"traits=\{([^\}]+)\}", process_traits, content)

    if add_fields:
        content = add_stuff_blocks(content, add_fields)

    if parentage:
        character_name = os.path.splitext(os.path.basename(input_file))[0]
        if character_name in parentage:
            new_fields = (
                f"\n\tmother={parentage[character_name]['mother']}"
                f"\n\tfather={parentage[character_name]['father']}"
            )
            new_fields+=extra_fields
            if not re.search(r"^\s*mother=", content, re.MULTILINE):
                content = re.sub(r"(\{)", rf"\1{new_fields}", content, count=1)


    content=replace_multiple_tabs_with_one(content)
    
    with open(output_file, 'w+', encoding='utf-8') as file:
        file.write(content)

# Function to combine multiple files into one
def combine_files(input_folder, output_folder, output_filename):
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, output_filename)

    with open(output_file_path, 'w+', encoding='utf-8') as output_file:
        for filename in sorted(os.listdir(input_folder)):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    output_file.write(input_file.read())

    print(f"All files combined into: {output_file_path}")

# Main Processing Logic
def main():
    # Folder paths
    source_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\Rulers")
    target_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\mod\\Pantheons\\build\\characters")
    final_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\mod\\Pantheons\\history\\characters")

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

    #clean build folder
    delete_files_except_gitkeep(target_folder)

    # Iterate through source files and process them
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        if os.path.isfile(source_file_path):
            with open(source_file_path, 'r', encoding='utf-8') as file:
                source_content = file.read()

            data = extract_info("config", source_content)
            dataover = extract_info("portrait_override", source_content)
            if data:
                lowercase_filename = os.path.splitext(filename)[0].lower()
                content = f"\n{lowercase_filename} = {data} portrait_override={dataover}\n}}"+"}"+"\n\n"

                with open(os.path.join(target_folder, lowercase_filename), 'w+', encoding='utf-8') as file:
                    file.write(content)

    # Clean target files and add parentage & dynasty
    for filename in os.listdir(target_folder):
        target_file_path = os.path.join(target_folder, filename)
        if os.path.isfile(target_file_path):
            with open(target_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            cleaned_content = clean_content(content)

            with open(target_file_path, 'w+', encoding='utf-8') as cleaned_file:
                cleaned_file.write(cleaned_content)

            process_file(target_file_path, target_file_path, parentage[str(args.folder_path)], "dna", extra_fields[str(args.folder_path)])

    # Combine files into the final output file
    combine_files(target_folder, final_folder, f"characters_{args.folder_path}.txt")

# Run the main function
if __name__ == "__main__":
    main()
