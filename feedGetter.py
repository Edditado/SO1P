#! /usr/bin/env python
#encoding: utf8

import urllib2
from xml.dom import minidom



#Funcion que realiza iteraciones de los items(title, description) para imprimirlos
def printTextN(ItNode, node):
	d={"title":"* Título: ", "description":"- Descripción: "}
	text = ""
	for text_node in ItNode.childNodes:
		if (text_node.nodeType == node.TEXT_NODE):
			text += text_node.nodeValue
	if (len(text)>0):
		return "\n"+d[ItNode.nodeName]+"\n"+text+"\n"


#Funcion que itera los nodos de items
def printItems(chNode, items, node):
	feed = ""
	#Imprime la informacion de nodos encontrados en cada channel
	for inode in chNode.childNodes:
		if inode.nodeName in items:
			feed += printTextN(inode, node)
	return feed


#Funcion que recibe por parametro el urlrss y presenta la informacion
def getFeeds(url):
	feeds = []
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
							feed = printItems(channelNode,["title","description"], node)
							feeds.append(feed)
		else:
			print "No se pudo obtener el xml"
	else:
		print "Error obteniendo el url"
	
	return feeds


