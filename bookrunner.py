__author__ = "Celest"
import requests
import os
import urllib.request
import json
import click


@click.command()
@click.option(
    "--id", "--ID", "-id", "-ID",
    prompt="ID of the series?\n>>",
    help="ID of the Booklive series",
)
def bookdead(id):
    click.secho(f"---------------------------------------", fg="bright_cyan")

    covernum = '001'
    covernum.zfill(3)

    a = requests.get('https://res.booklive.jp/' + id + '/' + covernum + '/thumbnail/X.jpg')

    bookname = urllib.request.urlopen(
        'https://booklive.jp/json/recommend-watch?title_id=' + id 
    )
    Data = json.loads(bookname.read())
    idkhowtonamethisone = Data['title_info']
    bookname = idkhowtonamethisone['title_name']

    while True:
        while a.status_code == 200:
            a = requests.get('https://res.booklive.jp/' + id + '/' + covernum + '/thumbnail/X.jpg')
            if a.status_code == 200:
                click.secho(f'Downloading cover n°' + covernum + ' of "' + bookname + '"', fg="green")

                path = 'Covers of ' + bookname
                os.makedirs(path, exist_ok=True)
                with open(path + '/' + covernum + '.jpg', 'wb') as outfile:
                    outfile.write(a.content)

                covernum = int(covernum) + 1
                covernum = str(covernum)
                covernum  = covernum.zfill(3)

        else:
            click.secho(f"---------------------------------------", fg="bright_cyan")
            click.secho(f'Download finished.')
            break
            #figure out when to stop lmao code 200 doesn't work but oh well, as long as we get the covers

if __name__ == '__main__':
    bookdead()
