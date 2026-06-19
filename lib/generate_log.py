from datetime import datetime
import os

def generate_log(data):
    if not isinstance(data, list):
        raise ValueError("Input data must be a list.")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w", encoding="utf-8") as file:
        for entry in data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename
