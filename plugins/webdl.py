import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from Haji.helpers import CMD

__MODULES__ = "Webdl"
__HELP__ = """
<blockquote>⪼ **--Command help Webdl--**</blockquote>

<blockquote>**Download html code**</blockquote>
**ᐉ Keterangan: Dapatkan kode html dari url**
ᐈ Perintah: `{0}webdl` (url)

<b>   {1}</b>
"""


def download_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return (
                f"Failed to download source code. Status code: {response.status_code}"
            )

    except Exception as e:
        return f"An error occurred: {str(e)}"


@CMD.UBOT("webdl")
async def _(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "**Please enter a URL along with the /webdl command.**"
        )
        return

    url = message.command[1]

    source_code = download_website(url)
    if source_code.startswith("An error occurred") or source_code.startswith(
        "Failed to download"
    ):
        return await message.reply_text(source_code)
    else:
        with open("website.txt", "w", encoding="utf-8") as file:
            file.write(source_code)
        return await message.reply_document(
            document="website.txt", caption=f"**Source code of {url}**"
        )
