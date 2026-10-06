from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

class SummarizationError(Exception):
    pass

def summarize(text: str) -> str:
    """Summarize the text extracted from the PDF and return it as a string"""

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the given text concisely; avoid using fillers or a preamble."
                },
                {
                    "role": "user",
                    "content": f"{text}"
                }
            ],

            model="openai/gpt-oss-120b"
        )

    except Exception as err:
        # "from err" below indicates exception chaining.
        # Python implicitly catches exception chaining, however, the messages displayed are different.
        # without from err: "During handling of the above exception, another exception occurred:" is set as the __context__
        # with from err: "The above exception was the direct cause of the following exception:" is set as the __cause__
        raise SummarizationError(f"LLM summarization failed: {err}") from err
    else:
        return response.choices[0].message.content