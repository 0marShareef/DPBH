from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from fastapi.templating import Jinja2Templates
import PIL.Image
import io
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

os.environ['GOOGLE_API_KEY'] = "AIzaSyB6wn3odWjs3JjVjjikMhL5fr-8rKyd_WA"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('LLaVa-V4')

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    image = PIL.Image.open(io.BytesIO(content))

    response = model.generate_content(['''
        Generate a caption describing any dark patterns in the given image of a web/mobile UI. 
        A dark pattern (also known as a "deceptive design pattern") is "a user interface that has been 
        carefully crafted to trick users into doing things, 
        such as buying overpriced insurance with their purchase or signing up for recurring bills". 
        The image may or may not contain any dark patterns. If there are no dark patterns detected,
        then just reply with "No dark patterns".
        Only provide the caption in your response and no additional text. 
        Remember, use your knowledge to check if a dark pattern actually exists in the image.
        If there are no dark patterns then just reply with "No dark patterns"
    ''', image])

    return {"text_output": response.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
