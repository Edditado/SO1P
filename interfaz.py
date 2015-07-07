#!/usr/bin/env python
#encoding: utf8

import gtk
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
        
        fileItem = gtk.MenuItem("Archivo")
        editItem = gtk.MenuItem("Edición")
        helpItem = gtk.MenuItem("Ayuda")
        
        fileMenu = gtk.Menu()
        addItem = gtk.MenuItem("Agregar RSS..")
        addItem.connect("activate", self.createAddWindow)
        fileMenu.append(addItem)   
        
        editMenu = gtk.Menu()
        edNameItem = gtk.MenuItem("Cambiar nombre")
        removeItem = gtk.MenuItem("Eliminar")
        editMenu.append(edNameItem)
        editMenu.append(removeItem) 
        
        helpMenu = gtk.Menu()
        aboutItem = gtk.MenuItem("Acerca de..")
        helpMenu.append(aboutItem)
             
        fileItem.set_submenu(fileMenu)
        editItem.set_submenu(editMenu)
        helpItem.set_submenu(helpMenu)

        self.menuBar.append(fileItem)
        self.menuBar.append(editItem)
        self.menuBar.append(helpItem)
        
        self.extContainer.pack_start(self.menuBar, expand=False)
        
        #Seccion de feeds
        self.container = gtk.HPaned()
        self.container.set_position(200)
                
        #Columna izquierda
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.selecTree = gtk.TreeView()
        self.selecTree.connect("row-activated", self.showFeeds)
        
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
        
        #Obtencion de Rss guardadas
        self.getSavedRss()
    	self.getSavedFeeds()


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
        #button.connect("clicked", self.getEntryText)
        
        form.pack_start(button, expand=False)
        container.pack_start(form, expand=False)
        
        self.addWindow.add(container)
        self.addWindow.show_all()
    
        
    """def getEntryText(self, widget):
    	url = self.entry.get_text()
    	self.addWindow.destroy()
    	
    	urlSplit = url.split("/")
    	if(urlSplit[0] == "http:" or urlSplit[0] == "https:"):
    		pag = urlSplit[2]
    		rss = urlSplit[len(urlSplit)-1].split(".")[0]
    		it = self.selecTreeStore.append(None, [pag])
    		print it
        	self.selecTreeStore.append(it, [rss])
        	
    		feeds = fg.getFeeds(url)
    		for feed in feeds:
    			self.feedsTreeStore.append(None, [feed])
    	
    	for parent in self.selecTreeStore:
    		self.selecTreeStore.append(parent.iter, ["oeoe"])
    		childs = parent.iterchildren()
    		for child in childs:
    			print child[0]"""
    
    
    def showFeeds(self, treeview, path, column):
    	model = treeview.get_model()
    	it = model.get_iter(path)
    	val = model.get_value(it, 0)
    	itp = model.iter_parent(it)
    	valp = ""
    	if (itp is not None):
    		valp = model.get_value(itp, 0)
    	
    	for pag, rss, feeds in self.rssList:
    		if(valp == pag and val == rss):
    			self.feedsStore.clear()
    			for feed in feeds:
    				self.feedsStore.append([feed])

	  
    def getSavedRss(self):
    	rssFile = open("rssDir.txt", "r")
    	for line in rssFile:
    		pagExist = False
    		urlSplit = line.split("/")
    		pag = urlSplit[2]
    		for treePag in self.selecTreeStore:
    			if(treePag[0] == pag):
    				rss = urlSplit[len(urlSplit)-1].split(".")[0]
    				self.selecTreeStore.append(treePag.iter, [rss])
    				pagExist = True
    	
    		if(not pagExist):
    			it = self.selecTreeStore.append(None, [pag])
    			rss = urlSplit[len(urlSplit)-1].split(".")[0]
    			self.selecTreeStore.append(it, [rss])
    		
    	rssFile.close()
    	self.selecTree.expand_all()
     
    
    def getSavedFeeds(self):
    	self.rssList = []
    	rssFile = open("rssDir.txt", "r")
    	for line in rssFile:
    		urlSplit = line.split("/")
    		pag = urlSplit[2]
    		rss = urlSplit[len(urlSplit)-1].split(".")[0]
    		feeds = fg.getFeeds(line)
    		self.rssList.append((pag, rss, feeds))
    	
    	rssFile.close()
    		
			
    







mainW = MainWindow()
gtk.main()
