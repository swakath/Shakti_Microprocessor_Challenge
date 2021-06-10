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
        #print("Server[successful] : ",res["msg"])
        #print("Account details :- \nrfid :",res["rfid"])
		return True,res["rfid"]
	else :
		print("Server[error] : ",res["msg"])
		return False,False

def confirmWrite(rfid):
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
	print("This is the packet info: ",text);	
	return text
	
def unwrapData(packet):
	flag = False	
	bridge = packet.split(" X")
	info = [] #[IN,RFID,PIN,AMOUNT,NAME]
	
	if len(bridge)>=5:
		info.append(bridge[0])
		if info[0] == 'IN':	
			info.append(int (bridge[1]))
			info.append(bridge[2])
			info.append(float(bridge[3]))
			info.append(bridge[4])
			flag = True
		else:
			info = []
	return flag,info	
	
def writeCard(RFID,Pin,Amount,Name):
	flag = False #flag is true is write is successful
	text = wrapData(RFID,Pin,Amount,Name)
	writer = SimpleMFRC522()

	try:
        	print("Now place your tag to write.\n")
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
    print("The Card is already written")
    return False
  print("The card is empty")
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
	custRFID = 123456	
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
		print("Card Created Succefully\n");
		print("Customer ID: ",custRFID,"\nCustomer PIN: ",custPIN,'\n')
	else:		
		print("Card write failure please try again");		
	# Taking input for the 
	isValidOption = False	
	while not isValidOption:
		option = input("Please Select Your Option:\n1) Continue with Add User\n2)Go to Main Page\n")
		if option=='1':
			addUser()
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
	#name,address,mobile number
	
	#Getting employee information
	print("Please enter the following Employee details: ")
	empName = input("Name: ") #Customer Name
	empMobile = input("Mobile Number:(+91)") #Customer Mobile Number	
	empAdd = input("Address: ")	#Customer Address
	
	selectedOption = verificationBOX("Is the employee an admin [Y|N] ")
	if selectedOption:
		opt = 0
	else:
		opt = 2
		
	empID = 123456	
	empPass = generatePIN() #Generating Customer Pin
	
	
	# Verification of the information
	isVerified = False # Verification in True if input is y|Y
	isVerified = verificationBOX("Information is verified. Proceed to issue RFID tag. [Y|N] ")

	if isVerified:
		#Add employee info in data base
		#Print emp id and pass
		print("Add is success.\n")
	else:
		print("Verification Fail. New Employee detaild not created.\n")
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

############# Login Functions ####################	
def loginWindow():
	while True:   
		print("######### LOGIN PAGE #########")
		empID = input("Employee ID:");
		pwd = getpass.getpass(prompt='Pass ')
		isValidCred = False	
		isValidCred = True
		isAdmin = False
		#isValidCred,isAdmin = validateEmp(empID,pwd) 
		print(isValidCred,isAdmin)      	
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
		option = input("\nSelect your option:\n1) Add user\n2) Get user info\n3) Deposite\nEnter \'exit\' to exit\n")
		if option=='1':
			addUser()
		elif option=='2':
			isCardEmpty()
			print("LOL")
		elif option=='3':
			#deposite()
			print("LOL")
		elif option=='exit':
			quit()
		else:
			print("Please enter valid option\n")
	
		

def adminPage():
	clear()
	print("######### ADMIN PAGE #########")
	while True:
		option = input("\nSelect your option:\n1) Create Employee ID \n2) Get Employee Info\n3)Remove Employee\nEnter\'exit\' to exit\n")
		if option=='1':
			addEmployee()
		elif option=='2':
			print("Enter Employee ID : ")
			ID = input()
			#getEmployeeInfo(ID)
			print("Details Printed")
		elif option=='3':
			removeEmployee()
		elif option=='exit':
			quit()
		else:
			print("Please enter valid option\n")
	
loginWindow();
