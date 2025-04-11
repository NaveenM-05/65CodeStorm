from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="WhatsApp Simulator")

# Define the message payload using Pydantic
class WhatsAppMessage(BaseModel):
    customer_id: str
    message: str

@app.post("/simulate-whatsapp")
def simulate_whatsapp(msg: WhatsAppMessage):
    # For now, we simply print the message to the console to simulate message receipt.
    print(f"Simulated WhatsApp message from {msg.customer_id}: {msg.message}")
    # Return a simple response to acknowledge receipt.
    return {"status": "received", "data": msg}

# For running the server directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
