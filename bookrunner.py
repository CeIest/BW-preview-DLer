__author__ = "Celest"
import requests
import click
import json
import sys
import os
import re


def gethdcoverlink(cover_buid):
    cover_response = requests.get(f"https://bookwalker.jp/{cover_buid}")
    cover_str = re.search(r'<meta property="og:image" content="https://c.bookwalker.jp/(\d+)/t_700x780.jpg">', cover_response.text).group(1)
    hdcover_url = f"https://c.bookwalker.jp/coverImage_{str(int(str(cover_str)[::-1]) - 1)}.jpg"
    return hdcover_url




if len(sys.argv) > 1:
    buid = sys.argv[1]
else:
    buid = input("Book ID?\n>>")


if buid.startswith("de") and len(buid) == 38:
    cover_buid = buid
    buid = buid[2:]
else:
    cover_buid = f"de{buid}"
hdcoverlink = gethdcoverlink(cover_buid)


BID_response = requests.get(f"https://viewer-trial.bookwalker.jp/trial-page/c?cid={buid}&BID=0")
BID_data = json.loads(BID_response.content)


if BID_data["status"] != "200":
    click.secho(f"\nWrong book ID, or the preview isn't released yet.", fg="red")
    if len(requests.get(hdcoverlink).content) < 32050: # 32050 is "NOW PRINTING"'s cover filesize
        print(hdcoverlink)
    exit()



base_URL = BID_data["url"]

bookname = BID_data["cti"]
bookname = re.sub(':',  '：', bookname)
bookname = re.sub('/',  '／', bookname)



click.secho(f"\nDownloading {bookname}'s preview files...", fg="green")
click.secho(f"---------------------------------------", fg="bright_cyan")


authinfo = BID_data["auth_info"]
authstring = f'?pfCd={authinfo["pfCd"]}&Policy={authinfo["Policy"]}&Signature={authinfo["Signature"]}&Key-Pair-Id={authinfo["Key-Pair-Id"]}'

bookpath = f"Books/Preview {bookname}"
os.makedirs(bookpath, exist_ok=True)



if BID_data["cty"] == 0:    # If LN = 0. If Manga = 1.
    base_URL = f"{base_URL}normal_default/"




# Downloads metadata
click.secho(f"Downloading metadata", fg="white")

metadata_link = f"{base_URL}configuration_pack.json{authstring}"

meta_response = requests.get(metadata_link)
book_metadata = json.loads(meta_response.content)

with open(f"{bookpath}/metadata.json", 'wb') as md:
    md.write(json.dumps(book_metadata, ensure_ascii=False, indent=2).encode("utf8"))


# Downloads HD cover
click.secho(f"Downloading HD cover", fg="white")
with open(f"{bookpath}/Cover.jpg", "wb") as cf:
    cf.write(requests.get(hdcoverlink).content)
    






pagespath = f"{bookpath}/Pages"
os.makedirs(pagespath, exist_ok=True)


d_count = 1
for d in book_metadata["configuration"]["contents"]:

    keyname = d["file"]

    for i in range(book_metadata[keyname]["FileLinkInfo"]["PageCount"]):

        click.secho(f"Downloading {os.path.basename(keyname)}    as Page {i + 1}", fg="white")

        page_response = requests.get(f"{base_URL}{keyname}/{i}.jpeg{authstring}")

        with open(f"{pagespath}/i-{d_count:03d}.jpg", "wb") as pf:
            pf.write(page_response.content)
        d_count += 1

    
click.secho(f"---------------------------------------", fg="bright_cyan")
click.secho(f"Download finished.", fg="green")
