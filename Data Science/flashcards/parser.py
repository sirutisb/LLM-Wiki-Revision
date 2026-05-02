import re

# Read your source file
with open('data-science-at-scale.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all Front/Back pairs using regex
# This ignores the "SECTION" headers and "===" dividers
matches = re.findall(r'Front:\s*(.*?)\nBack:\s*(.*?)(?=\n---|\Z)', content, re.DOTALL)

# Write to a new tab-separated text file
with open('anki_ready.txt', 'w', encoding='utf-8') as f:
    for front, back in matches:
        # Clean up any stray newlines and separate the front and back with a tab
        front_clean = front.replace('\n', ' ').strip()
        back_clean = back.replace('\n', ' ').strip()
        f.write(f"{front_clean}\t{back_clean}\n")

print(f"Successfully converted {len(matches)} cards!")
