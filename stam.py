import requests
import os


LIME_TOKEN="lmwr_sk_B1dZNDhRx5_EhenL3JOjBmia9W1uyynseQ6j6UEADeoXjGSc"


def generate_image_request(prompt: str, aspect_ratio='1:1'):
    pre_prompt = ''
    url = "https://api.limewire.com/api/image/generation"
    payload = {
        "prompt": f"{pre_prompt} {prompt}",
        "aspect_ratio": aspect_ratio
    }

    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {LIME_TOKEN}",
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data


print(generate_image_request("pink lion with a big pig head"))
