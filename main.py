import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse

def shorten_link(token, url):
  headers = {
    "Authorization": "Bearer {}".format(token)       
    }
  payload = {
    "long_url": url     
    }
  response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json=payload)
  response.raise_for_status()
  bitlink = response.json()["link"]
  return bitlink


def count_clicks(token, parsed_url):
  headers = {
    "Authorization": "Bearer {}".format(token) 
    }
  url = "https://api-ssl.bitly.com/v4/bitlinks/{domain}{bitlink}/clicks/summary".format(domain=parsed_url.netloc, bitlink=parsed_url.path)
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  clicks_count = response.json()["total_clicks"]
  return clicks_count

def parse_arguments():
  parser = argparse.ArgumentParser(
      description='Create short url and count clicks')
  parser.add_argument('input_url', type=str, help='url to create a short link or a short link to count clicks')

  return parser.parse_args()

def main():
  load_dotenv()
  token = os.getenv("BITLY_TOKEN")
  args = parse_arguments()
  user_input = args.input_url
  parsed_url = urlparse(user_input)

  try:
    bitlink = shorten_link(token, user_input)
    print(bitlink)
  except requests.exceptions.HTTPError:
    try:
      clicks_count = count_clicks(token, parsed_url)
      print(clicks_count)
    except requests.exceptions.HTTPError:
      print("Неверно введена ссылка")


if __name__ == "__main__":
  main()