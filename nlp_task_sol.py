# Import required library
import spacy
import nltk
from nltk.corpus import words
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt_tab')
nltk.download('words')

# Inputs of each testcase
text1 = "In April 2023, Sundar Pichai did announce that Google would be launehing a new AI product namcd Gemini. Barack Obama also gave a speech at Harvard University, cmphasizing the role of technology in modern education."
text2 = "Project X is an exclusive elub at Veermata Jijabai Technological Institute, Mumbai, mcant to 5erve as a healthy environment for 5tudents to learn from each other and grow together. Through the guidance of their mcntors these 5tudents are able to complete daunting tasks in a relatively short time frame, gaining significant exposure and knowledge in their domain of choice."
text3 = "I will be eompleting my BTech dcgree in Mechanical Engineering from VJTI in 2028"
text4 = "However the rcsults were clear"

# Parse the input text
doc1 = nlp(text4)
# Extract tokens from the original doc
tokens = [token.text for token in doc1]

# Load the list of valid English words (lowercase for comparison)
english_vocab = set(w.lower() for w in words.words())

# Initialize
print_things = []
misspelled = []
misspelledno = []
corrected_tokens = []

# Collect misspelled words
for token in doc1 :
  if token.is_alpha and token.text.lower() not in english_vocab :
    if not any(ent.label_ in {'PERSON', 'ORG', 'GPE'} and ent.start <= token.i < ent.end for ent in doc1.ents) :
        misspelled += [token.text]
  if token.text.isalnum() and not token.is_alpha and not token.is_digit and token.text.lower() not in english_vocab :
    if not any(ent.label_ in {'PERSON', 'ORG'} and ent.start <= token.i < ent.end for ent in doc1.ents) :
        misspelledno += [token.text]

# Dictionary containing OCR-style character corrections and full-word fixes
ocr_replaceno = {
    '0' : 'o' ,
    '1' : 'l' ,
    '2' : 'i' ,
    '3' : 'e' ,
    '4' : 'a' ,
    '5' : 's' ,
    '6' : 'b' ,
    '7' : 't' ,
    '8' : 'g' ,
    '9' : 'z'
}

ocr_replace = {
    '0' : 'o' ,
    '1' : 'l' ,
    '2' : 'i' ,
    '3' : 'e' ,
    '4' : 'a' ,
    '5' : 's' ,
    '6' : 'b' ,
    '7' : 't' ,
    '8' : 'g' ,
    '9' : 'z' ,
    'e' : 'c' ,
    'c' : 'e'
}

# Function to correct each word character by character
def correct_ocrce(word):
    # convert string to list for easy character replacement
    corrected = list(word)
    for i in range(min(3, len(word))):
        corrected[i] = ocr_replace.get(corrected[i], corrected[i])
    return ''.join(corrected)

# Function to correct each word character by character
def correct_ocr(word):
    return ''.join(ocr_replace.get(char, char) for char in word)

# Function to correct each word character by character
def correct_ocrno(word):
    return ''.join(ocr_replaceno.get(char, char) for char in word)

# Reconstruct full sentence with corrections
def apply_all_corrections(token):
    word = token.text
    ce_count = word.count('c') + word.count('e')
    original = word
    c = 0
    if ce_count > 1 and original in misspelled :
        word = correct_ocrce(word)
    if word in misspelled:
        word = correct_ocr(word)
    elif word in misspelledno:
        word = correct_ocrno(word)
    if word.lower() in ['however', 'whatever', 'although', 'but', 'nevertheless', 'eventhough', 'whereas'] :
      word += ','
    return word

corrected_tokens = [apply_all_corrections(token) for token in doc1]

# Reassemble full corrected sentence
fixed_statement = ' '.join(corrected_tokens)
print(fixed_statement)

# Re-parse the fixed text
doc2 = nlp(fixed_statement)

# Extract PERSON, ORG, and valid GPE entities
for ent in doc2.ents :
  if not len(ent.text) <= 3 :
    if ent.label_ == 'PERSON':
      print_things.append(ent.text)
    if ent.label_ == 'ORG':
      print_things.append(ent.text)
    if ent.label_ == 'GPE':
      print_things.append(ent.text)

# Print the final list of extracted entities
print(print_things)