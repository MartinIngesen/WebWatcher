import requests, sys, hashlib, time, smtplib, yaml, datetime

config = yaml.safe_load(open("config.yml"))

if len(sys.argv) < 2:
    print "[!] Need to supply a file with urls to watch."
    print "[!] Example: python webwatcher.py /path/to/file.txt"
    sys.exit()

def sendmail(url):
    datet = datetime.datetime.now().time()
    datestring = "%s:%s" % (str(datet.hour), str(datet.minute))

    FROM = config['username']
    TO  = config['recipients']
    SUBJECT = config['subject'] % datestring
    BODY = "There was a change in the url " + url + " at " + datestring
    MESSAGE = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (FROM, TO, SUBJECT, BODY)

    username = config['username']
    password = config['password']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(FROM, TO, MESSAGE)
    server.quit()

# READ FILE
print "[+] Reading file"
urls = []

with open(sys.argv[1], 'r') as fil:
    urls = fil.read().strip().split("\n")


# PREPROCESS HASHES
print "[+] Preprocessing hashes"
hashes = []

for url in urls:
    print "    [-] " + url
    r = requests.get(url, cookies=config["cookies"]).text
    print r
    hashes.append(hashlib.md5(r).hexdigest())

# START LOOKING FOR CHANGES
print "[*] Looking for changes"
while 1:
    for index, url in enumerate(urls):
        r = requests.get(url, cookies=config["cookies"]).text
        hasj = hashlib.md5(r).hexdigest()
        if hasj != hashes[index]:
            # SHIT BANDIT SEND AN EMAIL
            #sendmail(url)
            print "[!] We noted a change in the url " + url
            hashes[index] = hasj

    time.sleep(30)
