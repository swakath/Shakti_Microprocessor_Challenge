import requests
import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from mfrc522 import SimpleMFRC522
import getpass
from os import system, name
from time import sleep
import random
import math

def clear():
  
    # for windows
	if name == 'nt':
		_ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
	else:
		_ = system('clear')


####### DB Query functions #########
url = "https://shakti-challenge.herokuapp.com"
# url = "http://localhost:5001"
def check_str(entry,length):
	if isinstance(entry, str) and len(entry) <= length:
		return True
	print("Invalid Datatype or length")
	return False

def registerEmp(empId,name,password,mobile,authority):
	if not(check_str(empId,30) and check_str(name,30) and check_str(password,30) and check_str(mobile,10) and isinstance(authority,int)):
		print("Datatype error.\n")
		return False
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
		#print("Server[successful] : ",res["msg"])
		#print("Employee details :- \n empId :",res["empId"],"\nname :",res["name"])
		return True
	else :
		print("Server[error] : ",res["msg"])
		return False

def validateEmp(empId,password):
	if not(check_str(empId,30) and check_str(password,30)):
		print("Datatype error.\n")
		return False,False
	req_json = {
	"empId" : empId, # string 30
	"password" : password # string 30
	}
	response = requests.get(url+"/empValidate",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
		#print("Server[successful] : ",res["msg"])
		#print("Account details :- \nname :",res["name"],"\nisManager :",res["isManager"])
		return True,res["isManager"]
	else :
		print("Server[error] : ",res["msg"])
		return False,False

def getEmpDetails(empId):
	if not check_str(empId,30):
		print("Datatype Error")
		return False,False	
	req_json = {
		"empId" : empId,
	}
	response = requests.get(url+"/empDetails",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
        #print("Server[successful] : ",res["msg"])
        #print(res["empId"],res["name"],res["mobile"],res["authority"])
		return True,res
	else :
		#print("Server[error] : ",res["msg"])
		return False,res

def validateUser(rfid,pin):
	info = []
	if not (isinstance(rfid,int) and check_str(pin,10)):
		print("Data type error.\n")
		return False,info
		
	req_json = {
		"rfid" : rfid, # integer
		"pin" : pin # string 10
	}
	response = requests.get(url+"/validate",json=req_json)
	res = json.loads(response.text)
	
	if res["valid"]:
		#print("Server[successful] : ",res["msg"])
		#print("Account details :- \nrfid :",res["rfid"],"\nname :",res["name"],"\nbalance :",res["balance"])
		info = [res["rfid"],res["name"],res["balance"]]
		return True,info
	else :
		print("Server[error] : ",res["msg"])
		return False,info

def registerUser(name,pin,address,mobile,balance):

	if not (check_str(name,30) and check_str(pin, 10) and check_str(address,50) and check_str(mobile,10) and isinstance(balance,int)):
		print("Data type error.\n")
		return False,False

	req_json = {
		"pin" : pin, # string 10
		"address" : address, # string 50
		"mobile" : mobile, # string 10
		"balance" : balance, # integer
		"name" : name # integer 30
	}
	response = requests.post(url+"/register",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
        #print("Server[successful] : ",res["msg"])
        #print("Account details :- \nrfid :",res["rfid"])
		return True,res["rfid"]
	else :
		print("Server[error] : ",res["msg"])
		return False,False

def confirmWrite(rfid):
	if not isinstance(rfid, int):
		print("Data type error.\n")
		return False

	req_json = {
		"rfid" : rfid # integer
	}
	response = requests.put(url+"/confirmWrite",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
        #print("Server[successful] : ",res["msg"])
		return True
	else :
		print("Server[error] : ",res["msg"])
		return False

def withdraw(rfid,pin,amount):
	if not ( isinstance(rfid,int) and isinstance(amount,int) and check_str(pin,10)):
		print("Data type error.\n")
		return False,False

	req_json = {
		"rfid" : rfid, # integer
		"pin" : pin, # string 10
		"amount" : amount # integer
	}
	response = requests.post(url+"/deduct",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
        #print("Server[successful] : ",res["msg"])
        #print("Account details :- \nrfid :",res["rfid"],"\ncurrent balance :",res["balance"])
		return True,res["balance"]    
	else :
		print("Server[error] : ",res["msg"])
		return False,False

def deposite(rfid,pin,amount):
	if not ( isinstance(rfid,int) and isinstance(amount,int) and check_str(pin,10)):
		print("Data type error.\n")
		return False,False

	req_json = {
		"rfid" : rfid, # integer
		"pin" : pin, # string 10
		"amount" : amount # integer
	}
	response = requests.put(url+"/addAmount",json=req_json)
	res = json.loads(response.text)
	if res["valid"]:
        #print("Server[successful] : ",res["msg"])
        #print("Account details :- \nrfid :",res["rfid"],"\ncurrent balance :",res["balance"])
		return True, res["balance"]    
	else :
		print("Server[error] : ",res["msg"])
		return False,False

def updateBalance(rfid,pin,balance):
    req_json = {
        "rfid" : rfid,
        "pin" : pin,
        "balance" : balance
    }
    response = requests.put(url+"/updateBalance",json=req_json)
    res = json.loads(response.text)
    if res["valid"]:
        # to get details 
        #print(res["rfid"], res["balance"])
        return True
    else :
        print(res["msg"])
        return False

def getDetails(rfid):
	req_json = {
		"rfid" : rfid
	}
	response = requests.get(url+"/getDetails",json=req_json)
	res = json.loads(response.text)
	info =[]
	if res["valid"]:
        # to get details 
        # print(res["rfid"], res["name"], res["balance"], res["address"], res["mobile"],res["issueDate"],res["lastAccessDate"])
		#info = [res["rfid"], res["name"], res["balance"], res["address"], res["mobile"],res["issueDate"],res["lastAccessDate"]]        
		return True,res
	else :
		return False,res

#verifyLogin(user,pwd) // to verify the user name and pwd and return the access type (User data / Employee data)
#getRFID()

def generatePIN():
	pin = random.randint(999, 9999)
	pin = str(pin)
	return pin

####### RFID Sensor Functions ##############
def wrapData(RFID,Pin,Amount,Name):	
	#IN - 4(2)
	#RFID - 8(6)
	#Pin - 6(4)
	#Amount -6(4)
	#Name - 24(22)
	
	if len(Name) > 22:
		Name = Name[0:22]
	text = "IN X" + str(RFID) + " X" + str(Pin) + " X" + str(Amount)+ " X"+ Name + " X"
	#print("This is the packet info: ",text);	
	return text
	
def unwrapData(packet):
	flag = False	
	bridge = packet.split(" X")
	info = [] #[IN,RFID,PIN,AMOUNT,NAME]
	
	if len(bridge)>=5:
		info.append(bridge[0])
		if info[0] == 'IN':	
			info.append(int (bridge[1])) #RFID
			info.append(bridge[2]) #PIN
			info.append(int(bridge[3])) #Amount
			info.append(bridge[4]) #Name
			flag = True
		else:
			info = []
	return flag,info	
	
def writeCard(RFID,Pin,Amount,Name):
	flag = False #flag is true is write is successful
	text = wrapData(RFID,Pin,Amount,Name)
	writer = SimpleMFRC522()
	try:
		writer.write(text)
	except:
		flag = False
		#print("Failed to write data in the tag")
	else:
		flag = True
		#print("Data written to the tag")
	finally:
		GPIO.cleanup()
	return flag


def readCard():
	flag = False
	info = [] #[IN,RFID,PIN,Amount,Name]
	reader = SimpleMFRC522()
	try:
		id, text = reader.read()
	except:
		flag = False
		info = []
		#print("Failed to read the card")	
	else:
		retFlag,info = unwrapData(text)
		flag = retFlag;
		if not flag:
			info = []
		#print("Data read from the card")
		
	finally:
		GPIO.cleanup()
	return flag,info

def verifyWrite(RFID,PIN,Amount,Name):
	flag = False
	custInfo = ['IN',RFID,PIN,Amount,Name]
	retFlag,cardInfo = readCard()
	if (cardInfo == custInfo) and retFlag:
		flag = True
	return flag	

def isCardEmpty():
	flag,info = readCard()
	if len(info)!=0 and info[0] == 'IN':
    	#print("The Card is already written")
		return False
  		#print("The card is empty")
	return True	
  			
####### Functions for user options #########
def verificationBOX(txt):
	isValid = False
	while not isValid:
		opt = input(txt)
		if opt=='y' or opt == 'Y':
			return True
		elif opt=='n' or opt == 'N':
			return False
		else:
			print("\'",opt,"\' is not a valid option. Please enter valid option.\n")

####### User functions ##########
def addUser():
	clear()
	print("######### ADD USER PAGE #########")
	#name,address,mobile number
	
	#Getting customer information
	print("Please enter the following customer details: ")
	custName = input("Name: ") #Customer Name
	custMobile = input("Mobile Number:(+91)") #Customer Mobile Number	
	custAdd = input("Address: ")	#Customer Address
	custRFID = 0
	custPIN = generatePIN() #Generating Customer Pin
	custBalance = 0 #Initial Card Balance is set to zero
	
	# Verification of the information
	isVerified = False # Verification in True if input is y|Y
	isVerified = verificationBOX("Information is verified. Proceed to issue RFID tag. [Y|N] ")
	
	
	
	# Adding the information to database and RFID Tag is verification is successful	
	isCardWrite = False	
	if isVerified:	
	# Data of the user is written in the RFID Tag
		isDatabaseWrite,custRFID = registerUser(custName,custPIN,custAdd,custMobile,custBalance)
		#custRFID = getRFID(custPIN,custBalance,custName) # Getting RFID from database
		if isDatabaseWrite:
			print("Place the RFID Tag.\n")
			isCardWrite	= isCardEmpty()
			if not isCardWrite:
				print("The Tag has is not empty.\n")
		if isCardWrite:	
			isCardWrite = writeCard(custRFID,custPIN,custBalance,custName)		
		else:
			isCardWrite = False
	# If the write is Successful the written data is read again to verify
		if isCardWrite:	
			#print("Card is written")
			isCardWrite	= verifyWrite(custRFID,custPIN,custBalance,custName) # Verification of write
		if isCardWrite:
			#print("Card written is verified
	# Updating Database if the write is successful and printing the credintials
			isDatabaseWrite = False
			isDatabaseWrite = confirmWrite(custRFID)
			
			# Update data base succeful column to true.
	if isCardWrite and isDatabaseWrite:
		print("Tag Created Succefully.\n");
		print("Customer ID: ",custRFID,"\nCustomer PIN: ",custPIN,'\n')
	else:		
		print("Tag write failure please try again.\n");		
	# Taking input for the 
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with Add User\n2) Go to Main Page\n")
		if option=='1':
			addUser()
			isValidOption = True
		if option =='2':
			mainPage()
			isValidOption = True
		else:
			print("Please enter valid option number.\n")

def depositeMoney():
	clear()
	isDeposit = False
	
	print("############## Deposite money ##############")
	print("Place the RFID Tag.\n")

	isDeposite,info = readCard()
	if isDeposite:
		RFID = info[1]
		PIN = info[2]
		Balance = info[3]
		Name = info[4]
		print("Card Info\nTag ID: ",RFID,"\nCustomer Name: ", Name,"\nCurrent Balance: ",Balance,"\n")
		isDeposite = updateBalance(RFID,PIN,Balance)
		value = int (input("Please enter deposite value (in Rs.): "))
		if isDeposite:		
			isDeposite = verificationBOX("Proceed depositing Rs." + str (value)+" [Y|N] ")
	if isDeposite:
		isDeposite,Balance = deposite(RFID,PIN,value)
		if isDeposite:
			print("Database updated")
			isDeposite = writeCard(RFID,PIN,Balance,Name)
			if isDeposite:
				isDeposite = verifyWrite(RFID,PIN,Balance,Name)
			if not isDeposite:
				withdraw(RFID,PIN,value)
	if isDeposite:
		print("Deposite Successful.\n")
		print("Updated Info\nTag Number: ",RFID,"\nCurrent Balance: ", Balance,"\n")
	else:
		print("Deposite Failure. \n")

	# Taking input for the 
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with Deposite money\n2) Go to Main Page\n")
		if option=='1':
			depositeMoney()
			isValidOption = True
		if option =='2':
			mainPage()
			isValidOption = True
		else:
			print("Please enter valid option number")

def getUserInfo():
	clear()
	print("########## User Info #############")
	RFID = input("Enter User Tag ID: ")
	isValid,res = getDetails(RFID)
	if isValid:
		print("\nUser info:\nTag ID: ", res['rfid'],"\nName: ",res['name'],"\nAddress: ",res['address'],"\nMobile Number: ",res['mobile'],"\nBalance: ",res['balance'],"\nLast access date: ",res['lastAccessDate'],'\n')
	else:
		print(res['msg'])
	# Taking input for the 
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with User Info\n2) Go to Main Page\n")
		if option=='1':
			getUserInfo()
			isValidOption = True
		if option =='2':
			mainPage()
			isValidOption = True
		else:
			print("Please enter valid option number")

############## Employee Functions #################
def addEmployee():
	clear()
	print("######### ADD Employee PAGE #########")
	# name,address,mobile number
	
	# Getting employee information
	print("Please enter the following Employee details: ")
	empName = input("Name: ") #Employee Name
	empMobile = input("Mobile Number:(+91)") #Employee Mobile Number	
	empAdd = input("Address: ")	#Employee Address
	empEmail = input("Email ID (Will be used for login): ")
	selectedOption = verificationBOX("Is the employee an admin [Y|N] ")
	if selectedOption:
		auth = 0
	else:
		auth = 2
	notPass = True
	while notPass:
		empPass = getpass.getpass(prompt='Enter Password: ')
		reEnter = input("Re-Enter Password: ")
		if empPass == reEnter:
			notPass = False
		else:
			print("Password not Matching.Try again.\n")
	selectedOption = False	
	selectedOption = verificationBOX("All details verified. Add employee details. [Y|N] ")
	if selectedOption:
		selectedOption = registerEmp(empEmail,empName,empPass,empMobile,auth)
	if selectedOption:
		print("Employee added successfully.\n")
	else:
		print("Employee add fail. Please try again.\n")
	
	# Taking input for the next instruction.
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with Add Employee\n2)Go to Admin Page\n")
		if option=='1':
			addEmployee()
			isValidOption = True
		if option =='2':
			adminPage()
			isValidOption = True
		else:
			print("Please enter valid option number")

def getEmployeeInfo():
	clear()	
	print("######### Get Employee Info ##########")
	empID = input("Enter Employee Email ID: ")
	isValid,res = getEmpDetails(empID)
	if isValid:
		print("\nEmployee Information")
		print("Email ID: ",res["empId"],"\nName:",res["name"],"\nMobile: ",res["mobile"],"\nAuthority: ",res["authority"],"\n")
	else:
		print(res['msg'],"\n")
	# Taking input for the next instruction.
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with Get Employee Info\n2) Go to Admin Page\n")
		if option=='1':
			getEmployeeInfo()
			isValidOption = True
		if option =='2':
			adminPage()
			isValidOption = True
		else:
			print("Please enter valid option number.\n")	
