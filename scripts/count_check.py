import os
import argparse
import re

# Function to count occurrences of 'XXXX = {' outside the main body
def count_pattern_outside_blocks(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()

        # Count the matches outside of nested blocks
        count = 0
        brace_count = 0
        lines = content.splitlines()

        for line in lines:
            line = line.strip()

            # Ignore lines inside blocks
            if brace_count > 0:
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                continue

            # Count occurrences of 'XXXX = {' if outside blocks
            if re.match(r"\b[\w-]+\s*=\s*{", line):
                print(line)
                count += 1

            # Track whether we're inside a block
            if '{' in line:
                brace_count += line.count('{')
            if '}' in line:
                brace_count -= line.count('}')

        return count

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main Processing Logic
def main():
    # Source and target paths
    source_file = os.path.expanduser(r"~\Documents\Paradox Interactive\Crusader Kings III\mod\Pantheons")

    # Argument parser to take folder path as input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", 
        type=str, 
        help="The path to the file"
    )
    # Parse the arguments
    args = parser.parse_args()

    if not args.path:
        exit(0)

    source_file += "\\"+args.path

    print(f"The total count was: {count_pattern_outside_blocks(source_file)}")

if __name__ == "__main__":
    main()
