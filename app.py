""" proto app as well as initial operator against the api """
import subprocess
import threading
import time
import requests

PORT_NUMBER = 8765

def run_api():
    subprocess.run(["uvicorn", "api.server:app", "--log-level=warning", f"--port={PORT_NUMBER}"])

def run_cmd_prompts():
    print("\r\n\r\n----------------")
    print("SplitWiser")
    print("----------------\r\n")
    is_running = True
    while is_running:
        x = input("What is your favorite color? ")
        print(f"{x}... NO, wait... ahhhhhh!")
        if x.lower() == 'exit':
            is_running = False
    print("\r\nShutting down...")
    requests.get(f"http://localhost:{PORT_NUMBER}/shutdown")
    time.sleep(3)


def run_main():
    print("loading...")
    t_api = threading.Thread(target=run_api, name='API')
    t_ui = threading.Thread(target=run_cmd_prompts, name='Command-Based UI')

    t_api.start()
    time.sleep(5)
    t_ui.start()

    t_ui.join()
    t_api.join()
    print("omg done!")
    


if __name__ == "__main__":
    run_main() 