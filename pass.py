import string
import random
from tkinter import Tk
import pyperclip

SEPERATOR = "-----"
FILE_PASS = "pass.txt"
FLAG_CHANGE_PASS = "flag_pass"
FLAG_CHANGE_USERNAME = "flag_username"

cryptor = input("Enter cryption key: >> ")

def randomPassGenerate():
	newid = ""
	newid += string.printable[:84][random.randint(0,60)]
	for _ in range(0,14):
		newid += string.printable[:84][random.randint(0,83)]
	return newid

def savePass(whom, un, pw):
	whom = whom.lower()
	un = un.lower()
	if (getPass(whom) != 0):
		y = input("You already have a password for " + whom + ". Do you want to update? (y/n) >> ")
		if y == "y" or y == "Y":
			deletePass(whom)
		else:
			return getPass(whom)
	with open(FILE_PASS, "a", encoding="utf-8") as fil:
		fil.write(whom + SEPERATOR + encrypt(un) + SEPERATOR + str(encrypt(pw)) + "\n")
	copyToClipboard(str(pw))
	print("Password", pw, "has been saved succesfully for", whom)

def getPass(whom):
	whom = whom.lower()
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read().split("\n")
		for item in a:
			b = item.split(SEPERATOR)
			if b[0] == whom:
				copyToClipboard(decrypt(b[2]))
				return decrypt(b[1]) + " " + decrypt(b[2])
		return 0

def getUserName(whom):
	whom = whom.lower()
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read().split("\n")
		for item in a:
			b = item.split(SEPERATOR)
			if b[0] == whom:
				copyToClipboard(decrypt(b[1]))
				return decrypt(b[1]) + " " + decrypt(b[2])
		return 0

def search(value):
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read().split("\n")
		a.pop()
		son = [["Platform", "User Name", "Password"], ["-----------","-----------","-----------"]]
		for item in a:
			b = item.split(SEPERATOR)
			if(value in b[0]):
				son.append([b[0], decrypt(b[1]), decrypt(b[2])])
		if (len(son) <= 2):
			print("Couldn't find",value)
			return
		row_format ="{:15}{:30}{:}"
		for item in son:
		    print (row_format.format(*item))

def deletePass(whom):
	whom = whom.lower()
	if (getPass(whom) == 0):
		print("You already don't have a password for", whom)
		return
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read()
		kesbas = a.index(whom)
		kesson = a[kesbas:].index("\n")
		son = a[:kesbas] + a[kesbas + kesson + 1:]
	with open(FILE_PASS, "w", encoding="utf-8") as fil:
		fil.write(son)
	print("Your password for", whom, "has been successfully deleted.")

def change(whom, newThing, flag):
	whom = whom.lower()
	if (getPass(whom) == 0):
		print("You already don't have a password for", whom)
		return
	if (newThing == "rast" or newThing == "random"):
		newThing = randomPassGenerate()
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read()
		kesbas = a.index(whom)
		kesson = a[kesbas:].index("\n")
		b = a[kesbas : kesbas + kesson]
		c = b.split(SEPERATOR)
		if flag == FLAG_CHANGE_PASS:
			d = c[0] + SEPERATOR + c[1] + SEPERATOR + encrypt(newThing) + "\n" 
			copyToClipboard(newThing)
			print("Your password has been changed from", whom, "to", newThing, "succesfully.")
		else:
			d = c[0] + SEPERATOR + encrypt(newThing) + SEPERATOR + c[2] + "\n" 
			print("Your username has been changed from", whom, "to", newThing, "succesfully.")
		son = a[:kesbas] + d + a[kesbas + kesson + 1:]
	with open(FILE_PASS, "w", encoding="utf-8") as fil:
		fil.write(son)

def printAllPasswords():
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read().split("\n")
		a.pop()
		son = [["Platform", "User Name", "Password"], ["-----------","-----------","-----------"]]
		for item in a:
			b = item.split(SEPERATOR)
			son.append([b[0], decrypt(b[1]), decrypt(b[2])])
		
		row_format ="{:15}{:30}{:}"
		for item in son:
			print(row_format.format(*item))

