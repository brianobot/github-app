import requests
import environ
from functools import partial

env = environ.Env()
env.read_env(".env")#, overwrite=True)

ACCESS_TOKEN = env("GITHUB_ACCESS_TOKEN")


def get_headers() -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {ACCESS_TOKEN}",
    }


def get_user_attribute(attr: str, params: dict | None = None) -> dict:
    url = f"https://api.github.com/user/{attr}"
    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()


def check_rate_limit() -> dict:
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=get_headers())
    return response.json()


def get_profile_url(profile_name: str) -> str:
    return f"https://github.com/{profile_name}"


def get_all(
    func: callable, 
    params: dict, 
    key: list[str] = ["login", "followers_url"]
) -> list:
    page = is_valid = True
    attrs = []
    while is_valid:
        attr: dict = func(params={**params, "page": page})
        if isinstance(attr, dict):
            if attr.get("message") == "Bad credentials":
                raise ValueError("Bad Credentials")
        new_attr = [
            f"{each['login']}:{get_profile_url(each['login'])}" for each in attr
        ]
        attrs.extend(new_attr)
        if len(attr) < params.get("per_page", 30):
            is_valid = False

        print(f"Page {int(page)} - Length: {len(new_attr)}")
        page += 1
    return attrs


def write_to_file(attrs: list, filename: str) -> int:
    with open(f"{filename}.txt", "w") as file:
        for name in attrs:
            file.write(name + "\n")
        file_no = file.fileno()
    return file_no


def compare_files(file1: str, file2: str):
    file1_data = set(open(file1).readlines())
    file2_data = set(open(file2).readlines())

    return file2_data - file1_data


def main():
    get_followers_func = partial(get_user_attribute, "followers")
    get_followings_func = partial(get_user_attribute, "following")

    all_followers = get_all(get_followers_func, params={"per_page": 100})
    all_followings = get_all(get_followings_func, params={"per_page": 100})

    # write_to_file(all_followers, 'all-followers')
    # write_to_file(all_followings, 'all-followings')

    # diffs = compare_files('all-followers.txt', 'all-followings.txt')
    # diffs = [diff.strip() for diff in diffs]

    diffs = set(all_followings) - set(all_followers)

    write_to_file(list(diffs), "not-following-back")

    print("Rate = ", check_rate_limit())


if __name__ == "__main__":
    main()
