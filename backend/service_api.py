from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Initialize FastAPI app
app = FastAPI(title="Service Request API")

# Set up basic logging to a file
logging.basicConfig(
    level=logging.INFO,
    filename="service_requests.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    filemode="a"  # Append mode
)

# Define the data model for service requests using Pydantic
class ServiceRequest(BaseModel):
    customer_id: str
    issue_category: str
    message: str

# Define a POST endpoint to create a service request
@app.post("/service-request")
def create_service_request(request: ServiceRequest):
    try:
        # Log the service request details
        logging.info(
            f"Service Request - Customer: {request.customer_id}, "
            f"Issue: {request.issue_category}, Message: {request.message}"
        )
        # For now, just return a success response
        return {"status": "success", "detail": "Service request logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with Uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
