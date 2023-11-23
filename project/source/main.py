import os

from IPython import get_ipython


def main():
    """Entry point for project"""
    os.system("D:/Programms/ngrok/ngrok http 8501")
    # os.system('curl -s http://localhost:4040/api/tunnels | python3 -c' +
    #            "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")
    # print("Hello world!")


if __name__ == "__main__":
    main()
