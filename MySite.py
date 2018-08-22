from bottle import *
from Administrator import *
from Formulator import *
import json



#creation d'un objet Form() pour la gestion simplifiée des formulaires html
fff = Form()



#creation de l'application bottle
app = Bottle()




#gestion du css
@app.route('/static/<filepath:path>')
def send_static(filepath):
	return static_file(filepath, root='./static/')
	
	
	
	
@app.route('/')
def index():
	
	#création d'un objet administrateur de base de données
	adm = Admi("mabd")
	
	uuu = adm.cheklog()
	
	
	if uuu == None:
		
		#bouton lien inscription
		inscription = fff.bouton_lien("/inscription", "get", "inscription", "", "Inscription")
	
		#bouton lien connexion 
		login = fff.bouton_lien("/login", "get", "login", "", "Connexion")
		
		#bouton vers page level 3
		lev = fff.bouton_lien("/level3", "get", "level3", "", "espace réservé aux users de level supérieur à 3")
		
		return inscription, login, lev
	
		
	else:
		
		logout = fff.bouton_lien("/logout", "post", "logout", "", "Deconnexion")
		
		compte = fff.bouton_lien("/compt", "post", "compt", "", uuu.mail)
		
		#bouton vers page level 3
		lev = fff.bouton_lien("/level3", "get", "level3", "", "espace réservé aux users de level supérieur à 3")
		
		return logout, compte, lev
		
	
	
	
#gestion des inscriptions
@app.get('/inscription')
def inscription():
	
	ins = fff.formulaire("/inscription", "post", "Envoyer", mail=("Mail", "email"))
	
	return ins

@app.post('/inscription')	
def inscription_traitement():
	
	adm = Admi("mabd")
	
	mail = request.forms.get("mail")
	
	mail = mail.lower()
	mail = mail.strip()
	
	
	if mail in adm.mail_liste:
		
		acceuil = fff.bouton_lien("/", "get", "", "", "Retour à l'acceuil")
		
		return "Vous possédez déjà un compte lié à ce mail", acceuil
		
	else:
	
		level = 0
		
		adm.creatuser(mail, level)
		
		acceuil = fff.bouton_lien("/", "get", "", "", "Retour à l'acceuil")
		
		return "Vous allez recevoir votre mot de passe à l'adresse {0}".format(mail), acceuil	
			

		
		
#gestion des connections

	
#login
@app.get('/login')
def login():
	
	
	log = fff.formulaire("/login", "post", "Envoyer", mail=("Mail", "email"), mdp=("Mot de passe", "password"))
	
	loose_login = fff.bouton_lien("/init_login", "post", "init_login", "", "Mot de passe oublié ! réinitialisez le.")
	
	return log, loose_login
	

@app.post('/login')	
def login_traitement():
	
	mail = request.forms.get("mail")
	
	mail = mail.lower()
	mail = mail.strip()
	
	mdp = request.forms.get("mdp")
	
	adm = Admi("mabd")
	
	adm.login(mail = mail, mdp = mdp, logokpath ='/', logfailpath = '/')
	
	
	
	
	
	
#réinitialisation du mot de passe	
@app.post('/init_login')
def init_login():
	
	
	ins = fff.formulaire("/init_login_traitement", "post", "Envoyer", mail=("Mail", "email"))
	
	return ins
	
	
@app.post("/init_login_traitement")
def init_login_traitement():
	
	adm = Admi("mabd")

	mail = request.forms.get("mail")
	
	mail = mail.lower()
	mail = mail.strip()
	
	adm.initialisemdp(mail)
	
	acceuil = fff.bouton_lien("/", "get", "", "", "Retour à l'acceuil")
	
	return "Vous allez recevoir votre nouveau mot de passe à l'adresse {0}".format(mail), acceuil
	
	
		
		

#logout
@app.post('/logout')
def logout():
	
	adm = Admi("mabd")
	
	adm.logout('/')
	
	
	
	
