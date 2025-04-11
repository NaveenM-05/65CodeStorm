from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/incoming-whatsapp")
async def receive_whatsapp(
    From: str = Form(...),
    Body: str = Form(...)
):
    print("📲 WhatsApp Message Received:")
    print("From:", From)
    print("Message:", Body)
    print("-" * 50)
    return PlainTextResponse("Message received")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
