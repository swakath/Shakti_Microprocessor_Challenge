import math

def check_str_30(entry):
	if isinstance(entry, str) and len(entry)==30:
		return True
	print("Invalid Datatype or length")
	return False


def check_str_10(entry):
	if isinstance(entry, str) and len(entry)==10:
		return True
	print("Invalid Datatype or length")
	return False
	
		
def check_int(entry):
	try:
	    int(entry)
	    if math.floor(math.log10(int(entry))+1)==10:
	    	return True
	    else:
	    	print("Invalid Length")
	    	return False
	    	
	except ValueError:
	    print("Invalid Datatype")	
	    return False
	    
	

		
#x = input("Enter String")
#print(check_int(x))




