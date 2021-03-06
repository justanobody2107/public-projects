#Import dependencies
import os, json, sys, random, re, time

#Check for dependencies
try:
    from tqdm import tqdm
except Exception:
    os.system("python3 -m pip install tqdm")
    from tqdm import tqdm
try:
    import requests
except Exception:
    os.system("python3 -m pip install requests")
    import requests
try:
    import zipfile
except Exception:
    os.system("python3 -m pip install zipfile")
    import zipfile

#Set defaults and version
imgtype = "sfw"
amount = 1
apiurl = ["https://nekos.life/api/v2/img/neko"]
version = "v1.2.6"
updated = False

#Update checker
def update():
    print("Checking for updates...")
    newversion = str(requests.get("https://raw.githubusercontent.com/justanobody2107/public-projects/main/nekodl/config/latestversion.txt").content)
    newver = [int(newver) for newver in re.findall(r'\d+', newversion)]
    oldver = re.sub('v', "", version)
    num1 = int(oldver.split('.')[0])
    num2 = int(oldver.split('.')[1])
    num3 = int(oldver.split('.')[2])
    newnum1 = newver[0]
    newnum2 = newver[1]
    newnum3 = newver[2]
    if num1 < newnum1 or num2 < newnum2 or num3 < newnum3:
        while True:
            updateans = input("Update found! Do you want to update?(y/n) ")
            if updateans == "y":
                print("Updating...")
                os.system("curl -so update.py https://raw.githubusercontent.com/justanobody2107/public-projects/main/nekodl/nekodl.py")
                if os.path.exists("update.py"):
                    os.remove("nekodl.py")
                    os.rename("update.py", "nekodl.py")
                    print("Updated.")
                    break
                else:
                    print("\033[0;31m[ERROR]: Failed to update\033[0m")
                    break
            elif updateans == "n":
                print("Ok, won't update.")
                while True:
                    askans = input("Ask to update next time?(y/n) ")
                    if askans == "y":
                        print("Ok, will ask again next time.")
                        with open(configfile) as f:
                            data = json.load(f)
                            savedir = data['savedir']
                            asktozip = data['asktozip']
                            askupdate = "y"
                        writetojson = {'savedir':savedir,'asktozip':asktozip, 'askupdate':askupdate}
                        with open(configfile, 'w') as f:
                            json.dump(writetojson, f, indent=2)
                        break
                    elif askans == "n":
                        print("Ok, won't ask next time.")
                        with open(configfile) as f:
                            data = json.load(f)
                            savedir = data['savedir']
                            asktozip = data['asktozip']
                            askupdate = "n"
                        writetojson = {'savedir':savedir,'asktozip':asktozip, 'askupdate':askupdate}
                        with open(configfile, 'w') as f:
                            json.dump(writetojson, f, indent=2)
                        break
                break
    else:
        print("No updates available.")   

#Reinstall (will only run when --reinstall tag attached)
def reinstall():
    print("Reinstalling")
    os.system("curl -so update.py https://raw.githubusercontent.com/justanobody2107/public-projects/main/nekodl/nekodl.py")
    if os.path.exists("update.py"):
        os.remove("nekodl.py")
        os.rename("update.py", "nekodl.py")
        print("Reinstalled.")
    else:
        print("\033[0;31m[ERROR]: Failed to reinstall\033[0m")

#Setup (will only run when --config tag attached)
def setup():
    if os.path.exists(configfile):
        os.remove(configfile)
    savedir = input("Where should I save the nekos? ")
    print("Saving to "+savedir)
    while True:
        asktozip = input("Should I ask you to zip the files at the end?(y/n) ")
        if asktozip == "y":
            print("Will ask to zip later :)")
            break
        elif asktozip == "n":
            print("Will never ask to zip again :(")
            break
    while True:
        askupdate = input("Should I ask to update, if there's an update, when the script is run?(y/n) ")
        if askupdate == "y":
            print("Will ask to update")
            break
        elif askupdate == "n":
            print("Will never ask to update again")
            break
    while True:
        defaultsfw = input("What is your preferred default sfw status?(s/n/g) ")
        if defaultsfw == "s":
            print("Will default to sfw.")
            break
        elif defaultsfw == "n":
            print("Will default to nsfw.")
            break
        elif defaultsfw == "g":
            print("Will default to gif.")
            break
    while True:
        defaultamount = int(input("What is your preferred default image count? "))
        if defaultamount != None:
            print("Will default to "+str(defaultamount)+" images")
            break
    writetojson = {'savedir':savedir,'asktozip':asktozip, 'askupdate':askupdate, 'sfw':defaultsfw, 'amount':defaultamount}
    with open(configfile, 'w') as f:
        json.dump(writetojson, f, indent=2)

#Check for setups and save args
args = sys.argv[1:]
if not os.path.isdir("nekodlconfig"):
    os.makedirs("nekodlconfig")
configdir = os.path.join(os.getcwd(), "nekodlconfig")
configfile = os.path.join(configdir, "config.json")
if os.path.exists("config.json"):
    os.rename("config.json", configfile)
