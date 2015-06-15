#! /usr/bin/env python
import urllib2
from xml.dom import minidom

# Obtencion de los datos de un url
urlData = urllib2.urlopen('http://www.calendario.espol.edu.ec/index.php/rss')

if (urlData):
	# Transformacion los datos del url a un xml
	xmlDoc = minidom.parse(urlData)
	if (xmlDoc):
		# Obtencion del nodo raiz del xml
		rootNode = xmlDoc.documentElement
		# Iteracion de los nodos hijos del nodo raiz
		for node in rootNode.childNodes:
			# Obtencion de los nodos de tipo <channel>
			if(node.nodeName == "channel"):
				for channelNode in node.childNodes:
					# Obtencion de los "Feeds"
					if (channelNode.nodeName == "item"):
						for itemNode in channelNode.childNodes:
							if (itemNode.nodeName == "title"):
								# Obtencion del titulo
								print "* Titulo:"
								title = ""
								for textNode in itemNode.childNodes:
									if (textNode.nodeType == node.TEXT_NODE):
										title += textNode.nodeValue
								# Impresion del titulo
								if (len(title)>0):
									print title

							if (itemNode.nodeName == "description"):
								# Obtencion de la descripcion
								print "- Descripcion:"
								description = ""
								for textNode in itemNode.childNodes:
									if (textNode.nodeType == node.TEXT_NODE):
										description += textNode.nodeValue
								# Impresion de la descripcion
								if (len(description)>0):
									print description + "\n"
									
	else:
		print "No se pudo obtener el XML...\n"
else:
	print "Error obteniendo el URL...\n"

