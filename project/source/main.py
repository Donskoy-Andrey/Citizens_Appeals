import os


def main():
    """Entry point for project"""
    os.system("D:/Programms/ngrok/ngrok http 8000")
    # os.system('curl -s http://localhost:4040/api/tunnels | python3 -c' +
    #            "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")


if __name__ == "__main__":
    main()
