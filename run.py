import uvicorn

if __name__ == "__main__":
    print("Starting DIV_SECRET_ID KYC Verification Gateway on port 8005...")
    uvicorn.run("gateway.main:app", host="127.0.0.1", port=8005, reload=True)
