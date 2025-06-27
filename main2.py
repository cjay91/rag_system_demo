from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

from typing import Annotated
from pydantic import BaseModel, Field

class Response(BaseModel):
    answer: Annotated[str, Field(description="The answer to the question")]
    rating: Annotated[int, Field(description="The rating of the answer from 1 to 10")]
    safety_rating: Annotated[int, Field(description="The safety rating of the answer from 1 to 10 for kids, 10 being the safest")]

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=my_api_key)
llm = genai.GenerativeModel("gemma-3-4b-it")

prompt = (
    "Answer the following question in JSON format with keys: answer (string), "
    "rating (integer 1-10), safety_rating (integer 1-10, 10 safest for kids).\n"
    "Question: Poem on India"
)

llm_response = llm.generate_content(prompt)
try:
    data = json.loads(llm_response.text)
    response = Response(**data)
    print(response.answer)
    print(response.rating)
    print(response.safety_rating)
except Exception as e:
    print("Could not parse response as JSON:", llm_response.text)
    print("Error:", e)

n = input("Enter the question: ")
# You can repeat the above logic for user input as well.