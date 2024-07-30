import threading
from main import main as run_main_assistant
from whatsapp_server import run as run_whatsapp_server

def run_assistant_thread():
    run_main_assistant()

def run_whatsapp_thread():
    run_whatsapp_server()

if __name__ == "__main__":
    # Create threads for the main assistant and WhatsApp server
    assistant_thread = threading.Thread(target=run_assistant_thread)
    whatsapp_thread = threading.Thread(target=run_whatsapp_thread)

    # Start both threads
    assistant_thread.start()
    whatsapp_thread.start()

    # Wait for both threads to complete
    assistant_thread.join()
    whatsapp_thread.join()
