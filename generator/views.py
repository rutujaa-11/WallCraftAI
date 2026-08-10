import re
from django.shortcuts import render
from .models import GeneratedImage
from .ai_models.mural_ai import generate_mural
from .ai_models.painting_ai import generate_painting
from .ai_models.general_ai import generate_general


# ==========================================
# PROMPT VALIDATION
# ==========================================

def is_valid_prompt(text):
    text = text.strip()

    if "--no" in text:
        parts = text.split("--no", 1)
        positive_part = parts[0].strip()
        negative_part = parts[1].strip() if len(parts) > 1 else ""
        if not negative_part:
            return False

    elif "--neg" in text:
        parts = text.split("--neg", 1)
        positive_part = parts[0].strip()
        negative_part = parts[1].strip() if len(parts) > 1 else ""
        if not negative_part:
            return False

    else:
        positive_part = text

    if len(positive_part) < 3 or not re.search(r"[a-zA-Z]", positive_part):
        return False

    if positive_part.lower() in [
        "abc", "asdf", "asdfgh", "qwerty", "aeiou", "uoiea", "aeiouy", "zxcvbn", "qazwsx"
    ]:
        return False

    if re.search(r"^(.)\1+$", positive_part):
        return False

    words = positive_part.split()
    vowels = set("aeiouyAEIOUY")

    for word in words:
        clean_word = re.sub(r"[^a-zA-Z]", "", word)

        if len(clean_word) < 2:
            continue

        if len(clean_word) >= 4:
            if not any(char in vowels for char in clean_word):
                return False

        if len(clean_word) >= 6:
            if re.search(r"[^aeiouy]{5,}", clean_word, re.IGNORECASE):
                return False

            if re.search(r"[aeiouy]{5,}", clean_word, re.IGNORECASE):
                return False

    return True


# ==========================================
# VIEWS
# ==========================================

def home(request):
    return render(request, "mural.html")


def mural(request):
    image = None
    error = None

    if request.method == "POST":
        raw_prompt = request.POST.get("prompt")

        if raw_prompt is None or raw_prompt.strip() == "":
            error = "Error: Please enter a prompt!"

        elif not is_valid_prompt(raw_prompt.strip()):
            error = "Error: Invalid prompt type. Please provide a clear description."

        else:
            prompt = raw_prompt.strip()
            try:
                image = generate_mural(prompt)
                GeneratedImage.objects.create(
                    prompt=prompt,
                    image_url=image,
                    category="Mural"
                )
            except Exception as e:
                error = "Error: Image generation failed. Please try again."
                print("MURAL ERROR:", e)

    return render(request, "mural.html", {"image": image, "error": error})


def painting(request):
    image = None
    error = None

    if request.method == "POST":
        raw_prompt = request.POST.get("prompt")

        if raw_prompt is None or raw_prompt.strip() == "":
            error = "Error: Please enter a prompt!"

        elif not is_valid_prompt(raw_prompt.strip()):
            error = "Error: Invalid prompt type. Please provide a clear description."

        else:
            prompt = raw_prompt.strip()
            try:
                image = generate_painting(prompt)
                GeneratedImage.objects.create(
                    prompt=prompt,
                    image_url=image,
                    category="Painting"
                )
            except Exception as e:
                error = "Error: Image generation failed. Please try again."
                print("PAINTING ERROR:", e)

    return render(request, "painting.html", {"image": image, "error": error})


def general(request):
    image = None
    error = None

    if request.method == "POST":
        raw_prompt = request.POST.get("prompt")

        if raw_prompt is None or raw_prompt.strip() == "":
            error = "Error: Please enter a prompt!"

        elif not is_valid_prompt(raw_prompt.strip()):
            error = "Error: Invalid prompt type. Please provide a clear description."

        else:
            prompt = raw_prompt.strip()
            try:
                image = generate_general(prompt)
                GeneratedImage.objects.create(
                    prompt=prompt,
                    image_url=image,
                    category="General"
                )
            except Exception as e:
                error = "Error: Image generation failed. Please try again."
                print("GENERAL ERROR:", e)

    return render(request, "general.html", {"image": image, "error": error})