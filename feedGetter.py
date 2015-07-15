#! /usr/bin/env python
#encoding: utf8

import urllib2
from xml.dom import minidom



#Funcion que realiza iteraciones de los items(title, description) para imprimirlos
def getTextN(ItNode, node):
	d={"title":"* Título: ", "description":"- Descripción: "}
	text = ""
	for text_node in ItNode.childNodes:
		if (text_node.nodeType == node.TEXT_NODE):
			text += text_node.nodeValue
	if (len(text)>0):
		if(ItNode.nodeName != "link"):
			return "\n"+d[ItNode.nodeName]+"\n"+text+"\n"
		else:
			return text


#Funcion que itera los nodos de items
def getItems(chNode, items, node):
	feed = ""
	link = ""
	#Imprime la informacion de nodos encontrados en cada channel
	for inode in chNode.childNodes:
		if inode.nodeName in items:
			if (inode.nodeName != "link"):
				feed += getTextN(inode, node)
			else:
				link += getTextN(inode, node)
	return (feed, link)


#Funcion que recibe por parametro el urlrss y presenta la informacion
def getFeeds(url):
	feeds = []
	try:
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
								feed, link = getItems(channelNode,["title","description","link"], node)
								feeds.append((feed,link))
			else:
				print "No se pudo obtener el xml"
		else:
			print "Error obteniendo el url"
			
		if(len(feeds)>0):
			return feeds
		else:
			return "error"
	except:
		return "error"


