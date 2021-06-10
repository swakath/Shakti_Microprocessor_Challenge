import requests
import json

url = "https://shakti-challenge.herokuapp.com"
# url = "http://localhost:5001"

def registerEmp(empId,name,password,mobile,authority):
    req_json = {
        "empId" : empId, # string 30
        "name" : name, # string 30
        "password" : password, # string 30
        "mobile" : mobile, # integer
        "authority" : authority #0,1,2
    }
    response = requests.put(url+"/empAdd",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Employee details :- \n empId :",res["empId"],"\nname :",res["name"])
        return True
    else :
        print("Server[error] : ",res["msg"])
        return False

def validateEmp(empId,password):
    req_json = {
        "empId" : empId, # string 30
        "password" : password # string 30
    }
    response = requests.get(url+"/empValidate",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Account details :- \nname :",res["name"],"\nisManager :",res["isManager"])
        return True,res["isManager"]
    else :
        print("Server[error] : ",res["msg"])
        return False,False

def validateUser(rfid,pin):
    req_json = {
        "rfid" : rfid, # integer
        "pin" : pin # string 10
    }
    response = requests.get(url+"/validate",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Account details :- \nrfid :",res["rfid"],"\nname :",res["name"],"\nbalance :",res["balance"])
    else :
        print("Server[error] : ",res["msg"])

def registerUser(name,pin,address,mobile,balance):
    req_json = {
        "pin" : pin, # string 10
        "address" : address, # string 50
        "mobile" : mobile, # integer
        "balance" : balance, # integer
        "name" : name # integer 30
    }
    response = requests.post(url+"/register",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Account details :- \nrfid :",res["rfid"])
    else :
        print("Server[error] : ",res["msg"])

def confirmWrite(rfid):
    req_json = {
        "rfid" : rfid # integer
    }
    response = requests.put(url+"/confirmWrite",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        return True
    else :
        print("Server[error] : ",res["msg"])
        return False

def withdraw(rfid,pin,amount):
    req_json = {
        "rfid" : rfid, # integer
        "pin" : pin, # string 10
        "amount" : amount # integer
    }
    response = requests.post(url+"/deduct",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Account details :- \nrfid :",res["rfid"],"\ncurrent balance :",res["balance"])
    else :
        print("Server[error] : ",res["msg"])

def deposite(rfid,pin,amount):
    req_json = {
        "rfid" : rfid, # integer
        "pin" : pin, # string 10
        "amount" : amount # integer
    }
    response = requests.put(url+"/addAmount",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        print("Server[successful] : ",res["msg"])
        print("Account details :- \nrfid :",res["rfid"],"\ncurrent balance :",res["balance"])
    else :
        print("Server[error] : ",res["msg"])

while True :
    option = input("\n1) validate rfid and pin\n2) addNewUser\n3) deduct amount\n4) add amount \n5) comfirm Write \n--Emp functions--\n6) Validate Employee\n7) add Employee\nSelect your option: ")
    if option == '1':
        rfid = input("Enter rfid : ")
        pin = input("Enter pin : ")
        validateUser(rfid,pin)
    elif option == '2':
        name = input("Enter name :")
        pin = input("Enter pin :")
        mobile = input("Enter mobile : ")
        address = input("Enter address :")
        balance = input("Enter the inital balance :")
        registerUser(name,pin,address,mobile,balance)
    elif option == '3':
        rfid = input("Enter rfid :")
        pin = input("Enter pin :")
        amount = input("Enter withdraw amount :")
        withdraw(rfid,pin,amount)
    elif option == '4':
        rfid = input("Enter rfid :")
        pin = input("Enter pin :")
        amount = input("Enter deposite amount :")
        deposite(rfid,pin,amount)
    elif option == '5':
        rfid = input("Enter rfid :")
        confirmWrite(rfid)
    elif option == '6':
        empId = input("Enter empId :")
        password = input("Enter password :")
        validateEmp(empId,password)
    elif option == '7':
        empId = input("Enter empId :")
        name = input("Enter name :")
        password = input("Enter password :")
        mobile = input("Enter mobile :")
        authority = input("Enter authority(0-Admin,1-manager,2-employee) :")
        registerEmp(empId,name,password,mobile,authority)
    else :
        break