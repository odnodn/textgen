import requests

save = "https://russian-dating.com/sendMessage"
txt = "Hello World"
login = "https://russian-dating.com/login"

idc = "1229994"
password = "4208361"

data = {"action": "login",
        "id": idc,
        "password": password,
        "submit": ""}

# construct the POST request
with requests.session() as s: # Use a Session object.
    r = s.post(login, data) # Login.
    print (r)

    form_data = {"number": "2yrwpi",
                 "notetype": "PlainText",
                 "noteaccess": "2",
                 "notequickedit": "false",
                 "notetitle": "whatever",
                 "notecontent": txt}

    r = s.post(save, data=form_data) # Save note.