if not os.path.exists(configfile):
    while True:
        createsetup = input("Want to create a config (this appears on first time run)?(y/n) ")
        if createsetup == "y":
            print("Starting setup")
            setup()
            break
        elif createsetup == "n":
            print("It's important to create a config file. Please rethink your decision")

#Config parser
with open(configfile) as config:
    while True:
        data = json.load(config)
        try:
            zip = data['asktozip']
            dir = data['savedir']
            chkupd = data['askupdate']
            defaulttype = data['sfw']
            if defaulttype == "n":
                imgtype = "nsfw"
            elif defaulttype == "s":
                imgtype == "sfw"
            elif defaulttype == "g":
                imgtype == "gif"
            amount = data['amount']
            break
        except Exception:
            print("Config is outdated, starting configuration.")
            config.close()
            setup()
            config = open(configfile)


#Check for config arg
if "--config" in args or "-c" in args:
    setup()
    imgtype = None

#Check for help arg
if "--help" in args or "-h" in args:
    print("NekoDL "+version+" - JustANobody#2107")
    print("--help      | -h      Displays this message")
    print("--config    | -c      Asks for configuration")
    print("--nsfw      | -n      Downloads nsfw image")
    print("--sfw       | -s      Downloads sfw image (default)")
    print("--gif       | -g      Downloads gif image")
    print("--batch     | -b      Downloads batch of images")
    print("--quick     | -q      Downloads/uses url map (quicker)")
    print("--update    | -u      Checks for updates")
    print("--reinstall | -r      Reinstalls script")
    imgtype = None

#Check for nsfw
if "--nsfw" in args or "-n" in args:
    imgtype = "nsfw"
if imgtype == "nsfw":
    apiurl=["https://nekos.life/api/v2/img/cum_jpg", "https://nekos.life/api/v2/img/lewd", "https://nekos.life/api/v2/img/pussy_jpg", "https://nekos.life/api/v2/img/lewdk", "https://nekos.life/api/v2/img/erokemo", "https://nekos.life/api/v2/img/blowjob", "https://nekos.life/api/v2/img/lewdkemo", "https://nekos.life/api/v2/img/tits", "https://nekos.life/api/v2/img/eroyuri", "https://nekos.life/api/v2/img/yuri", "https://nekos.life/api/v2/img/hentai"]

#Check for sfw
if "--sfw" in args or "-s" in args:
    imgtype = "sfw"
if imgtype == "sfw":
    apiurl = ["https://nekos.life/api/v2/img/neko"]

#Check for gif
if "--gif" in args or "-g" in args:
    imgtype = "gif"
if imgtype == "gif":
    apiurl=["https://nekos.life/api/v2/img/feetg", "https://nekos.life/api/v2/img/cum", "https://nekos.life/api/v2/img/bj", "https://nekos.life/api/v2/img/spank", "https://nekos.life/api/v2/img/solog", "https://nekos.life/api/v2/img/Random_hentai_gif", "https://nekos.life/api/v2/img/pussy", "https://nekos.life/api/v2/img/pwankg", "https://nekos.life/api/v2/img/nsfw_neko_gif"]

#Check for batch download
if "--batch" in args or "-b" in args:
    amount = int(input("How many images do you want to save? "))

#Check for urlmap tag
useurlmap = False
if "--quick" in args or "-q" in args:
    useurlmap = True
    print("Using url maps.")
    
#Check for urlmaps
if useurlmap == True:
    sfwurlmap = os.path.join(configdir, "sfw.txt")
    nsfwurlmap = os.path.join(configdir, "nsfw.txt")
    gifurlmap = os.path.join(configdir, "gif.txt")
    if not os.path.exists(sfwurlmap):
        os.system("curl -so "+sfwurlmap+" "+"https://raw.githubusercontent.com/justanobody2107/public-projects/main/sfw.txt")
    if not os.path.exists(nsfwurlmap):
        os.system("curl -so "+nsfwurlmap+" "+"https://raw.githubusercontent.com/justanobody2107/public-projects/main/nsfw.txt")
    if not os.path.exists(gifurlmap):
        os.system("curl -so "+gifurlmap+" "+"https://raw.githubusercontent.com/justanobody2107/public-projects/main/gif.txt")

#Check for update
if "--update" in args or "-u" in args:
    update()
    updated = True
    imgtype = None

#Check for reinstall
if "--reinstall" in args or "-r" in args:
    reinstall()
    updated = True
    imgtype = None

#Make/set directory
pathsfw = os.path.join(dir, 'sfw')
pathnsfw = os.path.join(dir, 'nsfw')
pathgif = os.path.join(dir, "gif")
if not os.path.isdir(dir):
    os.makedirs(dir)
if not os.path.isdir(pathsfw):
    os.makedirs(pathsfw)
if not os.path.isdir(pathnsfw):
    os.makedirs(pathnsfw)
if not os.path.isdir(pathgif):
    os.makedirs(pathgif)

