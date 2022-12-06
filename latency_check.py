import subprocess
import re
import sqlite3
from datetime import datetime

server = "www.google.com"
request_time = datetime.now()
ping_result = subprocess.run([f"ping -c 2 {server} | grep round-trip"], shell=True, capture_output=True, text=True)

#print(ping_result.stdout)

parsed_text = ping_result.stdout.strip()


_, avg_time, _, _ = re.findall("\d+\.\d+", parsed_text)
print(parsed_text)
print(f"Average latency = {avg_time}")



connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# table = """ CREATE TABLE server_latency (
#   Host CHAR(60) NOT NULL,
#   Latency REAL,
#   created_at NUMERIC
# )
# """
# cursor.execute(table)

insert_values = (server, avg_time, request_time)
insert_query = "INSERT INTO server_latency VALUES(?, ?, ?)"
cursor.execute(insert_query, insert_values)
connection.commit()


result = cursor.execute("Select * from server_latency ORDER BY created_at DESC;")
print(result.fetchall())
connection.close()

