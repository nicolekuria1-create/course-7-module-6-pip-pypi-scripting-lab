from lib.generate_log import generate_log
import requests


def fetch_data():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1", timeout=10
    )
    if response.status_code == 200:
        return response.json()
    return {}


if __name__ == "__main__":
    log_data = ["User logged in", "User updated profile", "Report exported"]
    filename = generate_log(log_data)

    post = fetch_data()
    with open("api_post_title.txt", "w", encoding="utf-8") as file:
        file.write(post.get("title", "No title found"))

    print(f"Log generated in {filename}")
    print("Fetched Post Title:", post.get("title", "No title found"))
    print("API output written to api_post_title.txt")
