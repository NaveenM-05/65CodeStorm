from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from logger import log_service_request  # Use the shared logger

app = FastAPI()

@app.post("/whatsapp")
async def handle_whatsapp(request: Request, From: str = Form(...), Body: str = Form(...)):
    try:
        # Log to terminal
        print(f"📩 WhatsApp Message Received:\nFrom: {From}\nBody: {Body}\n{'-'*50}")
        
        # Create a log message and log it in service_request.log
        log_message = f"WhatsApp Message - From: {From}, Body: {Body}"
        log_service_request(log_message)

        # Return a JSON response
        return JSONResponse(content={"status": "success", "message": "Message received"}, status_code=200)
    
    except Exception as e:
        error_message = f"Error in WhatsApp handler: {str(e)}"
        print("❌", error_message)
        log_service_request(error_message)
        return JSONResponse(content={"status": "error", "message": "Internal server error"}, status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
