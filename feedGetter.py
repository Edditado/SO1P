#! /usr/bin/env python
import urllib2
from xml.dom import minidom



#Funcion que realiza iteraciones de los items(title, description) para imprimirlos
def printTextN(ItNode, node):
	d={"title":"* Titulo: ", "description":"- Descripcion: "}
	text = ""
	for text_node in ItNode.childNodes:
		if (text_node.nodeType == node.TEXT_NODE):
			text += text_node.nodeValue
	if (len(text)>0):
		print d[ItNode.nodeName]
		print text
		print ""





#Funcion que itera los nodos de items
def printItems(chNode, items, node):
	#Imprime la informacion de nodos encontrados en cada channel
	for inode in chNode.childNodes:
		if inode.nodeName in items:
			printTextN(inode, node)
	print "\n"





#Funcion que recibe por parametro el urlrss y presenta la informacion
def getFeeds(url):
	# Obtencion de los datos de un url
	urlData = urllib2.urlopen(url)
	if (urlData):
		# Transformacion los datos del url a un xml
		xmldoc = minidom.parse(urlData)
		if (xmldoc):
			# Obtencion del nodo raiz del xml
			rootNode=xmldoc.documentElement
			# Iteracion de los nodos hijos del nodo raiz
			for node in rootNode.childNodes:
			#Obtencion de los nodos tipo <channel>
				if(node.nodeName=="channel"):
					for channelNode in node.childNodes:
						# Obtencion de los "Feeds"
						if (channelNode.nodeName == "item"):
							printItems(channelNode,["title","description"], node)
		else:
			print "No se pudo obtener el xml"
	else:
		print "Error obteniendo el url"

			







#Funcion main que inicia el programa
def main():
	#Llamada a la funcion getFeeds con el link rss xml
	getFeeds('http://www.calendario.espol.edu.ec/index.php/rss')



main()
