def parse_flashcards_to_anki(input_file, output_file):
    """
    Parses a text file of flashcards into a tab-separated format for Anki.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    anki_cards = []
    current_front = None

    for line in lines:
        line = line.strip()
        
        # Identify the Front of the card
        if line.startswith("Front:"):
            current_front = line[len("Front:"):].strip()
            
        # Identify the Back of the card, pair it, and save
        elif line.startswith("Back:") and current_front is not None:
            current_back = line[len("Back:"):].strip()
            anki_cards.append(f"{current_front}\t{current_back}")
            current_front = None  # Reset for the next card

    # Write the formatted cards to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for card in anki_cards:
            outfile.write(card + '\n')

    print(f"Successfully parsed {len(anki_cards)} flashcards and saved to {output_file}.")

# --- How to use ---
# 1. Save your raw flashcard text into a file named 'raw_flashcards.txt'
# 2. Run this script.
# 3. Import the resulting 'anki_deck.txt' file into Anki.

if __name__ == "__main__":
    # You can replace these filenames with your actual file paths
    INPUT_FILENAME = 'raw_flashcards.txt'
    OUTPUT_FILENAME = 'anki_deck.txt'
    
    # Note: To run this immediately on the provided text without saving to a file first, 
    # you can adapt the script to process a multiline string instead.
    try:
        parse_flashcards_to_anki(INPUT_FILENAME, OUTPUT_FILENAME)
    except FileNotFoundError:
        print(f"Error: Please ensure you have saved your text into '{INPUT_FILENAME}' in the same directory.")