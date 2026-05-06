# Clean OCR Noise
from utils.text_cleaning import clean_text

text = f'''Dr. Jo hn Sm ith
        MD
        '''
print("text = ",text)
print(clean_text(text))