import requests
import time
import json
import os
import pathlib import Path

executed_on = time.strftime('%Y-%m-%d %H:%M:%S')
YOUTUBE_DATA_API_KEY_FOR_GITHUB_1 = os.environ['YOUTUBE_DATA_API_KEY_FOR_GITHUB_1']

current_dir = Path(__file__).parent.resolve()


def fetch_i18nRegions():
    request_url = f"https://www.googleapis.com/youtube/v3/i18nRegions?part=snippet&key={YOUTUBE_DATA_API_KEY_FOR_GITHUB_1}"

    response = requests.get(request_url)

    print(
        f"{executed_on} :: RESPONSE Status-Code: {response.status_code} || Content-Type: {response.headers['content-type']}")

    if response.status_code == 429:
        print(
            f"{executed_on} :: Temporarily BANNED due to excess requests. EXITING...")
        sys.exit()

    return response.json()


def main():
    try:
        i18nRegions_json_data = fetch_i18nRegions()
    except Exception as err:
        raise Exception('API changed.')

    items = i18nRegions_json_data.get("items")

    print(f"{executed_on} :: Number of regions supported : {len(items)}")

    with open(f"{current_dir}/i18nRegions_list.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4)
        print(f"{executed_on} :: Done!")


if __name__ == '__main__':
    main()
