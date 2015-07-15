#!/usr/bin/env python
#encoding: utf8

import gtk
import threading
import feedGetter as fg

class MainWindow: 
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("RSS Reader")
        self.window.set_size_request(800, 500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", gtk.main_quit)        
        
        #Contenedor de MenuBar y Seccion de feeds   
        self.extContainer = gtk.VBox()
        
        #Creacion del menu
        self.menuBar = gtk.MenuBar()
        
        fileItem = gtk.MenuItem("Opciones")
        
        fileMenu = gtk.Menu()
        addItem = gtk.MenuItem("Agregar RSS..")
        addItem.connect("activate", self.createAddWindow)
        removeItem = gtk.MenuItem("Quitar RSS")
        #removeItem.connect("activate", self.removeRss)
        fileMenu.append(addItem)  
        fileMenu.append(removeItem) 
                            
        fileItem.set_submenu(fileMenu)
        self.menuBar.append(fileItem)
        self.extContainer.pack_start(self.menuBar, expand=False)
        
        #Seccion de feeds
        self.container = gtk.HPaned()
        self.container.set_position(200)
                
        #Columna izquierda
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.selecTree = gtk.TreeView()
        
        self.selecCol = gtk.TreeViewColumn("Fuentes")
        self.selecCol.set_alignment(0.5)
        self.selecCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        
        cell = gtk.CellRendererText()
        self.selecCol.pack_start(cell, False)
        self.selecCol.add_attribute(cell, "text", 0)
        self.selecTree.append_column(self.selecCol) 
        
        self.selecTreeStore = gtk.TreeStore(str)
        self.selecTree.set_model(self.selecTreeStore) 
        scrolled.add(self.selecTree)      
        self.container.add1(scrolled)
               
        # Columna derecha
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.feedsTree = gtk.TreeView()
        self.feedsTree.set_rules_hint(True)     

        self.feedsCol = gtk.TreeViewColumn("Feeds")
        self.feedsCol.set_alignment(0.5)
        self.feedsCol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
 
        cell = gtk.CellRendererText()
        self.feedsCol.pack_start(cell, False)
        self.feedsCol.add_attribute(cell, "text", 0)
        self.feedsTree.append_column(self.feedsCol)
        
        self.feedsStore = gtk.ListStore(str)            
        self.feedsTree.set_model(self.feedsStore)   
        scrolled.add(self.feedsTree)  
        self.container.add2(scrolled)
        
        self.extContainer.pack_start(self.container)
        	
        self.window.add(self.extContainer)
        
        self.window.show_all()
        
        #Arreglos necesarios
        self.rssList = []
        self.feeds = []
        self.feedLinks = []
        #Obtencion de Rss guardadas
        self.getSavedRss()


  	#Obtiene las url del archivo, separa su dominio y su archivo rss y los coloca en forma de arbol 
  	#en el panel izquierdo
    def getSavedRss(self):
    	rssFile = open("rssDir.txt", "r")
    	for line in rssFile:
    		pagExist = False
    		urlSplit = line.split("/")
    		pag = urlSplit[2]
    		rss = urlSplit[len(urlSplit)-1].split(".")[0]
    		for treePag in self.selecTreeStore:
    			if(treePag[0] == pag):
    				self.selecTreeStore.append(treePag.iter, [rss])
    				pagExist = True
    	
    		if(not pagExist):
    			it = self.selecTreeStore.append(None, [pag])
    			self.selecTreeStore.append(it, [rss])
    		    		
    		self.rssList.append((pag, rss, line))
    		
    	rssFile.close()
    	self.selecTree.expand_all()
    
    
    #Añade un nuevo Rss al panel izquierdo, y guarda su url en el archivo
    def saveNewRss(self, btn):
    	url = self.entry.get_text()
    	feeds = fg.getFeeds(url)
    	if(feeds == "error"):
    		messagedialog = gtk.MessageDialog(self.addWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Fuente de RSS no válida")
    		messagedialog.run()
    		messagedialog.destroy()
    	else:
    		pagExist = False
    		urlSplit = url.split("/")
    		pag = urlSplit[2]
    		rss = urlSplit[len(urlSplit)-1].split(".")[0]
    		for treePag in self.selecTreeStore:
    			if(treePag[0] == pag):
    				self.selecTreeStore.append(treePag.iter, [rss])
    				pagExist = True
    	
    		if(not pagExist):
    			it = self.selecTreeStore.append(None, [pag])
    			self.selecTreeStore.append(it, [rss])
    			
    		self.rssList.append((pag, rss, url))
    		rssFile = open("rssDir.txt", "a")
    		rssFile.write(url+"\n")
    		rssFile.close()
    		self.addWindow.destroy()
    
    """
    #Remueve un Rss del panel izquierdo y del archivo
    def removeRss(self, widget):
    	parent = False
    	toRemove = []
    	selection = self.selecTree.get_selection()
    	model, it = selection.get_selected()

    	val = model.get_value(it, 0)
    	itp = model.iter_parent(it)
    	valp = ""
    	
    	if (itp is None):
    		parent = True
    	else:
    		valp = model.get_value(itp, 0)
    	
    	if(parent):
    		for pag, rss, url in self.rssList:
    			if(val == pag):
    				toRemove.append(url)
    				self.rssList.remove((pag, rss, url))
    	else:
    		for pag, rss, url in self.rssList:
    			if(valp == pag and val == rss):
    				toRemove.append(url)
    				self.rssList.remove((pag, rss, url))
    	
    	f = open("rssDir.txt","r")
    	lines = f.readlines()
    	f.close()
    	
    	for line in lines:
    		for url in toRemove:
  				if line == url:
  					lines.remove(line)
   				
    	f = open("rssDir.txt","w")
    	f.writelines(lines)
    	f.close()
    	    	
    	self.selecTreeStore.remove(it)
    """		
    
    
    #Creacion de la ventana para Agregar Rss
    def createAddWindow(self, widget):
    	self.addWindow = gtk.Window()
        self.addWindow.set_title("Agregar RSS")
        self.addWindow.set_size_request(500, 100)
        self.addWindow.set_position(gtk.WIN_POS_CENTER)
        self.addWindow.connect("destroy", lambda w: gtk.main_quit)
        
        container = gtk.VBox()
        
        label = gtk.Label("Ingrese URL del RSS:")
        align = gtk.Alignment(0,0,0,0)
        align.set_padding(25,0,0,0)
        align.add(label)
        container.pack_start(align, expand=False)
        
        form = gtk.HBox(False, 5)       
        self.entry = gtk.Entry()
        form.pack_start(self.entry)     
        button = gtk.Button("Agregar") 
        button.connect("clicked", self.saveNewRss)
        
        form.pack_start(button, expand=False)
        container.pack_start(form, expand=False)
        
        self.addWindow.add(container)       
        self.addWindow.show_all()
    		
			
    



mainW = MainWindow()
gtk.main()
