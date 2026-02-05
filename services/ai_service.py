from google import genai

MODEL_NAME = "gemini-3-flash-preview"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")

def generate_bio(name: str,info: str,style: str) -> str:
    api_key=GEMINI_API_KEY
    style_map={
        "short":"very short and punchy",
        "professional":"professional and trustworthy",
        "fun":"fun and friendly"
    }
    style_text=style_map.get(style,"clear and modern")

    prompt=f"""
    Write a short link-in-bio profile text.
    Name: {name}
    About: {info}
    Style: {style_text}
    
    Rules:
    -2 or 3 sentences only
    -good for social/profile page
    -no emojis unless fun style or is requested 
    -no hashtags
    """
    client=genai.Client(api_key=api_key)
    try:
        response=client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return (response.text or "").strip() or "No result from AI (empty text)."
    except Exception as e:
        return f"AI Error: {e}"


