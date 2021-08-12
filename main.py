# developed by novuh (github.com/n0vuh)
# AntiZon is intended for the purpose of getting a consumer a better price for a product.
# AntiZon is not intended to be used as financial advice.


# source code, p.s: ignore lazy code, it'll be fixed
import json
import os

from colorama import Back, Fore, Style
from src.utils.console import clear, title, tags
from src.amzn.item import AMZN
from src.gogl.find import SERP, process

def query_loop(amzn: AMZN, serp: SERP):
    query = input(tags.default + "Amazon Product ASIN >> ")
    print(tags.default + f"Searching Amazon for '{query}'...")
    amazon_data = amzn.get_item(query)
    try:
        amzn_value = amazon_data.value
        amzn_title = amazon_data.name
        print(tags.okay + "Found a result!")
    except AttributeError:
        print(tags.error + str(amazon_data["message"]))
        query_loop(amzn, serp)
    print(tags.default + f"Searching Google for '{amzn_title}'...")
    try:
        r = process(serp.get(amzn_title))
        print(tags.okay + f"Found {len(r['extracted'])} result(s)!")
    except Exception as e:
        print(tags.error + f"Error occured while searching Google: {e}")
        query_loop(amzn, serp)
    print(tags.default + "Processing retrieved data...")

    cheaper = []
    for res in r["extracted"]:
        if res["price"] < amzn_value:
            cheaper.append(
                {
                    "price": res["price"],
                    "source": res["supplier"],
                    "link": res["link"]
                }
            )
    
    print(tags.okay + f"Found {len(cheaper)} cheaper listings!")
    print(tags.default + "Writing...")
    with open("output.txt", "a") as fp:
        for res in cheaper:
            fp.write(f"${res['price']} | {res['link']} | {res['source']}\n")

    print(tags.okay + "Done! You can view the results inside output.txt.")
    input(Fore.BLACK + Style.BRIGHT + "Press ENTER to quit.")
    exit()

def main():
    clear()

    # title stuff
    title("AntiZon by novuh")
    length = os.get_terminal_size().columns
    print(Style.BRIGHT + Fore.WHITE + Back.YELLOW + "AntiZon by github.com/n0vuh".center(length, " ") + Back.RESET + "\n")

    # load config file
    print(Back.RESET + tags.default + "Loading config file...")
    cfg = json.load(open("src/resources/config.json", "r"))

    # check to see if config has any data, if not, require user to give required data
    dump = False
    if cfg["serpkey"] == "":
        print(tags.error + "You do not have a SerpAPI key! Get one @ serpapi.com")
        serp_key = input(tags.default + "SerpAPI Key >> ")
        dump = True

    if cfg["amznkey"] == "":
        print(tags.error + "You do not have a Rainforest key! Get one @ rainforestapi.com")
        amzn_key = input(tags.default + "Rainforest Key >> ")
        dump = True

    if dump:
        json.dump({"serpkey": serp_key, "amznkey": amzn_key}, open("src/resources/config.json", "w"))
        main()
    
    # setup api classes
    amzn = AMZN(cfg["amznkey"])
    serp = SERP(cfg["serpkey"])

    # search loop
    query_loop(amzn, serp)



if __name__ == "__main__":
    main()
