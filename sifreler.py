import string
import random
from tkinter import Tk
import pyperclip

SEPERATOR = "-----"
FILE_PASS = "sfr.txt"
FLAG_CHANGE_PASS = "flag_pass"
FLAG_CHANGE_USERNAME = "flag_username"

cryptor = input("Şifreyi girin: ")

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
		y = input(whom + " için zaten şifreniz bulunmaktadır. Güncellemek ister misiniz? (e/h) >> ")
		if y == "e" or y == "E":
			deletePass(whom)
		else:
			return getPass(whom)
	with open(FILE_PASS, "a", encoding="utf-8") as fil:
		fil.write(whom + SEPERATOR + encrypt(un) + SEPERATOR + str(encrypt(pw)) + "\n")
	copyToClipboard(str(pw))
	print(whom, "için yeni şifre", pw, "başarı ile kaydedildi.")

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
		son = [["Platform", "Kullanıcı Adı", "Şifre"], ["-----------","-----------","-----------"]]
		for item in a:
			b = item.split(SEPERATOR)
			if(value in b[0]):
				son.append([b[0], decrypt(b[1]), decrypt(b[2])])
		if (len(son) <= 2):
			print(value, "için arama sonucu bulunamadı.")
			return
		row_format ="{:15}{:30}{:}"
		for item in son:
		    print (row_format.format(*item))

def deletePass(whom):
	whom = whom.lower()
	if (getPass(whom) == 0):
		print(whom, "için zaten bir şifreniz yok.")
		return
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read()
		kesbas = a.index(whom)
		kesson = a[kesbas:].index("\n")
		son = a[:kesbas] + a[kesbas + kesson + 1:]
	with open(FILE_PASS, "w", encoding="utf-8") as fil:
		fil.write(son)
	print(whom, "şifreniz başarı ile silinmiştir.")

def change(whom, newThing, flag):
	whom = whom.lower()
	if (getPass(whom) == 0):
		print(whom, "için zaten bir şifreniz yok.")
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
			print(whom, "şifreniz başarı ile", newThing ,"olarak değiştirilmiştir.")
		else:
			d = c[0] + SEPERATOR + encrypt(newThing) + SEPERATOR + c[2] + "\n" 
			print(whom, "kullanıcı adınız başarı ile", newThing, "olarak değiştirilmiştir.")
		son = a[:kesbas] + d + a[kesbas + kesson + 1:]
	with open(FILE_PASS, "w", encoding="utf-8") as fil:
		fil.write(son)

def printAllPasswords():
	with open(FILE_PASS, "r", encoding="utf-8") as fil:
		a = fil.read().split("\n")
		a.pop()
		son = [["Platform", "Kullanıcı Adı", "Şifre"], ["-----------","-----------","-----------"]]
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
	komut = input(">> ")
	komut = komut.strip()

	if "add" in komut and komut.index("add") == 0:
		p = input("Ne için yeni şifre oluşturmak istiyorsunuz? >> ")
		u = input("Kullanıcı adını girin. >> ")
		savePass(p, u, randomPassGenerate())
	
	if "hard" in komut and komut.index("hard") == 0:
		p = input("Ne için yeni şifre oluşturmak istiyorsunuz? >> ")
		u = input("Kullanıcı adını girin. >> ")
		s = input("Şifrenizi girin. >> ")
		savePass(p, u, s)
			
	elif "get" in komut and komut.index("get") == 0:
		a = komut.split(" ")
		if len(a) >= 2:
			if a[1] == "user" or a[1] == "username" or a[1] == "kull":
				if len(a) >= 3:
					print(getUserName(a[2]))
				else:
					u = input("Ne için kullanıcı adını almak istiyorsunuz? >> ")
					print(getUserName(u))
				continue
			if getPass(a[1]) == 0:
				print(a[1], "için şifreniz bulunmamaktadır.")
			else:
				print("Kullanıcı adı ve şifreniz:", getPass(a[1]))
		else:
			t = input("Ne için yeni şifre almak istiyorsunuz? >> ")
			if getPass(t) == 0:
				print(t, "için şifreniz bulunmamaktadır.")
			else:
				print("Kullanıcı adı ve şifreniz:", getPass(t))
	
	elif "search" in komut and komut.index("search") == 0:
		a = komut.split(" ")
		if len(a) >= 2:
			search(a[1])
		else:
			t = input("Aranacak metninizi girin. >> ")
			search(t)

	elif "delete" in komut and komut.index("delete") == 0:
		a = komut.split(" ")
		if len(a) >= 2:
			deletePass(a[1])
		else:
			t = input("Neyin şifresini silmek istiyorsunuz? >> ")
			deletePass(t)
	
	elif "change" in komut and komut.index("change") == 0:
		a = komut.split(" ")
		if len(a) >= 4:
			if a[2] == "pass" or a[2] == "pw" or a[2] == "password":
				change(a[1], a[3], FLAG_CHANGE_PASS)
			else:
				change(a[1], a[3], FLAG_CHANGE_USERNAME)
		elif len(a) == 3:
			t = input("Yeni değeri girin. (Rastgele için rast yazın.)>> ")
			if a[2] == "pass" or a[2] == "pw" or a[2] == "password":
				change(a[1], t, FLAG_CHANGE_PASS)
			else:
				change(a[1], t, FLAG_CHANGE_USERNAME)
		elif len(a) == 2:
			f = input("Şifre mi değişecek, kullanıcı adı mı? (pass/user) >> ")
			t = input("Yeni değeri girin. (Rastgele için rast yazın.)>> ")
			if f == "pass" or f == "pw" or f == "password":
				change(a[1], t, FLAG_CHANGE_PASS)
			else:
				change(a[1], t, FLAG_CHANGE_USERNAME)
			
		else:
			n = input("Ne için değişiklik yapmak istiyorsunuz? >> ")
			f = input("Şifre mi değişecek, kullanıcı adı mı? (pass/user) >> ")
			t = input("Yeni değeri girin. (Rastgele için rast yazın.) >> ")
			if f == "pass" or f == "pw" or f == "password":
				change(n, t, FLAG_CHANGE_PASS)
			else:
				change(n, t, FLAG_CHANGE_USERNAME)

	elif "all" in komut and komut.index("all") == 0:
		printAllPasswords()
	
	elif komut == "help":
		print("add / hard / get (who) / delete (who) / change (who) (flag) (newValue) / all")

	elif komut == "cikis" or komut == "exit":
		print("Görüşmek üzere.")
		break