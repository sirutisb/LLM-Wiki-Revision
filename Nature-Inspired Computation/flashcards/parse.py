import re

# File names
input_filename = "nic-flashcards.txt"
output_filename = "anki-import.txt"

def parse_flashcards(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split the text into individual card blocks based on double line breaks
        cards = content.strip().split('\n\n')
        processed_count = 0

        with open(output_file, 'w', encoding='utf-8') as f:
            for card in cards:
                # Use regex to isolate the Front and Back text
                match = re.match(r"Front:\s*(.*?)\nBack:\s*(.*)", card, re.DOTALL)
                if match:
                    front = match.group(1).strip()
                    back = match.group(2).strip()
                    
                    # Replace actual line breaks in the Back section with Anki-friendly <br> tags
                    back = back.replace('\n', '<br>')
                    
                    # Write to the new file separated by a tab
                    f.write(f"{front}\t{back}\n")
                    processed_count += 1

        print(f"Success! Parsed {processed_count} flashcards and saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Could not find the file named '{input_file}'. Please make sure it's in the same directory as this script.")

if __name__ == "__main__":
    parse_flashcards(input_filename, output_filename)