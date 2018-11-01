from tkinter import *
import firebase_admin
from firebase_admin import db
from base64 import b64decode, b64encode
from simplecrypt import encrypt, decrypt
from datetime import datetime
from time import time
from getpass import getpass
cred = firebase_admin.credentials.Certificate(
    '/home/minlaxz/confidential/serviceKey.json')
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://laxz-test.firebaseio.com/',
                               'databaseAuthVariableOverride': {
                                   'uid': 'writer'}})  # , name='laxz'

master_pass = db.reference(
    'restricted_access/confidentials/master_password').get()
sec_pass = db.reference(
    'restricted_access/confidentials/secret_password').get()


def check_or_save():
    t1 = time()
    domain = e0.get()
    email = e1.get()
    password = e2.get()
    databaseRef = db.reference('restricted_access/confidentials')
    try:
        check = databaseRef.child(domain).get()
        if check is not None:
            print("::::::#### FIREBASE Return ####::::::")
            for key, val in databaseRef.child(domain).get().items():
                if(key == 'email'):
                    femail = val
                    print('Email: {0}'.format(val))
                if(key == 'password'):
                    fpassword = val
                    print('Password: {0}'.format(val))
                if(key == 'entry_time'):
                    ftime = val
            decoded_email, decoded_password = decode_data(femail, fpassword)
            textChanged(decoded_email, decoded_password, ftime)

        else:
            if not email or not password:
                print("Empty")
                textErr()
            else:
                #Label(root, text='Saved').grid(row=0, column=3)
                databaseRef = db.reference(
                    'restricted_access/confidentials/'+domain)
                encoded_email, encoded_password = encode_data(email, password)
                update(databaseRef, domain, encoded_email, encoded_password)
    except ValueError:
        print('Enter Domain!')
    print(time() - t1)
    e1.delete(0, 'end')
    e2.delete(0, 'end')

def click_del_domain():
    domain = e0.get()
    databaseRef = db.reference('restricted_access/confidentials')
    try:
        check = databaseRef.child(domain).get()
        if check is not None:
            msg_text = """
            This will permanently delete
            the specific record!
            """
            top = Toplevel()
            top.geometry("315x135")
            top.title("Do you want to delete?")
            top.resizable(False,False)
            msg = Message(top, text=msg_text , fg = 'red')
            msg.pack()
            btnDismiss = Button(top, text="Confirm" , command=test)
            btnDismiss.pack()
        else:
            print("No Domain in database")
            error()

    except ValueError:
        print('Enter Domain!')

    except Exception as e:
        print(e)


def test():
    print("Ok")
    top.destory()
def dismiss():
    print("Dismiss")

def del_domain():
    domain = e0.get()
    e0.delete(0, 'end')
    databaseRef = db.reference('restricted_access/confidentials/'+domain)
    try:
        databaseRef.delete()
    except Exception as e:
        print(e)

def update(databaseRef, domain, email, password):
    databaseRef.set({
        u'domain': domain,
        u'email': email,
        u'password': password,
        u'entry_time': str(datetime.now())
    })

def encode_data(email, password):
    cipher_email = encrypt(sec_pass, email)
    cipher_password = encrypt(sec_pass, password)
    encoded_email = b64encode(cipher_email)
    encoded_password = b64encode(cipher_password)
    return encoded_email, encoded_password


def decode_data(encoded_email, encoded_password):
    cipher_email = b64decode(encoded_email)
    cipher_password = b64decode(encoded_password)
    return decrypt(sec_pass, cipher_email), decrypt(sec_pass, cipher_password)

#encoded_user = b64encode(encrypt(sec_pass ,  getpass("Enter Master Password: ")))
#print("Decoding ...")
#decoded_user = decrypt(sec_pass, b64decode(encoded_user))
#print("Working on it ...")
#encoded_master = b64encode(encrypt(sec_pass , master_pass))
#decoded_master = decrypt(sec_pass, b64decode(encoded_master))