#suppression compte
@app.post('/delet_account')
def delete_account():
	
	adm = Admi("mabd")
	
	user = adm.cheklog()
	
	adm.deletuser(user.id)
	
	adm.logout()
	

#compte user
@app.post('/compt')
def compt():
	
	del_account = fff.bouton_lien("/delet_account", "post", "", "", "Supprimer votre compte")
	
	modif_pwd = fff.bouton_lien("/modif_pwd", "post", "", "", "Modifier votre mot de passe")
	
	
	return del_account, modif_pwd
	
	
#modif mdp
@app.post('/modif_pwd')
def modifpwd():
	
	mpwd = fff.formulaire("/modif_pwd_trait", "post", "Envoyer", opwd = ("opwd", "password"), npwd1 = ("npwd1", "password"), npwd2 = ("npwd2", "password"))
	
	return mpwd

@app.post('/modif_pwd_trait')
def modipwdtrait():

	adm = Admi("mabd")
	
	user = adm.cheklog()
	
	opwd = request.forms.get("opwd")
	
	npwd1 = request.forms.get("npwd1")
	
	npwd2 = request.forms.get("npwd2")
	
	adm.modifpwd(user.mail, opwd, npwd1, npwd2)

	response.status = 303
	response.set_header('Location', '/')







############################################ Administrateur ####################################




# acces administateur 
@app.route('/acces', method = ('POST','GET'))
def acces():
	
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") == "accessok":
		
		#bouton configuration compte administrateur
		bconfig = fff.bouton("/config_acces", "post", "config", "", "Configuration des identifiants administrateur", classe = '')
		
		#bouton set & get user
		fsetgetuserbymail = fff.formulaire("/setgetuser", "post", "Voir ou modifier un user", mail=("mail", "email"))
		
		#bouton liste user mail
		bgetmaillist = fff.bouton("/mail_list", "post", "maillist", "", "Liste des mails des users", classe = "")
		
		bshowbd = fff.bouton("/show_bd", "post", "showbd", "", "Explorer la base de données", classe = "")
		
		
		return bconfig, fsetgetuserbymail, bgetmaillist, bshowbd
		
	
	elif request.method == 'GET':
		
		login = fff.formulaire('/acces', 'post', 'Envoyer', **{"name":("name", "text"), "password":("mot de passe","password")})
		
		return login
		
		
	elif request.method == 'POST':
		
		#recuperation des données du formulaire et hashage du pwd
		name = request.forms.get("name")
		pwd = request.forms.get("password")
		hpwd = hashlib.sha256(pwd.encode()).hexdigest()
		
		
		#recuperation des références jsonisée
		with open("config.txt", "r") as fp:
			conf = json.load(fp)
		
		nref = conf["name"]
		href = conf["pwd"]
		
		
		#comparaison
		if name.lower() == nref.lower() and hpwd == href:
			response.set_cookie("access", "accessok", secret="fzhiufhzehfziuefziuefauhefhaouhfa", max_age=3000)
			
		response.status = 303
		response.set_header('Location', '/acces')
		

@app.post("/config_acces")
def config_acces():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
		
	#formulaire changement name et pwd
	configform = fff.formulaire("/config_acces_trait", "post", "Envoyer", name = ("Nom", "TEXT"), pwd1 = ("Password", "PASSWORD"), pwd2 = ("Password Confirmation", "PASSWORD"))
			
	return configform



@app.post("/config_acces_trait")
def config_acces_trait():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	#recuperation des données du formulaire
	name = request.forms.get("name")
	pwd1 = request.forms.get("pwd1")
	pwd2 = request.forms.get("pwd2")
	
	#comparaison des pwd
	if pwd1 != pwd2:
		return "Error password"
	
	#hashage du mot de passe
	hpwd = hashlib.sha256(pwd1.encode()).hexdigest()
	
	#recuperation du dictionnaire de configuration
	with open("config.txt", "r") as fp:	
		
		try:
			conf = json.load(fp)
			
		except json.decoder.JSONDecodeError as err:
			conf = {}
			print(err)
		
	#modification du dictionnaire de configuration
	conf["name"] = name
	conf["pwd"] = hpwd
	
	with open("config.txt", "w") as fp:
		json.dump(conf, fp)
	
	
