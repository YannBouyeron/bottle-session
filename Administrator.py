import hashlib
import numpy as np
from sqlite3 import *
from bottle import request, response 
import time








class Admi:
	
	"""Les objets instenciés à partir de cette classe permettent la gestion des sessions du coté administrateur"""
	
	def __init__(self, bd):
		
		self.bd = bd
		
		
		self.initable()
			
		self.site = 'My Site'
		self.mail = '<vous@hotmail.fr>' #Entrez ici l'adresse mail de gestion de votre site (mail outloock)
		self.password = '<mdp>' #Entrez ici votre mot de passe
		
		
	def connect(self):
		
		"""Connection à la base de données"""
		
		conn = connect(self.bd) 
		cur = conn.cursor() 
		return conn, cur
		
		
	def initable(self):
		
		"""Initiation de la table users si elle n'existe pas deja"""
		
		conn, cur = self.connect()
		cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, mdphash TEXT, mail TEXT, level INTEGER, inscriptionDate TEXT, lastLogin TEXT)") 
		
	
	
	
	###################### Acces aux informations de la table users #########################
		
	@property	
	def users_table(self):
		
		"""retourne une liste de tuple de la table users"""
		
		conn, cur = self.connect()
		cur.execute("SELECT * from users")
		users_table = cur.fetchall()
		return users_table
		
		
	@property	
	def id_liste(self):
		
		"""retourne une liste des id de la table users"""
		
		id_liste = [i[0] for i in self.users_table]
		return id_liste
		
		
	@property	
	def mail_liste(self):
		
		"""retourne une liste des mail de la table users"""
		
		mail_liste = [i[2] for i in self.users_table]
		return mail_liste
		
		
	def userinfobymail(self, mail):
		
		"""retourne les info d’un mail dans la table users"""
		
		conn, cur = self.connect()
		cur.execute("SELECT * from users WHERE mail = ?",(mail,))
		info = cur.fetchone()	
		
		return info
		
		
	def userinfobyid(self, id):
		
		"""retourne les info d’un id dans la table users"""
		
		conn, cur = self.connect()
		cur.execute("SELECT * from users WHERE id = ?",(id,))
		info = cur.fetchone()	
		
		return info
		
		
		
		
		
		
		
	###################### Gestion des comptes ##########################
	
	
		
	def creatuser(self, mail, level):
		
		"""Ajoute un user dans la base de donnée"""
		
		if mail not in self.mail_liste:
		
			#generation de son id
			try:
				id = max(self.id_liste) + 1
			except ValueError:
				id = 1
			
			#generation de son mdp
			mdp, mdphash = self.new_mdp()
			
			#envoi des info par email
			mess ='Voici vos identifiants de connexion au site {site}: \n Identifiant: {mail} \n Mot de passe: {mdp}'.format(mail=mail, mdp=mdp, site=self.site)
			self.sendmail (self.mail, mail, self.site , mess, self.password)
			
			date = time.asctime()
			
			#remplissage de la base de donnees
			conn, cur = self.connect()
			cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", (id, mdphash, mail, level, date, date))
			conn.commit()		
		
		
	def deletuserbymail(self, mail):
		"""supprime un user de la table users
		mail est le mail de l'user à supprimer
		"""
		conn, cur = self.connect()
		cur.execute("DELETE FROM users WHERE mail =?",(mail,))
		conn.commit()		
		
	
	def deletuser(self, id):
		"""supprime un user de la table users
		id est l'id de l'user (int) à supprimer
		"""
		conn, cur = self.connect()
		cur.execute("DELETE FROM users WHERE id =?",(id,))
		conn.commit()	
		
	
	def initmdp(self, user):
		
		"""
		reinitialisation du mdp d'un user
		user est un objet de la class User
		"""
		
		#generation de son nouveau mdp
		mdp, mdphash = self.new_mdp()
		
		#envoi des info par email
		mess ='Bonjour {nom} {prenom}, voici vos nouveaux identifiants de connexion au site {site}: \n Identifiant: {mail} \n Mot de passe: {mdp}'.format(nom= user.nom, prenom= user.prenom, mail=user.mail, mdp=mdp, site=self.site)
		self.sendmail (self.mail, user.mail, self.site , mess, self.password)
		
		#modification de la base de donnee
		conn, cur = self.connect()
		cur.execute("UPDATE users SET mdphash = '{xx}' WHERE id = {yy} ".format(xx = mdphash, yy = user.id,))
		conn.commit()
		
		
	def initialisemdp(self, mail):
		
		"""reinitialisation du mdp d'un user à partir de son mail"""
		
		if mail in self.mail_liste:
			
			#generation de son nouveau mdp
			mdp, mdphash = self.new_mdp()
			
			#envoi des info par email
			mess ='Bonjour {mail}, voici votre nouveau mot de passe: {mdp}'.format(mail=mail, mdp=mdp)
			self.sendmail (self.mail, mail, self.site , mess, self.password)
			
			#modification de la base de donnee
			conn, cur = self.connect()
			cur.execute("UPDATE users SET mdphash = '{xx}' WHERE mail = '{yy}' ".format(xx = mdphash, yy = mail))
			conn.commit()
			
			
	def setleveluser(self, id, level):
		
		"""modification du level d'un user"""
		
		#modification de la base de donnee
		conn, cur = self.connect()
		cur.execute("UPDATE users SET level = '{xx}' WHERE id = '{yy}' ".format(xx = level, yy = id))
		conn.commit()
	
	
	def setmailuser(self, id, mail):
		
		"""modification du mail d'un user"""
		
		#modification de la base de donnee
		conn, cur = self.connect()
		cur.execute("UPDATE users SET mail = '{xx}' WHERE id = '{yy}' ".format(xx = mail, yy = id))
		conn.commit()
		
				
		
			
	def modifpwd(self, mail, oldmdp, newmdp1, newmdp2):
		
		"""remplace le mdp par un nouvel mdp choisi par l'utilisateur
		c'est moins securisé qu'un mot de passe generé de maniere aleatoire"""
		
		
		if mail in self.mail_liste and hashlib.sha224(oldmdp.encode()).hexdigest() == self.userinfobymail(mail)[1] and newmdp1 == newmdp2:
			
			
			#modification de la base de donnee
			conn, cur = self.connect()
			cur.execute("UPDATE users SET mdphash = '{xx}' WHERE mail = '{yy}' ".format(xx = hashlib.sha224(newmdp1.encode()).hexdigest(), yy = mail))
			conn.commit()
			
		
		
	def new_mdp(self):
		
		"""genere un mdp et hash le mdp, return mdp et mdphash"""
		
		x = [chr(i) for i in list(range(48,58))+list(range(97,123))]
		mdp = np.random.choice(x , 10)
		mdp = ''.join(mdp) #conversion de la liste de str en str
		bmdp = bytes(mdp, 'utf8')
		
		mdphash = hashlib.sha224(bmdp).hexdigest()
		
		return mdp, mdphash
		
		
	
		
			
	############## Gestion des sessions ################				
		
	def login(self, mail, mdp, logokpath ='/', logfailpath = '/'):
		
		#hashage du mot de passe
		bmdp = mdp.encode()
		mdphash = hashlib.sha224(bmdp).hexdigest()
		
		if mail in self.mail_liste:
		
			#recuperation info user
			conn, cur = self.connect()
			cur.execute("SELECT * from users WHERE mail = ?",(mail,))
			info = cur.fetchone()
		
			#verification conformité mdphash
			if mdphash == info[1]:
		
				#envoi cookie id
				response.set_cookie("loged", info[0], secret="1234")
				
				date = time.asctime()
				
				#modification de la base de donnee
				conn, cur = self.connect()
				cur.execute("UPDATE users SET lastLogin = '{xx}' WHERE mail = '{yy}' ".format(xx = date, yy = mail))
				conn.commit()
					
				#redirection
				response.status = 303
				response.set_header('Location', logokpath)
			
			else:
				print('mdp error')
				response.status = 303
				response.set_header('Location', logfailpath)
		
		else:
			print('mail error')
			response.status = 303
			response.set_header('Location', logfailpath)
		
		
	def logout(self, redirection):
		
		uid = request.get_cookie("loged", secret="1234")
		
		response.set_cookie("loged", uid, secret="1234", expires=0)
		
		response.status = 303
		response.set_header('Location', redirection)	
		
		
	def new_user(self, id = None):
		
		"""creation d'un nouvel objet user instencié a partir de son id"""
		
		return User(id, self.bd)			
	
	
	def cheklog(self):
		
		"""verifie si un utilisateur est logué par recherche de son cokkie; crée un objet user contenant ses info"""
		
		uid = request.get_cookie("loged", secret="1234")

		if uid:
			
			uuu = self.new_user(uid)
			
			return uuu
			
			
	def restrictlevel(self, level, redirection = "/"):
		
		uuu = self.cheklog()
		
		if uuu == None or uuu.level != level:
			
			response.status = 303
			response.set_header('Location', redirection)	
		
		else:
			
			return uuu
			
	
	
	def restrictlevelsup(self, limit, redirection = "/"):
		
		uuu = self.cheklog()
		
		if uuu == None or uuu.level < limit or type(limit) != type(int()):
			
			response.status = 303
			response.set_header('Location', redirection)	
			
		else:
			
			return uuu
		
		
			
			
		
		
	
		
			
	
	################## send mail ###################
	
	def sendmail(self, de, to, sujet, mess, mdp):
	
		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		
		msg = MIMEMultipart()
		msg['From'] = de
		msg['To'] = to
		msg['Subject'] = sujet
		message = mess
		msg.attach(MIMEText(message))
		mailserver = smtplib.SMTP('smtp.live.com', 25)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		#identifianr et mot de passe de l'envoyeur
		mailserver.login(de, mdp)
		#adresse envoyeur et adresse destinataire
		mailserver.sendmail(de , to , msg.as_string())
		mailserver.quit()
		
	
			
		
			
		
	
	
		
			



	
		
class User:
	
	def __init__(self, id, bd):
		
		self.bd = bd
		self.id = id
		
	def connect(self):
		
		"""Connection à la base de données"""
		
		conn = connect(self.bd) 
		cur = conn.cursor() 
		return conn, cur	
	
	def infolt(self):
		
		"retourne toute la table sous forme d'une liste de tuple'"
		
		conn, cur = self.connect()
		cur.execute("SELECT * from users WHERE id = ?",(self.id,))
		return cur.fetchone()
		
	def info(self,attribu):
		
		x = self.infolt()
		t = ['id','mdphash','mail','level','inscriptionDate','lastLogin']
		n = t.index(attribu)
		
		return x[n]
		
		
	@property
	def mdph(self):
		x = self.infolt()
		return x[1]
		
	@property
	def mail(self):
		x = self.infolt()
		return x[2]
		
	@property
	def level(self):
		x = self.infolt()
		return x[3]
		
		
	@property
	def CreationAccount(self):
		x = self.infolt()
		return x[4]
		
	@property
	def lastLogin(self):
		x = self.infolt()
		return x[5]
	
	
	
		
