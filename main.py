import requests
from urllib.parse import urlparse
import os
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


def count_clicks(token, link):
  headers = {
    "Authorization": "Bearer {}".format(token) 
    }
  url = "https://api-ssl.bitly.com/v4/bitlinks/{domain}{bitlink}/clicks/summary".format(domain=urlparse(link).netloc, bitlink=urlparse(link).path)
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
  token = os.getenv("BITLY_TOKEN")
  args = parse_arguments()
  user_input = args.input_url
  
  try:
    bitlink = shorten_link(token, user_input)
    print(bitlink)
  except requests.exceptions.HTTPError:
    try:
      clicks_count = count_clicks(token, user_input)
      print(clicks_count)
    except requests.exceptions.HTTPError:
      print("Неверно введена ссылка")


if __name__ == "__main__":
  main()