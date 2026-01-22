import os
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

SEED = 42
torch.manual_seed(SEED)
torch.set_num_threads(1)

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=30,
)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)


def generate_once(seed):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=30,
        do_sample=True,
        temperature=1,
        top_k=50,
        top_p=0.95,
        repetition_penalty=2.0,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)


for s in [1, 2, 3, 4, 5]:
    print("SEED", s)
    print(generate_once(s))
    print("-" * 40)

out_beam = model.generate(
    **inputs,
    max_length=50,
    num_beams=5,
    early_stopping=True,
)
txt_beam = tokenizer.decode(out_beam[0], skip_special_tokens=True)
print("---------")
print(txt_beam)

for beams in [10, 20]:
    start = time.time()
    out_beam = model.generate(
        **inputs,
        max_length=50,
        num_beams=beams,
        early_stopping=True,
    )
    elapsed = time.time() - start
    txt_beam = tokenizer.decode(out_beam[0], skip_special_tokens=True)
    print(f"num_beams={beams} time={elapsed:.3f}s")
    print(txt_beam)
