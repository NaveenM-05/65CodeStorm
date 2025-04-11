
from fastapi import FastAPI, Request, Form
from logger import log_service_request  # Assuming you already have this
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/whatsapp")
async def handle_whatsapp(request: Request, From: str = Form(...), Body: str = Form(...)):
    try:
        # Log the message to terminal
        print(f"📩 WhatsApp Message Received:\nFrom: {From}\nBody: {Body}\n{'-'*50}")
        
        # Log to service_requests.log file
        log_message = f"WhatsApp Message - From: {From}, Body: {Body}"
        log_service_request(log_message)

        # Placeholder response (customize if needed)
        return JSONResponse(content={"status": "success", "message": "Message received"}, status_code=200)
    
    except Exception as e:
        error_message = f"Error in WhatsApp handler: {str(e)}"
        print("❌", error_message)
        log_service_request(error_message)
        return JSONResponse(content={"status": "error", "message": "Internal server error"}, status_code=500)

