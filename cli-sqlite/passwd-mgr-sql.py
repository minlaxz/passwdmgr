import sqlite3
from datetime import datetime
from simplecrypt import encrypt , decrypt
from base64 import b64decode,b64encode
from getpass import getpass
from datetime import datetime
from sys import exit
sec_pass = 'laxzSecret'

def connect_db():
    db = sqlite3.connect('db.sqlite')
    return db

def create_table():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                      domains(id INTEGER PRIMARY KEY, domain TEXT unique, email TEXT, password TEXT, created_at TEXT)''')
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        print('DB closed.')
        db.close()

def add_data_db(domain):
    try:
        db = sqlite3.connect('db.sqlite')
        with db:
            email = encode_this(input("Email: "))
            password = encode_this(getpass("Password: "))
            now = str(datetime.now())
            db.execute('''INSERT INTO domains(domain, email, password, created_at)
                  VALUES(?,?,?,?)''', (domain, email, password, now))
            db.commit()

    except KeyboardInterrupt:
        db.rollback()
        ex = input("  Cancle? Yes[y] No[n]: ")
        if ex == 'y':
            print("Cancled !")
        else:
            pass
    #finally:
    #    print('DB closed. : add_data_db')
    #    db.close()

def decode_this(data):
    cipher_data = b64decode(data)
    print("Decrypting ...")
    return (decrypt(sec_pass , cipher_data)).decode("utf-8")

def encode_this(data):
    print("Encrypting ...")
    cipher_data = encrypt(sec_pass , data)
    return b64encode(cipher_data)

def del_domain(domain):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM domains WHERE domain=?''',(domain,))
        print('Delete : Done')
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    #finally:
    #    print('DB closed. : del_domain')
    #    db.close()
def update_domain(domain,email):
    try:
        db = connect_db()
        cursor = db.cursor()
        print("Email- {0}".format(email))
        password = encode_this(getpass("Enter update password: "))
        now = datetime.now()
        cursor.execute('''UPDATE domains SET password=? , created_at=? WHERE domain=?''',(password,now,domain))
        print("Update Done ...\n")
        db.commit()
        check_domain(domain)
    except Exception as e:
        db.rollback()
        raise e

def check_domain(domain):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('''SELECT email,password,created_at FROM domains WHERE domain=?''',(domain,))
        data = cursor.fetchone()
        if data is None:
            add_data_db(domain)
        else:
            chk = input("{0} Exists! show[s], delete[d], update[u]: ".format(domain))
            if chk == 'd':
                del_domain(domain)
            
            elif chk == 'u':
                update_domain(domain,decode_this(data[0]))
                
            else:
                print("Email: {0} ,Password: {1} ,Created at: {2} ".format(decode_this(data[0]),decode_this(data[1]),data[2]))

    except Exception as e:
        raise e

while True:
    create_table()
    try:
        domain = input("Domain: ")
        check_domain(domain)
    except KeyboardInterrupt:
        ex = input("  Exit! Yes[y] No[n]: ")
        if ex == 'y':
            print("Adios!")
            exit()
        else:
            pass
