import subprocess
import threading
import time
from dotenv import load_dotenv
from .common.logger import get_logger
from .common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except Exception as e:
        logger.error("Backend server failed to start")
        raise CustomException("Backend server failed to start", error_detail=e)
    
def run_frontend():
    try:
        logger.info("Starting Frontend service")
        subprocess.run(["streamlit" , "run" , "app/frontend/ui.py"],check=True)
    except Exception as e:
        logger.error("Problem with frontend service")
        raise CustomException("Frontend failed to start" , error_detail=e)

if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    
    except CustomException as e:
        logger.exception(f"CustomException occured : {str(e)}")