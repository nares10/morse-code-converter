import tkinter as tk
from tkinter import messagebox

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.', ':': '---...', ',': '--..--',
    '=': '-...-', '!': '-.-.--', '.': '.-.-.-', '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'
}

# Function to convert text to morse code
def text_to_morse(text):
    morse_code = ''
    case_info = []
    for char in text:
        if char.upper() in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char.upper()] + ' '
            case_info.append(char.islower())
        else:
            morse_code = morse_code.rstrip() + ' / '  # separator for words
            case_info.append(None)  # space character
    return morse_code.rstrip(), case_info

# Function to convert morse code to text
def morse_to_text(morse_code, case_info):
    if not morse_code:
        return ""
    
    morse_code = morse_code.strip().split(' ')
    decipher = ''
    index = 0
    for letter in morse_code:
        if letter == '/':
            decipher += ' '  # adding space to separate words
            index += 1
        else:
            if letter:
                char = list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(letter)]
                if case_info[index]:
                    char = char.lower()
                decipher += char
                index += 1
    return decipher

# Functions for the buttons
def convert_text_to_morse():
    text = text_entry.get()
    morse_code, case_info = text_to_morse(text)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, morse_code)
    result_text.config(state=tk.DISABLED)
    text_entry.delete(0, tk.END)
    result_text.case_info = case_info  # Store case info in the result_text widget

def convert_morse_to_text():
    morse_code = text_entry.get()
    try:
        case_info = getattr(result_text, 'case_info', [None] * len(morse_code.split()))
        text = morse_to_text(morse_code, case_info)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, text)
        result_text.config(state=tk.DISABLED)
    except ValueError:
        messagebox.showerror("Error", "Invalid Morse Code")
    text_entry.delete(0, tk.END)

def select_conversion():
    selection = conversion_var.get()
    text_entry.delete(0, tk.END)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    
    if selection == "Text to Morse Code":
        text_entry_label.config(text="Enter text to convert to Morse code:")
        convert_button.config(command=convert_text_to_morse)
    elif selection == "Morse Code to Text":
        text_entry_label.config(text="Enter Morse code to convert to text (use space between letters and '/' for spaces between words):")
        convert_button.config(command=convert_morse_to_text)

# Setting up the GUI
root = tk.Tk()
root.title("Morse Code Converter")
root.geometry("600x400")  # Set default window size

# Make the window responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(sticky=tk.NSEW)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)

# Conversion selection
conversion_var = tk.StringVar(value="Text to Morse Code")
conversion_frame = tk.Frame(main_frame)
conversion_frame.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

conversion_label = tk.Label(conversion_frame, text="Select conversion type:")
conversion_label.pack(side=tk.LEFT)

conversion_option1 = tk.Radiobutton(conversion_frame, text="Text to Morse Code", variable=conversion_var, value="Text to Morse Code", command=select_conversion)
conversion_option1.pack(side=tk.LEFT)

conversion_option2 = tk.Radiobutton(conversion_frame, text="Morse Code to Text", variable=conversion_var, value="Morse Code to Text", command=select_conversion)
conversion_option2.pack(side=tk.LEFT)

# Entry for input
text_entry_label = tk.Label(main_frame, text="Enter text to convert to Morse code:")
text_entry_label.grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)

text_entry = tk.Entry(main_frame, width=50)
text_entry.grid(row=2, column=0, pady=5, padx=10, sticky=tk.EW)
text_entry.bind("<Return>", lambda event: convert_button.invoke())  # Bind Enter key to Convert button

# Convert button
convert_button = tk.Button(main_frame, text="Convert", command=convert_text_to_morse)
convert_button.grid(row=3, column=0, pady=5, padx=10, sticky=tk.W)

# Text widget for result
result_text = tk.Text(main_frame, height=5, width=50, state=tk.DISABLED)
result_text.grid(row=4, column=0, pady=20, padx=10, sticky=tk.NSEW)

# Start the GUI loop
root.mainloop()

