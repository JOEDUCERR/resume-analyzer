from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer Running"
    }


@app.get("/test")
def test():
    return {
        "message": "test works"
    }


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    print("File received")

    content = await file.read()

    print("File read complete")

    resume_text = content.decode("utf-8")

    print("Calling OpenAI")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert HR recruiter.

                Analyze resumes and provide:
                1. Candidate Summary
                2. Skills Found
                3. Recommended Job Roles
                4. Missing Skills
                """
            },
            {
                "role": "user",
                "content": resume_text
            }
        ]
    )

    print("OpenAI response received")

    return {
        "analysis": response.choices[0].message.content
    }