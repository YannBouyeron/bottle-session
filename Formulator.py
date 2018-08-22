import sys

class Form:
	
	
	def __init__(self):
		
		self.btn_link = """
	border:none;
	outline:none;
	background:none;
	cursor:pointer;
	color:#0000EE;
	padding:0;
	text-decoration:underline;
	font-family:inherit;
	font-size:inherit;
	"""
	
		self.lienblanc = """
	border:none;
	outline:none;
	background:none;
	cursor:pointer;
	color:#FAF0E6;
	padding:0;
	text-decoration:underline;
	font-family:inherit;
	font-size:inherit;
	"""
		
		self.iconecss = """
	background-image:url("/img/opo.gif");
	top right no-repeat;
	width: 16px;
	height: 16px;
	padding: 0 0 0 10px;
	border-width: 0px;
	background-color:#ffffff;
	cursor: pointer;
	border:0;
	"""
		
		self.icone = """
	border-width: 0px;
	background-color:#ffffff;
	"""
		
		
	#formulaires automatiques	
		
	def formulaire(self, action, method, value, **name_labeltype):
		
		
		"""
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			value = value du bouton d'envoi du formulaire
			**name_labeltype est un dico : {'name':('label','type')}
			
		Exemple:
			
			>>> f = Form()
			>>> mon_form = f.formulaire('/login', 'post', 'Envoyer', **{"pseudo":("pseudo", "text"), "mail":("mail", "email"), "mdp":("mot de passe","password")})
			>>> mon_form
			'<form action="/login" accept-charset="ISO-8859-1" method="post"> <label for=pseudo>pseudo:</label><input name = "pseudo" id = "pseudo" type = "text" /></br> <label for=mail>mail:</label><input name = "mail" id = "mail" type = "email" /></br> <label for=mdp>mot de passe:</label><input name = "mdp" id = "mdp" type = "password" /></br> <input value = "Envoyer" type="submit" />   </form>'
			
		Attention, en python < 3.6 le dico n'est pas ordonné
		
		"""
		
		k = name_labeltype.keys()
		
		if len(k) > 1:

			q = " ".join(["""<label for={n}>{t}:</label><input name = "{n}" id = "{n}" type = "{ty}" /></br>""".format(t = name_labeltype[j][0], n = j, ty = name_labeltype[j][1])for j in k])

		else:
			
			
			q = " ".join(["""<label for={n}>{t}:</label><input name = "{n}" id = "{n}" type = "{ty}" />""".format(t = name_labeltype[j][0], n = j, ty = name_labeltype[j][1])for j in k])

		f = """<form action="{0}" accept-charset="ISO-8859-1" method="{1}"> {2} <input value = "{3}" type="submit" />   </form>""".format(action, method, q, value)
		
		return f
		
	def text(self, action, method, label, name, bouton, value, rows=5, cols=10):
		
		"""
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			label = titre qui s'affiche au dessus de la zone de saisie
			bouton = value du bouton d'envoi du formulaire
			value = contenu par defaut (attention ce n'est pas un placeholder)
			rows = nombre de lignes
			cols = nombre de colonnes
		
		Exemple:
			>>> f = Form()
			>>> t = f.text('/redaction', 'post', 'Editeur', 'text1', 'envoyer', 'Il etait une fois...')
			>>> t
			'<form method="post" action="/redaction" accept-charset="Windows-1256"><p><label for="text1">Editeur</label><br/><textarea name="text1" id="text1" rows="5" cols="10" wrap="virtual">Il etait une fois...</textarea></p><input type="submit" value="envoyer"/></form>'
			
		"""
		
		return """<form method="{method}" action="{action}" accept-charset="ISO-8859-1"><p><label for="{name}">{label}</label><br/><textarea name="{name}" id="{name}" rows="{rows}" cols="{cols}" wrap="virtual" style="overflow:scroll;">{value}</textarea></p><input type="submit" value="{bouton}"/></form>""".format(action=action, method=method, label=label, name=name, bouton=bouton, value=value, rows=rows, cols=cols)
	
		
	#boutons automatiques			
		
	def boutimp(self, action, method, name, value, classe = ''):
		
		"""
		C'est un "faux" bouton, ou bouton de type input dont la value transmise est la value d'affichage du bouton.
		
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			name = nom du bouton
			value = value du bouton
			class = css class
		
		Exemple:
			
			>>> f = Form()
			>>> b = f.boutimp("/logout", "post", "bout_log_out", "Logout" )
			>>> b
			'<form action = "/logout" method = "post"> <input type = "submit" name = "bout_log_out" value = "Logout" style = ""/> </form>'
		"""
		
		return """<form action = "{0}" method = "{1}" accept-charset="ISO-8859-1"> <input type = "submit" name = "{2}" value = "{3}" class = "{4}"/> </form>""".format(action, method, name, value, classe)
		
		
	def bouton(self, action, method, name, value, label, classe = ''):
		
		"""
		C'est un "vrai" bouton dont la value transmise peut etre différente de la value d'affichage du bouton
		
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			name = nom du bouton
			value = str transmise avec le bouton
			label = label qui s'affiche dans le bouton
			class = css class
		"""
		
		
		return """<form action="{0}" method="{1}" accept-charset="ISO-8859-1"> <button type="submit" name="{2}" value="{3}" class = "{5}">{4}</button></form>""".format(action, method, name, value, label, classe)
		
		
	def bouton_lien(self, action, method, name, value, label):
		
		"""
		C'est un "vrai" bouton (dont la value transmise peut etre différente de la value d'affichage du bouton) déguisé en lien html.
		
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			name = nom du bouton
			value = str transmise avec le bouton
			label = label qui s'affiche dans le bouton
			class = css class
		"""
		
		return """<form action="{0}" method="{1}" accept-charset="ISO-8859-1"> <button type="submit" name="{2}" value="{3}" style = "{5}" >{4}</button></form>""".format(action, method, name, value, label, self.btn_link)
		
		
	def bouton_lienb(self, action, method, name, value, label):
		
		"""
		C'est un "vrai" bouton (dont la value transmise peut etre différente de la value d'affichage du bouton) déguisé en lien html blanc.
		
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			name = nom du bouton
			value = str transmise avec le bouton
			label = label qui s'affiche dans le bouton
			class = css class
		"""
		
		return """<form action="{0}" method="{1}" accept-charset="ISO-8859-1"> <button type="submit" name="{2}" value="{3}" style = "{5}" >{4}</button></form>""".format(action, method, name, value, label, self.lienblanc)
	
	
	
	
	#liste deroulante automatique
	
	def listder(self, action, method, name, label, classe = '', bout = 'Envoyer', **value_txt):
		
		"""
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			name = nom de la liste
			label = label affiché au dessus des cases a cocher
			**value_txt associe les noms des champs de la liste au text des champs de la liste.
		
		Attention:
			
			en python3.6 les champs sont dans l'ordre du dico
			en python<3.6 les chanps sont dans l'ordre alphabetique
		"""
		
		k = value_txt.keys()
		
		if sys.version_info < (3,6):
			
			k = sorted(k)
		
		q = " ".join(["""<option value="{v}">{t}</option>""".format(v = i, t = value_txt[i]) for i in k])
		
		
	
		return """<form action="{0}" method="{1}" accept-charset="ISO-8859-1"><label for="{2}">{3}</label><select name="{2}" id={2} class="{4}">{q}</select><input type="submit" value="{5}"/></form>""".format(action, method, name, label, classe, bout, q=q)
	
			
							
	#cases automatiques
					
	def case(self, action, method, label, value='Envoyer', **namevalue):
		
		"""
		Arguments:
			
			action = route à laquelle serra envoyé le formulaire
			methode = post (ou get)
			value = value du bouton d'envoi
			label = label affiché au dessus des cases a cocher
			**namevalue = dico associant les noms des cases et leur value qui s'affiche
		
		Exemple:
			
			f = Form()
			mes_cases = f.case('/traitcase', 'post', 'cochez des cases', paris='Paris', rome='Rome', dakar='Dakar')
		"""

		x = " ".join(["""<input type="checkbox" name="{n}" value="{m}" id="{n}" /> <label for="{n}">{m}</label><br/>""".format(n = i, m = namevalue[i]) for i in namevalue.keys()])
	
		return """<form action="{0}" method="{1}" accept-charset="ISO-8859-1"> {2} <br/> {3} <input value="{4}" type="submit" /> </form>""".format(action, method, label, x, value)
		
		


