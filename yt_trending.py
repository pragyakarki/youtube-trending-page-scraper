import requests
import sys
import json
import time
import os
import argparse

executed_on = time.strftime('%Y-%m-%d %H:%M:%S')
current_dir = os.getcwd()

YOUTUBE_DATA_API_KEY_FOR_GITHUB_1 = os.environ['YOUTUBE_DATA_API_KEY_FOR_GITHUB_1']
YOUTUBE_DATA_API_KEY_FOR_GITHUB_2 = os.environ['YOUTUBE_DATA_API_KEY_FOR_GITHUB_2']

i18nRegions_list_1 = ['DZ', 'AR', 'AU', 'AT', 'AZ', 'BH', 'BD', 'BY', 'BE', 'BO', 'BA', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'HR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'EG', 'SV', 'EE',
                      'FI', 'FR', 'GE', 'DE', 'GH', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KW', 'LV', 'LB', 'LY', 'LI', 'LT', 'LU', 'MY']

i18nRegions_list_2 = ['MT', 'MX', 'ME', 'MA', 'NP', 'NL', 'NZ', 'NI', 'NG', 'MK', 'NO', 'OM', 'PK', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'PR', 'QA', 'RO', 'RU',
                      'SA', 'SN', 'RS', 'SG', 'SK', 'SI', 'ZA', 'KR', 'ES', 'LK', 'SE', 'CH', 'TW', 'TZ', 'TH', 'TN', 'TR', 'UG', 'UA', 'AE', 'GB', 'US', 'UY', 'VE', 'VN', 'YE', 'ZW']


def api_request(page_token, country_code, api_key):
    video_resource = "id,snippet,contentDetails,status,statistics,player,topicDetails,recordingDetails,localizations"

    # Builds the URL and requests the JSON from it
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part={video_resource}{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    response = requests.get(request_url)

    print(
        f"{executed_on} :: RESPONSE Status-Code: {response.status_code} || Content-Type: {response.headers['content-type']}")

    if response.status_code == 429:
        print(
            f"{executed_on} :: Temporarily BANNED due to excess requests. EXITING...")
        sys.exit()
    return response.json()


def get_pages(country_code, api_key, next_page_token="&"):
    country_data = []
    while next_page_token is not None:
        video_data_page_json = api_request(
            next_page_token, country_code, api_key)
        next_page_token = video_data_page_json.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        items = video_data_page_json.get('items')
        for item in items:
            country_data.append(item)

    return country_data


def write_to_file(country_code, country_data):

    print(f"{executed_on} :: Writing {country_code} data to file...")

    executed_time = time.strftime('%y.%m.%d') # Create one folder for each day
    path = os.path.join(current_dir, executed_time)
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{time.strftime('%y.%m.%d %H.%M.%S')}_{country_code}_YouTube_Trending_Videos.json", "w+", encoding='utf-8') as file:
        json.dump(country_data, file, ensure_ascii=False, indent=4)
        print(f"{executed_on} :: Done for {country_code}")


def get_data(country_codes, api_key):
    for country_code in country_codes:
        country_data = get_pages(country_code, api_key)
        write_to_file(country_code, country_data)


if __name__ == "__main__":
    get_data(i18nRegions_list_1, YOUTUBE_DATA_API_KEY_FOR_GITHUB_1)
    get_data(i18nRegions_list_2, YOUTUBE_DATA_API_KEY_FOR_GITHUB_2)
