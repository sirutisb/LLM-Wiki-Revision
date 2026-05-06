import os

def convert_to_anki(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    cards = []
    current_front = []
    current_back = []
    state = None # 'front' or 'back'

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            clean_line = line.strip()
            
            if clean_line.startswith('Front:'):
                # If we were previously in 'back' state, save the completed card
                if current_front and current_back:
                    front_text = " ".join(current_front).replace('\t', ' ')
                    back_text = " ".join(current_back).replace('\t', ' ')
                    cards.append(f"{front_text}\t{back_text}")
                    current_front = []
                    current_back = []
                
                state = 'front'
                current_front.append(clean_line.replace('Front:', '', 1).strip())
            elif clean_line.startswith('Back:'):
                state = 'back'
                current_back.append(clean_line.replace('Back:', '', 1).strip())
            elif clean_line == "":
                continue
            else:
                # Handle potential multi-line content
                if state == 'front':
                    current_front.append(clean_line)
                elif state == 'back':
                    current_back.append(clean_line)

    # Add the final card
    if current_front and current_back:
        front_text = " ".join(current_front).replace('\t', ' ')
        back_text = " ".join(current_back).replace('\t', ' ')
        cards.append(f"{front_text}\t{back_text}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cards))
    
    print(f"Successfully converted {len(cards)} flashcards to {output_path}")

if __name__ == "__main__":
    convert_to_anki('flashcards/raw_flashcards.txt', 'flashcards/anki_flashcards.txt')
