#!/usr/bin/env python3
import os
import torch
from PIL import Image
from lavis.models import load_model_and_preprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "merlion.png")

    raw_image = Image.open(image_path).convert("RGB")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Correct pairing
    model, vis_processors, text_processors = load_model_and_preprocess(
        name="blip2_t5",
        model_type="caption_coco_flant5xl",  # or "flant5xxl" if you have enough VRAM
        device=device,
        is_eval=True
    )

    img = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    prompt = "Is there a merlion in the image? Answer yes or no."

    print("Running inference...")
    answer = model.generate({"image": img, "prompt": prompt})[0]

    print(f"Prompt: {prompt}")
    print(f"Response: {answer}")

if __name__ == "__main__":
    main()
