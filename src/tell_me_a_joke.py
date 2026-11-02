import json
import logging
import os
import requests

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/lab4.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def main():
    try:
        response = requests.get(url='https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}, timeout=10)
        if response.status_code == 200:
            logging.info("[LAB4_JOKE_HTTP_OK]")
            data = response.json()
            joke_text = data.get("joke", "")
            logging.info("[LAB4_JOKE_JSON_OK]")
            with open("data/joke.json", "w") as f:
                json.dump(data, f, indent=4)
            with open("data/joke.txt", "w") as f:
                f.write(joke_text)
            print(joke_text)
            logging.info("[LAB4_JOKE_PRINTED]")
    except requests.exceptions.RequestException as e:
        logging.error(f"[LAB4_ERR] HTTP request failed: {e}")

if __name__ == "__main__":
    logging.info("[LAB4_START]")
    main()