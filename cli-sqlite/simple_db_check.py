import sqlite3

db = sqlite3.connect('db')
cursor = db.cursor()

cursor.execute('''SELECT domain, email, password, created_at FROM domains''')
all_rows = cursor.fetchall()
for row in all_rows:
    print('Domain - {0} \n Email - {1} \n Password - {2} \n Created at - {3}'.format(row[0], row[1].decode("utf-8"), row[2].decode("utf-8") , row[3]))

db.close()
print('############ DONE ###########')