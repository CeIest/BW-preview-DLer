__author__      = "Celest"
import urllib.request
import requests
import click
import json
import os


########## RETRIEVING GENERAL METADATA ##########

click.secho(f"\nBook ID?", fg="green")
Cid = input(">>")[2:] # To replace with click stuff whenever I got time

# retrieving JSON data from requested preview
Cid_Url = urllib.request.urlopen("https://viewer-trial.bookwalker.jp/trial-page/c?cid="+Cid+"&BID=0")
# Loading JSON data of the page
Data = json.loads(Cid_Url.read())

# Reading values from JSON data
Status = Data['status']


if Status == "200":

    Base_URL = Data['url']
    Book_Name = Data['cti']
    Lp = Data['lp']
    Cty = Data['cty']
    Lin = Data['lin']
    Lpd = Data['lpd']
    Bs = Data['bs']
    Auth_info = Data['auth_info']
    Pfcd = Auth_info['pfCd']
    Policy = Auth_info['Policy']
    Signature = Auth_info['Signature']
    Key_Pair_Id = Auth_info['Key-Pair-Id']

    click.secho(f"\nDownloading {Book_Name}'s preview files...", fg="green")
    click.secho(f"---------------------------------------", fg="bright_cyan")

    # Creating authentification string
    Auth_String = '?pfCd='+Pfcd+'&Policy='+Policy+'&Signature='+Signature+'&Key-Pair-Id='+Key_Pair_Id


    # Creating book path
    Book_Path = "Preview "+Book_Name
    os.makedirs(Book_Path, exist_ok=True)


    # If LN = 0. If Manga = 1.
    if Cty == 0:
        Base_URL= Base_URL+"normal_default/"


    ########## RETRIEVING PREVIEW METADATA ##########

    # Retrieving the book's metadata and download it
    Metadata_Link = Base_URL+"configuration_pack.json"+Auth_String
    urllib.request.urlretrieve(Metadata_Link, Book_Path+"/metadata.json")

    #To-do: Save more metadata stuff in the future


    ########## RETRIEVING PREVIEW METADATA ##########

    # Creating chapters path
    Chapters_Path = Book_Path+"/Chapters"
    os.makedirs(Chapters_Path, exist_ok=True)

    # Creating pages path
    Pages_Path = Book_Path+"/Pages"
    os.makedirs(Pages_Path, exist_ok=True)


    # ##Explaining the concept:
    # In the JSON file;
    # "configuration"."contents" contains a list of all the chapter paths which are in the "file" value each
    # All the chapters are their own values inside the JSON file, each of them contain a "pagecount" value
    # exemple: "item/xhtml/p-002.xhtml"."FileLinkInfo"."PageCount": 13


    # Re-calling the metadata link for now because if I load the JSON file it returns reading errors                              
    Book_Metadata = urllib.request.urlopen(Metadata_Link)
    Book_Metadata = json.loads(Book_Metadata.read())

    # Reading the "configuration"."contents"
    Meta_Contents = Book_Metadata['configuration']['contents']

    Pages_Count_Name = 0

    # Doing the process for each Chapters ("contents")
    for d in Meta_Contents:

        Key_Name = d['file']

        Page_Count = Book_Metadata[Key_Name]['FileLinkInfo']['PageCount']

        for i in range(Page_Count):
            click.secho(f"Downloading "+os.path.basename(Key_Name)+" page "+str(i), fg="white")
            Page_URL = Base_URL+Key_Name+"/"+str(i)+".jpeg"+Auth_String
            Pages_Count_Name += 1


    # Saving the pages. Doing it in a weird process because BookWalker blocks some kind of script scraping
            Save = requests.get(Page_URL)

            Chapters_Name = os.path.basename(d['file'])
            Save_Path = Chapters_Path+"/"+Chapters_Name
            os.makedirs(Save_Path, exist_ok=True)
            with open(Save_Path+"/"+str(i)+".jpg", 'wb') as outfile:
                outfile.write(Save.content)


            Save_Pages_Path = Pages_Path+"/"
            os.makedirs(Save_Pages_Path, exist_ok=True)
            with open(Save_Pages_Path+"/"+str(Pages_Count_Name)+".jpg", 'wb') as outfile:
                outfile.write(Save.content)

    click.secho(f"---------------------------------------", fg="bright_cyan")
    click.secho(f"Download finished.", fg="green")

else:
    click.secho(f"\nWrong book ID, or the preview isn't released yet.\nMake sure your ID looks like this:\nde5bddb97a-1848-469f-bd3d-c0b926b8cbd3", fg="red")
