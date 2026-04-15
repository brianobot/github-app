from functools import partial
from typing import Callable

import environ
import requests

env = environ.Env()
env.read_env(".env")  # , overwrite=True)

ACCESS_TOKEN = env("GITHUB_ACCESS_TOKEN")


def get_headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {ACCESS_TOKEN}",
    }


def get_user_attribute(attr: str, params: dict | None = None) -> dict[str, str]:
    url = f"https://api.github.com/user/{attr}"
    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()


def check_rate_limit() -> dict[str, str]:
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=get_headers())
    return response.json()


def get_profile_url(profile_name: str) -> str:
    return f"https://github.com/{profile_name}"


def get_all(
    func: Callable, params: dict, key: list[str] = ["login", "followers_url"]
) -> list:
    page = is_valid = 1
    attrs = []
    while is_valid:
        attr: dict = func(params={**params, "page": page})

        if isinstance(attr, dict):
            if attr.get("message") == "Bad credentials":
                raise ValueError("Bad Credentials")

        new_attr = []
        for single_attr in attr:
            _key = single_attr.get(key[0])
            _value = get_profile_url(single_attr.get(key[0]))
            new_attr.append({f"{_key}": _value})

        attrs.extend(new_attr)
        if len(attr) < params.get("per_page", 30):
            is_valid = False

        print(f"Page {int(page)} - Length: {len(new_attr)}")
        page += 1

    return attrs


def write_to_file(attrs: list[tuple[str, str]], filename: str) -> int:
    with open(f"data/{filename}.txt", "w") as file:
        for attr in attrs:
            file.write(f"{attr}" + "\n")
        file_no = file.fileno()
    return file_no


def compare_files(file1: str, file2: str):
    file1_data = set(open(file1).readlines())
    file2_data = set(open(file2).readlines())

    return file2_data - file1_data


def main():
    get_followers_func = partial(get_user_attribute, "followers")
    get_followings_func = partial(get_user_attribute, "following")
    # get_public_repositories = partial(get_user_attribute, "repos")

    all_followers = get_all(get_followers_func, params={"per_page": 100})
    all_followings = get_all(get_followings_func, params={"per_page": 100})
    # all_repositories = get_all(get_public_repositories, params={"per_page": 100})

    diffs = set((tuple(item.items()) for item in all_followings)) - set(
        (tuple(item.items()) for item in all_followers)
    )
    write_to_file(list(diffs), "not-following-back")

    print("⏲️ Rate Limit: ", check_rate_limit())


if __name__ == "__main__":
    main()
