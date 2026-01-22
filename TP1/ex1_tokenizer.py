from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
phrase = "Artificial intelligence is metamorphosing the world!"

tokens = tokenizer.tokenize(phrase)

print(tokens)


token_ids = tokenizer.encode(phrase)
print("Token IDs:", token_ids)

print("Détails par token:")
for tid in token_ids:
    txt = tokenizer.decode([tid])
    print(tid, repr(txt))


# suite questions 

phrase2 = "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism."

tokens2 = tokenizer.tokenize(phrase2)
print(tokens2)

long_word = "antidisestablishmentarianism"
long_word_tokens = tokenizer.tokenize(long_word)
print(long_word_tokens)

subtoken_count = len(long_word_tokens)
print("Nombre de sous-tokens:", subtoken_count)
