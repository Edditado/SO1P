import gtk

actresses = [('Pagina1'), ('Pagina2'),
    ('Pagina3'), ('Pagina4'),
    ('Pagina5'), ('Pagina6' )]


class PyApp(gtk.Window): 
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_size_request(700, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        
        self.connect("destroy", gtk.main_quit)
        self.set_title("RSS")

        hbox = gtk.HBox(spacing=15)
        
        sw = gtk.ScrolledWindow()
        #sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        hbox.pack_start(sw, True, True, 0)

        store = self.create_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        sw.add(treeView)

        self.create_columns(treeView)
        
        """Seccion de Feeds"""
        self.hbox_busqueda = gtk.HBox(spacing = 2)
        
        self.label_buscar = gtk.Label("Buscar:")
        self.entry_buscar = gtk.Entry()
        self.sw_feeds = gtk.ScrolledWindow()
        
        self.hbox_busqueda.pack_start(self.label_buscar)
        self.hbox_busqueda.pack_start(self.entry_buscar)
        
        
        hbox.pack_start(self.sw_feeds, True, True, 0)
        
        vbox= gtk.VBox(False,0)
        vbox.pack_start(self.hbox_busqueda)
        vbox.pack_start(hbox)
        
        self.add(vbox)
        self.show_all()

	
    def create_model(self):
        store = gtk.ListStore(str)

        for act in actresses:
            store.append([act])
            print store

        return store


    def create_columns(self, treeView):
    
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Paginas", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
       


    def on_activated(self, widget, row, col):
       
        model = widget.get_model()
        text = model[row][0]
        print text



PyApp()
gtk.main()
