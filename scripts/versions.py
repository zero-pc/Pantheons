import json
import os
import re

# Read JSON data from the input file
def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    
def escape_markdown_special_chars(text):
    """Escape markdown special characters in the given text."""
    # Define special characters to escape in markdown
    special_chars = r"([\\`*_{}[\]()#+-.!|])"
    return re.sub(special_chars, r"\\\1", text)

# Convert JSON data to Markdown table format
def json_to_markdown(data, order):
    # Table header
    markdown = "## Mod List \n\n"
    markdown += "| Mod Name                      | Required Version | Status |\n"
    markdown += "|-------------------------------|------------------|--------|\n"

    # Table rows based on the order
    for mod_path in order["enabled_mods"]:
        print(mod_path)
        # Find the mod data by matching the gameRegistryId
        mod_data = next((mod for mod in data.values() if mod.get("gameRegistryId") == mod_path), None)
        if mod_data:
            name = mod_data.get("displayName", "N/A")
            required_version = mod_data.get("requiredVersion", "N/A")
            required_version = escape_markdown_special_chars(required_version)
            markdown += f"| {name:<30} | {required_version:<16} | |\n"

    return markdown

# Write the Markdown table to the output file
def write_markdown(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)

# Main function
def main():

    ck3_directory = r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III"
    ck3_directory = os.path.expanduser(ck3_directory)

    # Directory where the CK3 mod files are located
    mod_directory = r"~\DOCUMENTS\PARADOX INTERACTIVE\CRUSADER KINGS III\MOD\Pantheons"
    mod_directory = os.path.expanduser(mod_directory)  

    # Input and output file paths
    data_file = ck3_directory+"\mods_registry.json"  # Input file containing JSON data
    order_file = ck3_directory+"\dlc_load.json"  # Input file containing JSON data
    output_file = mod_directory+"\docs\mods_table.md"  # Output file containing the markdown table

    data = read_json(data_file)
    order = read_json(order_file)
    markdown_table = json_to_markdown(data,order)

    # Write the Markdown table to the output file
    write_markdown(output_file, markdown_table)
    print(f"Markdown table saved to {output_file}")

if __name__ == "__main__":
    main()
