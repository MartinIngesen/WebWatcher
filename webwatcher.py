import requests, sys, hashlib, time, smtplib, yaml, datetime

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

config = yaml.safe_load(open("config.yml"))
SLEEP_TIME = 30

if len(sys.argv) < 2:
    print("[!] Need to supply a file with urls to watch.")
    print("[!] Example: python webwatcher.py /path/to/file.txt")
    sys.exit()

def sendmail(url):
    datet = datetime.datetime.now().time()
    datestring = "{}:{}".format(str(datet.hour), str(datet.minute))

    FROM = config['username']
    TO  = config['recipients']
    SUBJECT = config['subject'] % datestring
    BODY = "There was a change in the url {} at {}".format(url, datestring)
    MESSAGE = "FROM: {}\nTo: {}\nSubject: {}\n\n{}".format(FROM, TO SUBJECT, BODY)

    username = config['username']
    password = config['password']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(FROM, TO, MESSAGE)
    server.quit()

# READ FILE
print("[+] Reading file")
urls = []

with open(sys.argv[1], 'r') as fil:
    urls = fil.read().strip().split("\n")

# PREPROCESS HASHES
print("[+] Preprocessing hashes")
hashes = []

for url in urls:
    print("\t[-] {}".format(url))
    r = requests.get(url, cookies=config["cookies"]).text
    hashes.append(hashlib.md5(r).hexdigest())

# START LOOKING FOR CHANGES
print("[*] Looking for changes")
while True:
    for index, url in enumerate(urls):
        r = requests.get(url, cookies=config["cookies"]).text
        hash = hashlib.md5(r).hexdigest()
        if hash != hashes[index]:
            # Detected a change, sending mail
            sendmail(url)
            print("[!] We noted a change in the url {}".format(url))
            hashes[index] = hash

    time.sleep(SLEEP_TIME)