def copyToClipboard(thing):
	pyperclip.copy(thing)

def encrypt(thing):
	a = string.printable[:84]
	r = ''
	i = 0
	for char in thing:
		r += a[(a.index(char) + a.index(cryptor[i])) % len(a)]
		i += 1
		i = i % len(cryptor)
	return r

def decrypt(thing):
	a = string.printable[:84]
	r = ''
	i = 0
	for char in thing:
		r += a[(a.index(char) - a.index(cryptor[i])) % len(a)]
		i += 1
		i = i % len(cryptor)
	return r

while True:
	command = input(">> ")
	command = command.strip()

	if "add" in command and command.index("add") == 0:
		p = input("Do you want to create a password for what platform? >> ")
		u = input("Enter your username. >> ")
		savePass(p, u, randomPassGenerate())
	
	if "hard" in command and command.index("hard") == 0:
		p = input("Do you want to create a password for what platform? >> ")
		u = input("Enter your username. >> ")
		s = input("Enter your password. >> ")
		savePass(p, u, s)
			
	elif "get" in command and command.index("get") == 0:
		a = command.split(" ")
		if len(a) >= 2:
			if a[1] == "user" or a[1] == "username" or a[1] == "kull":
				if len(a) >= 3:
					print(getUserName(a[2]))
				else:
					u = input("For which platform do you want to get your username? >> ")
					print("Your username has been copied to the clipboard.")
					print(getUserName(u))
				continue
			if getPass(a[1]) == 0:
				print("You don't have a password for", a[1])
			else:
				print("Your password has been copied to the clipboard.")
				print("Your username and password:", getPass(a[1]))
		else:
			t = input("For which platform do you want to get your username? >> ")
			if getPass(t) == 0:
				print("You don't have a password for", t)
			else:
				print("Your password has been copied to the clipboard.")
				print("Your username and password:", getPass(t))
	
	elif "search" in command and command.index("search") == 0:
		a = command.split(" ")
		if len(a) >= 2:
			search(a[1])
		else:
			t = input("Enter your search key. >> ")
			search(t)

	elif "delete" in command and command.index("delete") == 0:
		a = command.split(" ")
		if len(a) >= 2:
			deletePass(a[1])
		else:
			t = input("For which platform do you want to delete your password? >> ")
			deletePass(t)
	
	elif "change" in command and command.index("change") == 0:
		a = command.split(" ")
		if len(a) >= 4:
			if a[2] == "pass" or a[2] == "pw" or a[2] == "password":
				change(a[1], a[3], FLAG_CHANGE_PASS)
			else:
				change(a[1], a[3], FLAG_CHANGE_USERNAME)
		elif len(a) == 3:
			t = input("Enter new value. (Write random for random.)>> ")
			if a[2] == "pass" or a[2] == "pw" or a[2] == "password":
				change(a[1], t, FLAG_CHANGE_PASS)
			else:
				change(a[1], t, FLAG_CHANGE_USERNAME)
		elif len(a) == 2:
			f = input("Do you want to change username or password? (pass/user) >> ")
			t = input("Enter new value. (Write random for random.)>> ")
			if f == "pass" or f == "pw" or f == "password":
				change(a[1], t, FLAG_CHANGE_PASS)
			else:
				change(a[1], t, FLAG_CHANGE_USERNAME)
			
		else:
			n = input("For which platform do you want to change something? >> ")
			f = input("Do you want to change username or password? (pass/user) >> ")
			t = input("Enter new value. (Write random for random.)>> ")
			if f == "pass" or f == "pw" or f == "password":
				change(n, t, FLAG_CHANGE_PASS)
			else:
				change(n, t, FLAG_CHANGE_USERNAME)

	elif "all" in command and command.index("all") == 0:
		printAllPasswords()
	
	elif command == "help":
		print("add / hard / get (who) / delete (who) / search (key) / change (who) (flag) (newValue) / all")

	elif command == "cikis" or command == "exit":
		print("See you.")
		break