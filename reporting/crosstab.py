import os

def main():
	os.system('xlsx2csv -f %Y/%m/%d ' + fn_in + ' ' + fn_out)
	os.system('fart -c -i ' + fn_out + "ZAR/" + 'ZAR')
	
if name = __main__:
	main()
