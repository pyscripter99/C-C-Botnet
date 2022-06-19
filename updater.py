import os
import requests

print("Checking version...")
if os.path.exists("version.txt"):
    ver = ""
    with open("version.txt", "r") as f:
        ver = f.read()
    if ver == requests.get("https://raw.githubusercontent.com/pyscripter99/C-C-Botnet/main/version.txt").text:
        print("Same version")
    else:
        print("Updating...")
        repo = "https://github.com/pyscripter99/C-C-Botnet/archive/refs/heads/main.zip"
        r = requests.get(repo, allow_redirects=True)
        with open("update.zip", "wb") as f:
            f.write(r.content)

        import zipfile

        zipfile.ZipFile("update.zip").extractall()
        print("Checking version...")
        if os.path.exists("C-C-Botnet-main\\version.txt"):
            ver = ""
            with open("C-C-Botnet-main\\version.txt", "r") as f:
                ver = f.read()
            if ver == requests.get("https://raw.githubusercontent.com/pyscripter99/C-C-Botnet/main/version.txt").text:
                print("Same version")
            else:
                print("COULD NOT VERIFY VERISION, PLEASE CHECK GITHUB REPO FOR MANUAL UPDATE!!!!")
        else:
            print("No version file found!")

        input("PLEASE MOVE THE FILES FROM C-C-Botnet-main TO THIS DIR, THEN RESTART THE SERVER")
else:
    print("No version file found!")