@app.post("/setgetuser")
def setgetuser():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	adm = Admi("mabd")
	
	mail = request.forms.get("mail")
	
	infoUser = adm.userinfobymail(mail)
	
	line = """<tr><td>{0}</td><td><label for = "mail"></label><input name = "mail" id = "mail" type = "email" value = "{1}"/></td><td><label for = "level"></label><input name = "level" id = "level" type = "int" value = "{2}"/></td></tr>""".format(infoUser[0], infoUser[2], infoUser[3])
	
	table = """<form action="/setuser" accept-charset="ISO-8859-1" method="post"><table><caption></caption><tr><th>ID</th><th>Mail</th><th>Level</th></tr>{line}</table><input name = "id" type = "hidden", value = "{id}"/><input value = "Envoyer" type="submit" /></form>""".format(mail = mail, line = line, id = infoUser[0])
	
	#bouton supprimer
	suppr = fff.bouton("/suppr", "post", "suppr", infoUser[0], "Supprimer le compte", classe = "")
	table += "<div>{0}</div>".format(suppr)
	
	#bouton retour acces
	back = fff.bouton("/acces", "post", "back", "", "Retour", classe = '')
	table += "<div>{0}</div>".format(back)
	
	return template("table.html", table = table)
	
	
@app.post("/setuser")
def setuser():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	id = request.forms.get('id')
	
	mail = request.forms.get("mail")
	
	level = request.forms.get("level")
	
	adm = Admi("mabd")
	
	adm.setleveluser(id, level)
	
	adm.setmailuser(id, mail)
	
	response.status = 303
	response.set_header('Location', '/acces')
	

@app.post("/suppr")
def suppr():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	id = request.forms.get("suppr")
	
	adm = Admi("mabd")
	
	adm.deletuser(id)
	
	response.status = 303
	response.set_header('Location', '/acces')
	
	
	
	
	
@app.post("/mail_list")
def mailiste():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	adm = Admi("mabd")
	
	x = adm.mail_liste
	
	
	#bouton retour acces
	
	back = fff.bouton("/acces", "post", "back", "", "Retour", classe = '')
	
			
	return " ".join(x), back
	
@app.post("/show_bd")
def showbd():
	
	if request.get_cookie("access", secret="fzhiufhzehfziuefziuefauhefhaouhfa") != "accessok":
		response.status = 303
		response.set_header('Location', '/acces')
	
	
	adm = Admi("mabd")
	
	x = adm.mail_liste
	
	bdhtml = """<table><caption></caption><tr><th>ID</th><th>Mail</th><th>Level</th><th>Creation Account</th><th>Last login</th></tr>"""
	
	for mail in x:
		
		infoUser = adm.userinfobymail(mail)
	
		line = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>""".format(infoUser[0], infoUser[2], infoUser[3], infoUser[4], infoUser[5])
	
		bdhtml += line
		
	bdhtml += """</table>"""
	
	
	#bouton retour acces
	back = fff.bouton("/acces", "post", "back", "", "Retour", classe = '')
	bdhtml += """<div>{0}</div>""".format(back)
	
	return template("table.html", table = bdhtml)
	
		
		
	
	
############################## page reservée aux users de level == 3 #################

@app.route("/level3")
def level3():
	
	adm = Admi("mabd")
	
	user = adm.restrictlevel(3)
	
	if user != None:
	
		return "salut {0} tu es de niveau 3".format(user.mail)
	
	
	
	
	
app.run(host='0.0.0.0', port=27200, reload=True, debug=True)
	