#Download script
i = 0
badfile = 0
if imgtype != None:
    pbar = tqdm(total=amount, ascii = True, colour="green")
    if useurlmap == False:
        while i < amount:
            if badfile == amount:
                pbar.close()
                print("\033[0;31m[ERROR]: All of the pictures were duplicates or had bad formatting\033[0m")
                badfile = 0
                break
            randapiurl = random.choice(apiurl)
            apiworks = False
            while True:
                try:
                    randapicontent = requests.get(randapiurl)
                    break
                except Exception:
                    randapiurl = random.choice(apiurl)
            data = json.loads(randapicontent.content)
            url = data['url']
            if url.find('/'):
                imagename = url.rsplit('/', 1)[1]
            if imgtype == "nsfw":
                imagepath = os.path.join(pathnsfw,imagename)
                if not os.path.exists(imagepath):
                    os.system("curl -so "+pathnsfw+"/"+imagename+" "+url)
                    i = i + 1
                    pbar.update(1)
                else:
                    badfile = badfile+1
            elif imgtype == "sfw":
                imagepath = os.path.join(pathsfw,imagename)
                if not os.path.exists(imagepath):
                    os.system("curl -so "+pathsfw+"/"+imagename+" "+url)
                    i = i + 1
                    pbar.update(1)
                else:
                    badfile = badfile+1
            elif imgtype == "gif":
                imagepath = os.path.join(pathgif,imagename)
                if not os.path.exists(imagepath):
                    os.system("curl -so "+pathgif+"/"+imagename+" "+url)
                    i = i + 1
                    pbar.update(1)
                else:
                    badfile = badfile+1
    else:
        while i < amount:
            if imgtype == "nsfw":
                with open(nsfwurlmap) as f:
                    file = str(f.read())
                    urls = file.split("\n")
                if badfile == len(urls)-1:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
                if amount-badfile > len(urls)-1:
                    amount = len(urls)-1
                    pbar.close()
                    print("Updating count...")
                    pbar = tqdm(total=amount, ascii = True, colour="green")
                try:
                    if urls[i].find('/'):
                        imagename = urls[i].rsplit('/', 1)[1]
                    url = urls[i]
                    imagepath = os.path.join(pathnsfw,imagename)
                    if not os.path.exists(imagepath):
                        os.system("curl -so "+pathnsfw+"/"+imagename+" "+url)
                        i = i + 1
                        pbar.update(1)
                    else:
                        badfile = badfile + 1
                        i = i + 1
                        amount = amount + 1
                except Exception:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
            elif imgtype == "sfw":
                with open(sfwurlmap) as f:
                    file = str(f.read())
                    urls = file.split("\n")
                if badfile == len(urls)-1:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
                if amount-badfile > len(urls)-1:
                    amount = len(urls)-1
                    pbar.close()
                    print("Updating count...")
                    pbar = tqdm(total=amount, ascii = True, colour="green")
                try:
                    if urls[i].find('/'):
                        imagename = urls[i].rsplit('/', 1)[1]
                    url = urls[i]
                    imagepath = os.path.join(pathsfw,imagename)
                    if not os.path.exists(imagepath):
                        os.system("curl -so "+pathsfw+"/"+imagename+" "+url)
                        i = i + 1
                        pbar.update(1)
                    else:
                        badfile = badfile + 1
                        i = i + 1
                        amount = amount + 1
                except Exception:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
            elif imgtype == "gif":
                with open(gifurlmap) as f:
                    file = str(f.read())
                    urls = file.split("\n")
                if badfile == len(urls)-1:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
                if amount-badfile > len(urls)-1:
                    amount = len(urls)-1
                    pbar.close()
                    print("Updating count...")
                    pbar = tqdm(total=amount, ascii = True, colour="green")
                try:
                    if urls[i].find('/'):
                        imagename = urls[i].rsplit('/', 1)[1]
                    url = urls[i]
                    imagepath = os.path.join(pathgif,imagename)
                    if not os.path.exists(imagepath):
                        os.system("curl -so "+pathgif+"/"+imagename+" "+url)
                        i = i + 1
                        pbar.update(1)
                    else:
                        badfile = badfile + 1
                        i = i + 1
                        amount = amount + 1
                except Exception:
                    pbar.close()
                    print("\033[0;31m[ERROR]: Some or all of the pictures were duplicates\033[0m")
                    badfile = 0
                    break
    pbar.close()

#Zip script
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

#Ask to zip
zipped = False
if zip == "y" and imgtype != None:
    while True: 
        prompt = input("Zip up files?(y/n) ")
        if prompt == "y":
            print("Zipping files...")
            zipf = zipfile.ZipFile('nekos.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir(dir, zipf)
            zipf.close()
            print("Zip created at \033[0;36m"+os.getcwd()+"\033[0m with filename \033[0;36mnekos.zip\033[0m")
            break
        elif prompt == "n":
            print("Alright, won't zip files")
            break

#Update
if chkupd == "y" and updated == False:
    update()
