import gtk


class PyApp(gtk.Window): 
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_size_request(400, 300)
        self.set_position(gtk.WIN_POS_CENTER)
        
        self.connect("destroy", gtk.main_quit)
        self.set_title("Tree")
        
        box1 = gtk.HBox()
        
        tree = gtk.TreeView()
	
        
        languages = gtk.TreeViewColumn()
        languages.set_title("Selector")
 
        cell = gtk.CellRendererText()
        languages.pack_start(cell, True)
        languages.add_attribute(cell, "text", 0)
 
        treestore = gtk.TreeStore(str)
 
        it = treestore.append(None, ["Pag1"])
        treestore.append(it, ["Rss11"])
        treestore.append(it, ["Rss12"])
        treestore.append(it, ["Rss13"])
        treestore.append(it, ["Rss14"])
 
        it = treestore.append(None, ["Pag2"])
        treestore.append(it, ["Rss21"])
        treestore.append(it, ["Rss22"])
        treestore.append(it, ["Rss23"])
        treestore.append(it, ["Rss24"])
 
        tree.append_column(languages)
        tree.set_model(treestore)
        
        box1.pack_start(tree)
        
        tree2 = gtk.TreeView()
        tree2.set_rules_hint(True)     

        feeds = gtk.TreeViewColumn()
        feeds.set_title("Feeds")
 
        cell = gtk.CellRendererText()
        feeds.pack_start(cell, True)
        feeds.add_attribute(cell, "text", 0)
        
        treestore2 = gtk.TreeStore(str)
	   
	treestore2.append(None, ["Feed1\nOeoeoeoeoe"])
        treestore2.append(None, ["Feed2\nJjahdkjashdjkhasdkas"])
        
        tree2.append_column(feeds)
        tree2.set_model(treestore2)
        box1.pack_start(tree2)
	

        self.add(box1)
        self.show_all()

    

PyApp()
gtk.main()
