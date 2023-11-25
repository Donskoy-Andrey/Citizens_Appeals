import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "cointegrated/rut5-base-absum"
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model.eval()


def summarize(
    text,
    n_words=None,
    compression=None,
    max_length=1000,
    num_beams=3,
    do_sample=False,
    repetition_penalty=10.0,
    **kwargs
):
    """
    Summarize the text
    The following parameters are mutually exclusive:
    - n_words (int) is an approximate number of words to generate.
    - compression (float) is an approximate length ratio of summary and original text.
    """
    try:
        if n_words:
            text = "[{}] ".format(n_words) + text
        elif compression:
            text = "[{0:.1g}] ".format(compression) + text
        x = tokenizer(text, return_tensors="pt", padding=True).to(model.device)
        with torch.inference_mode():
            out = model.generate(
                **x,
                max_length=max_length,
                num_beams=num_beams,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty,
                **kwargs
            )
    except Exception:
        print("###_Exception in summary prediction_###")
        return text
    else:
        return tokenizer.decode(out[0], skip_special_tokens=True)