decoded_master = '1'
decoded_user = '1'

if decoded_master == decoded_user:
    print("Authentication : OK")
else:
    print("Wrong Passowrd")
    exit()


root = Tk()
root.geometry("630x270")
root.title("encod3d passwd online mgr by laxz")
root.configure(background='grey')
root.resizable(False,False)

def error():
    t6 = Text(root, width=30, height=1, bg='grey', fg='red')
    t6.pack()
    t6.insert(END, 'No Domain in database')
    t6.place(x=340, y=50)
    t6.config(state=DISABLED)

def textErr():
    t2 = Text(root, width=30, height=1, bg='grey', fg='red')
    t2.pack()
    t2.insert(END, 'Email: Null')
    t2.place(x=340, y=50)
    t2.config(state=DISABLED)

    t3 = Text(root, width=30, height=1, bg='grey', fg='red')
    t3.pack()
    t3.insert(END, 'Password: Null')
    t3.place(x=340, y=100)
    t3.config(state=DISABLED)

    t4 = Text(root, width=40, height=1, bg='grey', fg='red')
    t4.pack()
    t4.insert(END, 'Created at: Null')
    t4.place(x=300, y=150)
    t4.config(state=DISABLED)


def textChanged(email, password, time):
    t2 = Text(root, width=40, height=1, bg='grey', fg='white')
    t2.pack()
    t2.insert(END, 'Email: ')
    t2.insert(END, email)
    t2.place(x=300, y=50)
    t2.config(state=DISABLED)

    t3 = Text(root, width=40, height=1, bg='grey', fg='white')
    t3.pack()
    t3.insert(END, 'Password: ')
    t3.insert(END, password)
    t3.place(x=300, y=100)
    # t3.config(state=DISABLED)

    t4 = Text(root, width=40, height=1, bg='grey', fg='white')
    t4.pack()
    t4.insert(END, 'Created at: ')
    t4.insert(END, time)
    t4.place(x=300, y=150)
    t4.config(state=DISABLED)


############# TEXT #################
t1 = Text(root, width=20, height=1, bg='grey', fg='white')
t1.pack()
t1.insert(END, '::::Information::::')
t1.place(x=380, y=2)
t1.config(state=DISABLED)

t5 = Text(root, width=35, height=5, bg='black', fg='white')
t5.pack()
t5.insert(END, 'Developed by Min Latt.(root.lazx)  ')
t5.insert(END, 'Using Firebase\'s Realtime Database ')
t5.insert(END, 'This is under GNU License :ae lae: ')
t5.insert(END, 'https://github.com/minlaxz/passmgrpython')
t5.place(x=5,y=100)
t5.config(state=DISABLED)
#####################################


########### ENTRIES ################
e0 = Entry(root, width=25)
e1 = Entry(root, width=25)
e2 = Entry(root, width=25 , show="*")

e0.pack()
e1.pack()
e2.pack()

e0.place(x=80, y=2)
e1.place(x=80, y=27)
e2.place(x=80, y=54)
####################################


########### LABLES #################
l0 = Label(root, text="Domain", bg='grey')
l1 = Label(root, text="Email", bg='grey')
l2 = Label(root, text="Password", bg='grey')

l0.pack()
l1.pack()
l2.pack()

l0.place(x=2, y=2)
l1.place(x=2, y=27)
l2.place(x=2, y=54)
####################################


########### BUTTONS ################
# .grid(row=4, column=0, sticky=W, pady=4)
delBtn = Button(root, text='Delete', bg='red', fg='white', command=click_del_domain)
quitBtn = Button(root, text='Adios', bg='grey', fg='red', command=root.quit)
saveBtn = Button(root, text='Check or Save', bg='grey', fg='black', command=check_or_save)
quitBtn.pack()
saveBtn.pack()
delBtn.pack()
delBtn.place(x=220 ,y=220)
quitBtn.place(x=10, y=220)
saveBtn.place(x=85, y=220)
####################################


mainloop()
