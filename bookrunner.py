__author__      = "Celest"
import requests
import urllib.request
import json
import os


cid = input("BookWalker book ID?\n>>")[2:]


########## RETRIEVING GENERAL METADATA ##########

# retrieving JSON data from requested preview
url = "https://viewer-trial.bookwalker.jp/trial-page/c?cid="+cid+"&BID=0"
response = urllib.request.urlopen(url)
# Loading JSON data of the page
data = json.loads(response.read())

# Reading values from JSON data
status = data['status']


if status == "200":

    baseURL = data['url']
    bookName = data['cti']
    lp = data['lp']
    cty = data['cty']
    lin = data['lin']
    lpd = data['lpd']
    lin = data['bs']
    auth_info = data['auth_info']
    pfcd = auth_info['pfCd']
    policy = auth_info['Policy']
    signature = auth_info['Signature']
    KeyPairId = auth_info['Key-Pair-Id']

    print(f"Downloading {bookName}'s preview files...")
    print("------------------------")

    # Creating authentification string
    authString = '?pfCd='+pfcd+'&Policy='+policy+'&Signature='+signature+'&Key-Pair-Id='+KeyPairId


    # Creating book path
    bookPath = "Preview "+bookName
    os.makedirs(bookPath, exist_ok=True)


    # If LN = 0. If Manga = 1.
    if cty == 0:
        baseURL= baseURL+"normal_default/"


    ########## RETRIEVING PREVIEW METADATA ##########

    # Retrieving the book's metadata and download it
    MetadataLink = baseURL+"configuration_pack.json"+authString
    urllib.request.urlretrieve(MetadataLink, bookPath+"/metadata.json")

    #To-do: Save more metadata stuff in the future

    # Write the book ID in a file
    with open(bookPath+"/de"+cid, 'wb') as BookIDWrite:
        pass

    ########## RETRIEVING PREVIEW METADATA ##########

    # Creating chapters path
    ChaptersPath = bookPath+"/Chapters"
    os.makedirs(ChaptersPath, exist_ok=True)

    # Creating pages path
    PagesPath = bookPath+"/Pages"
    os.makedirs(PagesPath, exist_ok=True)


    # ##Explaining the concept:
    # In the JSON file;
    # "configuration"."contents" contains a list of all the chapter paths which are in the "file" value each
    # All the chapters are their own values inside the JSON file, each of them contain a "pagecount" value
    # exemple: "item/xhtml/p-002.xhtml"."FileLinkInfo"."PageCount": 13


    # Re-calling the metadata link for now because if I load the JSON file it returns reading errors                              
    BookMetadata = urllib.request.urlopen(MetadataLink)
    BookMetadata = json.loads(BookMetadata.read())

    # Reading the "configuration"."contents"
    MetaContents = BookMetadata['configuration']['contents']

    PagesCountName = 0

    # Doing the process for each Chapters ("contents")
    for d in MetaContents:

        keyName = d['file']

        PageCount = BookMetadata[keyName]['FileLinkInfo']['PageCount']

        for i in range(PageCount):
            PageShow = PageCount + 1
            print("Downloading "+os.path.basename(keyName)+" page "+str(i))
            pageURL = baseURL+keyName+"/"+str(i)+".jpeg"+authString
            PagesCountName += 1


    # Saving the pages. Doing it in a weird process because BookWalker blocks some kind of script scraping
            Save = requests.get(pageURL)

            chaptersName = os.path.basename(d['file'])
            SavePath = ChaptersPath+"/"+chaptersName
            os.makedirs(SavePath, exist_ok=True)
            with open(SavePath+"/"+str(i)+".jpg", 'wb') as outfile:
                outfile.write(Save.content)


            SavePagesPath = PagesPath+"/"
            os.makedirs(SavePagesPath, exist_ok=True)
            with open(SavePagesPath+"/"+str(PagesCountName)+".jpg", 'wb') as outfile:
                outfile.write(Save.content)

    print("------------------------")
    print("Download finished.")

else:
    print("\nWrong book ID, or the preview isn't released yet.\nMake sure your ID looks like this:\nde5bddb97a-1848-469f-bd3d-c0b926b8cbd3")
