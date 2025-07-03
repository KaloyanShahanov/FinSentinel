import logging
from app.api import app
from app.sentinel import start_crypto_monitor
#from app.alerts import send_test_email  

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

   # logging.info("Sending test email alert at startup...")
   # try:
   #     send_test_email()
   #     logging.info("Test email alert sent successfully.")
   # except Exception as e:
   #    logging.error(f"Failed to send test email alert: {e}")

    logging.info("Starting crypto monitor thread...")
    try:
        start_crypto_monitor()
        logging.info("Crypto monitor started successfully.")
    except Exception as e:
        logging.error(f"Failed to start crypto monitor: {e}")

    import uvicorn

    logging.info("Starting FastAPI server...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logging.error(f"Failed to start FastAPI server: {e}")