############# Login Functions ####################	
def loginWindow():
	while True:
		clear()   
		print("######### LOGIN PAGE #########")
		empID = input("Employee ID:");
		pwd = getpass.getpass(prompt='Pass ')
		isValidCred = False	
		#isValidCred = True
		#isAdmin = True
		isValidCred,isAdmin = validateEmp(empID,pwd) 
		#print(isValidCred,isAdmin)      	
		if isValidCred:
			print (u'\u2713',"Authentication Successful")
			sleep(2)
			clear()
			print("Welcome!!")
			sleep(2)
			clear()
			if isAdmin:
				adminPage()
			else:			
				mainPage()
		else:
			print("----Incorrect credentials. Please try again.-----")

def mainPage():
	clear()
	print("######### HOME PAGE #########")
	while True:
		option = input("\nSelect your option:\n1) Add user\n2) Get user info\n3) Deposite money\nEnter \'exit\' to exit\n")
		if option=='1':
			addUser()
		elif option=='2':
			getUserInfo()
		elif option=='3':
			depositeMoney()
			print("LOL")
		elif option=='exit':
			quit()
		else:
			print("Please enter valid option\n")
	
		

def adminPage():
	clear()
	print("######### ADMIN PAGE #########")
	while True:
		option = input("\nSelect your option:\n1) Create Employee ID \n2) Get Employee Info\n3) Go to customer option\nEnter\'exit\' to exit\n")
		if option=='1':
			addEmployee()
		elif option=='2':
			getEmployeeInfo()
		elif option=='3':
			mainPage()
		elif option=='exit':
			quit()
		else:
			print("Please enter valid option\n")
	
loginWindow();
