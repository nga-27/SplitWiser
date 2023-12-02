""" proto app as well as initial operator against the api """
import subprocess

def run_main():
    subprocess.run(["uvicorn", "api.server:app", "--reload"]) 


if __name__ == "__main__":
    run_main() 