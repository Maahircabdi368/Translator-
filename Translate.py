import re
from transformers import MarianMTModel, MarianTokenizer

# Model English -> Somali
model_name = "Helsinki-NLP/opus-mt-en-so"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Check if line is "code/assembly/command"
def looks_like_code(line):
    code_keywords = ["mov", "jmp", "push", "ret", "nop", "cmp", "%", "$0x", "call", "lea", "objdump"]
    return any(kw in line for kw in code_keywords)

# Clean and split text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.?!])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

# Translate one sentence
def translate_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs, max_length=256)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Main translation with code detection
def english_to_somali(text):
    lines = text.splitlines()
    results = []
    for line in lines:
        if looks_like_code(line):
            results.append(line)  # keep code same
        else:
            # turjumaad kaliya English
            sentences = clean_text(line)
            if sentences:
                translated = [translate_sentence(s) for s in sentences]
                results.extend(translated)
            else:
                results.append(line)
    return "\n".join(results)

# ===============================
# Tijaabo
english_text = """
Hello my brother. Yesterday I went to the market but forgot milk.

reader@hacking:~/booksrc $ objdump -D a.out | grep -A20 main.:
08048374 <main>:
 8048374: 55 push %ebp
 8048375: 89 e5 mov %esp,%ebp
"""

print("=== Output ===")
print(english_to_somali(english_text))
