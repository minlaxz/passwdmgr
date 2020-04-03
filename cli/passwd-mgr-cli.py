# This Python Cli Script is developed by Min Latt (laxz) (facebook:minlaxz)

import SOME

cred = admin.credentials.Certificate('serviceKey.json')
admin.initialize_app(cred ,
{
    'databaseURL' : 'https://laxz-test.firebaseio.com/' ,
    'databaseAuthVariableOverride' : {
        'uid' : 'service-writer'
    }
})
databaseRef = db.reference('restricted_access/confidentials')
#master_pass = db.reference('restricted_access/confidentials/master_password').get()
sec_pass = db.reference('restricted_access/confidentials/secret_password').get()
def chech_or_save():
    try:
        domain = input("\n\n Domain Name: ")
        if databaseRef.child(domain).get() is not None:
            check = input("Domain Exist! Show[s] Delete[d]: ")
            if check == 's':
                print_info(domain)
            elif check == 'd':
                del_domain(domain)
            else:
                print("Error")
        else:
            email = input("Enter Email: ")
            e = encode_this(email)
            password = getpass("Enter Password: ")
            p = encode_this(password)

            save_acc(e,p,domain)
    except ValueError:
        print("Eh! Domain ?")
        pass
    
    except KeyboardInterrupt:
        ex = input("  Exit! Yes[y] No[n]: ")
        if ex == 'y':
            print("Adios!")
            exit()
        else:
            pass

    except Exception as e:
        print(e)

def print_info(domain_name):
    for key , val in databaseRef.child(domain_name).order_by_key().get().items():
        if(key == 'email'):
            print("Email is: {0}".format(decode_this(val)))
        if(key == 'password'):
            print("Password is: {0}".format(decode_this(val)))
        if(key == 'time_entry'):
            print("Created at: {0}".format(val))

def decode_this(data):
    cipher_data = b64decode(data)
    print("Decrypting ...")
    return (decrypt(sec_pass , cipher_data)).decode("utf-8")

def encode_this(data):
    print("Encrypting ...")
    cipher_data = encrypt(sec_pass , data)
    return b64encode(cipher_data)

def save_acc(email,password,domain):
    databaseRef.child(domain).set({
        u'domain': domain,
        u'email': email,
        u'password': password,
        u'time_entry': str(datetime.now())
    })

def del_domain(domain):
    try:
        if(input("Delete Confirm! Yes[y] No[n]: ")== 'y'):
            print("It is Deleting ...")
            databaseRef.child(domain).delete()
            print("Domain Successfully deleted!")
        else:
            pass

    except Exception as e:
        print(e)

while True:
    chech_or_save()
