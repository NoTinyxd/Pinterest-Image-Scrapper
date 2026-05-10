import os
import hashlib
import requests
import time
from urllib.parse import quote
from colorama import Fore, Style, init
from playwright.sync_api import sync_playwright

init(autoreset=True)

query = input(f"{Fore.GREEN}[ + ]{Style.RESET_ALL} - Input: ").strip()
url = f"https://www.pinterest.com/search/pins/?q={quote(query)}&rs=typed"

os.makedirs("pfp", exist_ok=True)

seen = set()
counter = {"saved": 0}
start = time.time()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    def handle_route(route, request):
        if request.resource_type == "image":
            img_url = request.url
            if img_url not in seen:
                seen.add(img_url)
                try:
                    r = requests.get(img_url, timeout=10)
                    if r.status_code == 200:
                        name = hashlib.md5(img_url.encode()).hexdigest() + ".jpg"
                        with open(os.path.join("pfp", name), "wb") as f:
                            f.write(r.content)
                        counter["saved"] += 1
                        print(f"{Fore.CYAN}[ + ]{Style.RESET_ALL} Saved: {name}")
                except:
                    pass
        route.continue_()

    page.route("**/*", handle_route)

    try:
        page.goto(url)
    except:
        pass

    input()

elapsed = round(time.time() - start, 1)
print(f"{Fore.GREEN}[ + ]{Style.RESET_ALL} GOT {counter['saved']} Images! , took : {elapsed}s")
