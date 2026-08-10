import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_API_TOKEN
)


def generate_general(prompt):
    clean_prompt = prompt.strip()

    low_quality_keywords = ["blurry", "low quality", "ugly", "distorted", "pixelated", "bad quality"]

    if any(keyword in clean_prompt.lower() for keyword in low_quality_keywords):
        full_prompt = f"{clean_prompt}, 16:9"
    else:
        full_prompt = (
            f"{clean_prompt}, "
            f"detailed, high quality, "
            f"sharp focus, "
            f"16:9"
        )

    try:
        image = client.text_to_image(
            prompt=full_prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )

        os.makedirs("media/generated", exist_ok=True)
        filename = "media/generated/general_generated.png"
        image.save(filename)

        return "/media/generated/general_generated.png"

    except Exception as e:
        print("GENERAL AI ERROR:", e)
        raise