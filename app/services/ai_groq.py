from groq import AsyncGroq
from app.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


async def ask_groq(question: str, document_text: str) -> str:

    system_prompt = """You are a helpful assistant that answers questions strictly based on the document provided by the user.

Your rules:
- Only use information from the document to answer
- If the answer is not in the document, say exactly: "I could not find this information in the uploaded document."
- Do not use any outside knowledge
- Do not make up or guess any information
- Keep your answers clear, concise , to the point and from the document only
- Do not add any extra letter which is not in the Document only send the answer which is in document
- Even if a question is answered in interactive form you dont have to be interactive and only reply from the text given in the document only send that"""

    user_message = f"""Here is the document:

--- START OF DOCUMENT ---
{document_text}
--- END OF DOCUMENT ---

Question: {question}"""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0,
        max_tokens=2048
    )

    return response.choices[0].message.content
