#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
import os
import json
import socket
import gettext
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gegl', '0.4')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gimp, GimpUi, Gegl, Gtk, Gdk, GObject, GLib
import sys

class PseudoAdjustmentLayer(Gimp.PlugIn):
    
    GIMP_OFFICIAL_MENU = [
        ("Colors", [
            ("gimp:color-balance", "Color Balance"), ("gegl:color-temperature", "Color Temperature"),
            ("gimp:hue-chroma", "Hue-Chroma"), ("gimp:hue-saturation", "Hue-Saturation"),
            ("gegl:saturation", "Saturation"), ("gegl:exposure", "Exposure"),
            ("gegl:shadows-highlights", "Shadows-Highlights"), ("gimp:brightness-contrast", "Brightness-Contrast"),
            ("gimp:levels", "Levels"), ("gimp:curves", "Curves"),
            ("gegl:invert-linear", "Linear Invert"), ("gegl:value-invert", "Value Invert"),
            ("gimp:threshold", "Threshold"), ("gimp:colorize", "Colorize"), ("gimp:posterize", "Posterize"),
            ("gegl:color-to-alpha", "Color to Alpha"), ("gegl:color-overlay", "Color Overlay"),
            ("gegl:color-warp", "Color Warp"), ("gegl:dither", "Dither"),
            ("gegl:rgb-clip", "RGB Clip"), ("gegl:local-threshold", "Local Threshold"),
            ("Components", [("gegl:channel-mixer", "Channel Mixer"), ("gegl:component-extract", "Extract Component"), ("gegl:mono-mixer", "Mono Mixer")]),
            ("Desaturate", [("gimp:desaturate", "Desaturate"), ("gegl:mono-mixer", "Mono Mixer"), ("gegl:sepia", "Sepia")]),
            ("Map", [("gegl:alien-map", "Alien Map"), ("gegl:color-exchange", "Color Exchange"), ("gegl:rotate-colors", "Rotate Colors")]),
            ("Tone mapping", [("gegl:fattal02", "Fattal et al. 2002"), ("gegl:mantiuk06", "Mantiuk 2006")])
        ]),
        ("Blur", [
            ("gegl:focus-blur", "Focus Blur"), ("gegl:gaussian-blur", "Gaussian Blur"), ("gegl:lens-blur", "Lens Blur"),
            ("gegl:mean-curvature-blur", "Mean Curvature Blur"), ("gegl:median-blur", "Median Blur"), ("gegl:pixelize", "Pixelize"),
            ("gegl:selective-gaussian-blur", "Selective Gaussian Blur"), ("gegl:variable-blur", "Variable Blur"),
            ("gegl:motion-blur-circular", "Circular Motion Blur"), ("gegl:motion-blur-linear", "Linear Motion Blur"),
            ("gegl:motion-blur-zoom", "Zoom Motion Blur"), ("gegl:tileable-blur", "Tileable Blur")
        ]),
        ("Enhance", [
            ("gegl:antialias", "Antialias"), ("gegl:deinterlace", "Deinterlace"), ("gegl:high-pass", "High Pass"),
            ("gegl:noise-reduction", "Noise Reduction"), ("gegl:red-eye-removal", "Red Eye Removal"),
            ("gegl:snn-mean", "Symmetric Nearest Neighbor"), ("gegl:unsharp-mask", "Sharpen (Unsharp Mask)"),
            ("gegl:despeckle", "Despeckle"), ("gegl:nl-filter", "NL Filter")
        ]),
        ("Distorts", [
            ("gegl:apply-lens", "Apply Lens"), ("gegl:emboss", "Emboss"), ("gegl:engrave", "Engrave"),
            ("gegl:lens-distortion", "Lens Distortion"), ("gegl:kaleidoscope", "Kaleidoscope"), ("gegl:mosaic", "Mosaic"),
            ("gegl:newsprint", "Newsprint"), ("gegl:polar-coordinates", "Polar Coordinates"), ("gegl:ripple", "Ripple"),
            ("gegl:shift", "Shift"), ("gegl:spherize", "Spherize"), ("gegl:value-propagate", "Value Propagate"),
            ("gegl:video-degradation", "Video Degradation"), ("gegl:waves", "Waves"), ("gegl:whirl-pinch", "Whirl and Pinch"), ("gegl:wind", "Wind")
        ]),
        ("Light and Shadow", [
            ("gegl:bevel", "Bevel"), ("gegl:bloom", "Bloom"), ("gegl:drop-shadow", "Drop Shadow"), 
            ("gegl:inner-glow", "Inner Glow"), ("gegl:lens-flare", "Lens Flare"), 
            ("gegl:long-shadow", "Long Shadow"), ("gegl:supernova", "Supernova"), ("gegl:vignette", "Vignette")
        ]),
        ("Noise", [
            ("gegl:noise-cie-lch", "CIE lch Noise"), ("gegl:noise-hsv", "HSV Noise"), ("gegl:noise-hurl", "Hurl"),
            ("gegl:noise-pick", "Pick"), ("gegl:noise-rgb", "RGB Noise"), ("gegl:noise-slur", "Slur"), ("gegl:noise-spread", "Spread")
        ]),
        ("Edge-Detect", [
            ("gegl:difference-of-gaussians", "Difference of Gaussians"), ("gegl:edge", "Edge"), ("gegl:edge-laplace", "Laplace"),
            ("gegl:edge-neon", "Neon"), ("gegl:edge-sobel", "Sobel"), ("gegl:image-gradient", "Image Gradient")
        ]),
        ("Generic", [
            ("gegl:convolution-matrix", "Convolution Matrix"), ("gegl:distance-transform", "Distance Map"),
            ("gegl:layer-style", "Layer Style"), ("gegl:layer-styles", "Layer Styles"), ("gegl:normal-map", "Normal Map"), 
            ("gegl:dilate", "Dilate"), ("gegl:erode", "Erode")
        ]),
        ("Combine", [("gegl:depth-merge", "Depth Merge")]),
        ("Artistic", [
            ("gegl:apply-canvas", "Apply Canvas"), ("gegl:cartoon", "Cartoon"), ("gegl:cubism", "Cubism"),
            ("gegl:glass-tile", "Glass Tile"), ("gegl:oilify", "Oilify"), ("gegl:photocopy", "Photocopy"),
            ("gegl:slic", "Simple Linear Iterative Clustering"), ("gegl:softglow", "Softglow"),
            ("gegl:waterpixels", "Waterpixels"), ("gegl:clothify", "Clothify"), ("gegl:weave", "Weave")
        ]),
        ("Map", [
            ("gegl:bump-map", "Bump Map"), ("gegl:displace", "Displace"), ("gegl:fractal-trace", "Fractal Trace"),
            ("gegl:illusion", "Illusion"), ("gegl:little-planet", "Little Planet"), ("gegl:panorama-projection", "Panorama Projection"),
            ("gegl:recursive-transform", "Recursive Transform"), ("gegl:paper-tile", "Paper Tile"), ("gegl:tile-seamless", "Tile Seamless")
        ]),
        ("Render", [
            ("gegl:checkerboard", "Checkerboard"), ("gegl:grid", "Grid"), ("gegl:maze", "Maze"), ("gegl:plasma", "Plasma"),
            ("gegl:noise-solid", "Solid Noise"), ("gegl:sinus", "Sinus"), ("gegl:noise-cell", "Cell Noise"),
            ("gegl:noise-perlin", "Perlin Noise"), ("gegl:noise-simplex", "Simplex Noise")
        ])
    ]

    def do_query_procedures(self):
        return ["python-pseudo-adjustment-layer-v71"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        procedure.set_image_types("*")
        procedure.set_documentation("Simulates Adjustment Layers in GIMP 3 using NDE groups.", "Simulates Adjustment Layers.", name)
        procedure.set_menu_label("Pseudo Adjustment Layer")
        procedure.add_menu_path('<Image>/Filters/')
        return procedure

    def _gettext_translate(self, text, target_lang):
        domains = ["gimp30", "gegl-0.4", "gimp30-std-plug-ins"]
        locale_dirs = [None, "/app/share/locale", "/usr/share/locale", "/usr/local/share/locale"]
        for d in domains:
            for ld in locale_dirs:
                try:
                    t = gettext.translation(d, localedir=ld, languages=[target_lang])
                    res = t.gettext(text)
                    if res and res != text: return res.replace("...", "")
                except Exception: continue
        return text

    def load_or_generate_translation(self, lang_code):
        lang_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Language")
        try:
            if not os.path.exists(lang_dir): os.makedirs(lang_dir)
        except Exception: pass
        
        lang_file = os.path.join(lang_dir, f"{lang_code}.json")
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f: return json.load(f)
            except Exception: pass
        
        trans_data = {"categories": {}, "filters": {}}

        def _collect(menu):
            for name, items in menu:
                lc = self._gettext_translate(name, lang_code)
                trans_data["categories"][name] = {"en": name, "local": lc}
                for item in items:
                    if isinstance(item[1], list): _collect([item])
                    else:
                        op, en = item
                        lf = self._gettext_translate(en, lang_code)
                        trans_data["filters"][op] = {"en": en, "local": lf}
                        
        _collect(self.GIMP_OFFICIAL_MENU)
        
        trans_data["categories"]["Hidden"] = {"en": "Hidden", "local": self._gettext_translate("Hidden", lang_code)}
        trans_data["categories"]["Others"] = {"en": "Others", "local": self._gettext_translate("Others", lang_code)}
        
        try:
            with open(lang_file, 'w', encoding='utf-8') as f: json.dump(trans_data, f, indent=4, ensure_ascii=False)
        except Exception: pass
        return trans_data

    def load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f: return json.load(f)
            except Exception: pass
        return default

    def save_json(self, path, data):
        try:
            with open(path, 'w') as f: json.dump(data, f, indent=4)
        except Exception: pass

    def _flatten_menu_ops(self, menu):
        ops = set()
        for _, items in menu:
            for item in items:
                if isinstance(item[1], list): ops.update(self._flatten_menu_ops([item]))
                else: ops.add(item[0])
        return ops

    def fetch_and_save_filters(self):
        gegl_ops = set(Gegl.list_operations())
        filters = []
        all_planned = self._flatten_menu_ops(self.GIMP_OFFICIAL_MENU)
        for op in all_planned:
            if op.startswith("gimp:") or op in gegl_ops: filters.append(op)
            
        for op in gegl_ops:
            if op not in all_planned and not op.startswith("gimp:") and not op.startswith("gegl:"):
                filters.append(op)
                
        self.save_json(self.filters_file, filters)
        return filters

    def load_filter_list(self):
        if os.path.exists(self.filters_file):
            try:
                with open(self.filters_file, 'r') as f:
                    saved_list = json.load(f)
                    valid_ops = self._flatten_menu_ops(self.GIMP_OFFICIAL_MENU)
                    return [f for f in saved_list if (f in valid_ops or not f.startswith("gimp:") and not f.startswith("gegl:"))]
            except Exception: pass
        return self.fetch_and_save_filters()

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables: return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error())
        self.lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: self.lock_socket.bind(("127.0.0.1", 54321))
        except socket.error: return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        GimpUi.init("python-pseudo-adjustment-layer")
        Gegl.init(None)

        self.image, self.drawable = image, drawables[0]
        base = os.path.dirname(os.path.abspath(__file__))
        self.fav_file = os.path.join(base, "pal_favorites.json")
        self.hist_file = os.path.join(base, "pal_history.json")
        self.filters_file = os.path.join(base, "pal_filters.json")
        self.config_file = os.path.join(base, "pal_config.json")
        self.hidden_file = os.path.join(base, "pal_hidden.json")
        
        self.favorites = self.load_json(self.fav_file, [])
        self.history = self.load_json(self.hist_file, [])
        self.hidden_filters = self.load_json(self.hidden_file, [])
        self.config = self.load_json(self.config_file, {"target_lang": "ja", "translate_active": False, "auto_close": True})
        
        self.available_filters = self.load_filter_list()
        self.current_translation = self.load_or_generate_translation(self.config["target_lang"])

        self.window = Gtk.Window(title="Pseudo Adjustment Layer")
        self.window.set_default_size(350, 600)
        self.window.set_keep_above(True)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)
        try: GimpUi.window_set_transient(self.window)
        except Exception: pass

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_vbox.set_border_width(10)
        self.window.add(main_vbox)
        
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        row1.pack_start(Gtk.Label(label="Translate filter names"), False, False, 0)
        
        self.sw_trans = Gtk.Switch()
        self.sw_trans.set_active(self.config["translate_active"])
        self.sw_trans.connect("notify::active", self.on_translate_toggled)
        row1.pack_end(self.sw_trans, False, False, 0)
        
        self.btn_lang = Gtk.Button(label="🌐 Select")
        self.btn_lang.connect("clicked", self.on_select_language_clicked)
        row1.pack_end(self.btn_lang, False, False, 5)
        
        main_vbox.pack_start(row1, False, False, 0)
        
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row2.pack_start(Gtk.Label(label="Auto-close on apply"), False, False, 0)
        self.sw_close = Gtk.Switch()
        self.sw_close.set_active(self.config["auto_close"])
        self.sw_close.connect("notify::active", self.on_autoclose_toggled)
        row2.pack_end(self.sw_close, False, False, 0)
        main_vbox.pack_start(row2, False, False, 0)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect("search-changed", self.on_search_changed)
        main_vbox.pack_start(self.search_entry, False, False, 0)

        self.store = Gtk.TreeStore(str, str)
        self.filter_model = self.store.filter_new()
        self.filter_model.set_visible_func(self.filter_tree_visible)
        
        self.treeview = Gtk.TreeView(model=self.filter_model)
        self.treeview.set_headers_visible(False)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-press-event", self.on_tree_button_press)
        self.treeview.connect("row-expanded", self.on_row_expanded)
        self.treeview.connect("row-collapsed", self.on_row_collapsed)
        self.treeview.append_column(Gtk.TreeViewColumn("Filter", Gtk.CellRendererText(), markup=0))

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.treeview)
        main_vbox.pack_start(scroll, True, True, 0)
        
        self.btn_reset = Gtk.Button(label="🔄 Reset List")
        self.btn_reset.connect("clicked", self.on_reset_filters_clicked)
        main_vbox.pack_start(self.btn_reset, False, False, 0)

        self.populate_tree()
        self.window.show_all()
        Gtk.main()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def populate_tree(self):
        self.store.clear()
        av, hi, tr = set(self.available_filters), set(self.hidden_filters), self.config["translate_active"]
        
        def _add_node(parent, items, is_hidden=False, level=0):
            for name, content in items:
                indent = "    " * level
                if isinstance(content, list):
                    lc = self.current_translation["categories"].get(name, {}).get("local", name) if tr else name
                    if name == "Hidden": markup = f"{indent}🌚 <span foreground='#bdbdbd'>{lc}</span>"
                    elif name == "Others": markup = f"{indent}🧩 {lc}"
                    else:
                        emoji = "▶️" if level == 0 else "⏩"
                        markup = f"{indent}{emoji} {lc}"
                        
                    node = self.store.append(parent, [markup, ""])
                    _add_node(node, content, is_hidden, level + 1)
                    if not self.store.iter_has_child(node): self.store.remove(node)
                else:
                    if name in av:
                        if is_hidden or name not in hi:
                            self.store.append(parent, [f"{indent}    {self.get_op_name_for_dialog(name)}", name])

        fav = self.store.append(None, ["⭐ Favorites", ""])
        for op in self.favorites:
            if op not in hi: self.store.append(fav, [f"    {self.get_op_name_for_dialog(op)}", op])
        if not self.store.iter_has_child(fav): self.store.remove(fav)

        hist = self.store.append(None, ["📝 History", ""])
        for op in self.history:
            if op not in hi: self.store.append(hist, [f"    {self.get_op_name_for_dialog(op)}", op])
        if not self.store.iter_has_child(hist): self.store.remove(hist)

        _add_node(None, self.GIMP_OFFICIAL_MENU)
        
        official_ops = self._flatten_menu_ops(self.GIMP_OFFICIAL_MENU)
        other_ops = [op for op in av if op not in official_ops and op not in hi]
        if other_ops:
            _add_node(None, [("Others", [(op, op) for op in sorted(other_ops)])])

        if self.hidden_filters:
            _add_node(None, [("Hidden", [(op, op) for op in self.hidden_filters])], is_hidden=True)

    def update_node_icon(self, model, treeiter, is_expanded):
        try:
            child_iter = model.convert_iter_to_child_iter(treeiter)
            val = self.store.get_value(child_iter, 0)
            if val:
                if is_expanded:
                    new_val = val.replace("▶️", "🔽").replace("⏩", "⏬")
                else:
                    new_val = val.replace("🔽", "▶️").replace("⏬", "⏩")
                if val != new_val:
                    self.store.set_value(child_iter, 0, new_val)
        except Exception: pass

    def on_row_expanded(self, tv, it_expanded, path):
        self.update_node_icon(tv.get_model(), it_expanded, True)
        if self.search_entry.get_text(): return
        model = tv.get_model()
        parent = model.iter_parent(it_expanded)
        it = model.iter_children(parent)
        while it:
            if model.get_path(it).to_string() != path.to_string(): tv.collapse_row(model.get_path(it))
            it = model.iter_next(it)

    def on_row_collapsed(self, tv, it_collapsed, path):
        self.update_node_icon(tv.get_model(), it_collapsed, False)

    def on_row_activated(self, tv, path, col):
        res = tv.get_selection().get_selected()
        if res and res[1]:
            op = res[0].get_value(res[1], 1)
            if op: self.selected_op_name = op; self.apply_filter(None)
            else: tv.collapse_row(path) if tv.row_expanded(path) else tv.expand_row(path, False)

    def apply_filter(self, widget):
        if not self.selected_op_name: return
        dr = self.image.get_selected_drawables()
        if not dr: return
        target, res = dr[0], self.treeview.get_selection().get_selected()
        if not res or not res[1]: return
        raw = res[0].get_value(res[1], 0).strip()
        dn = raw.split('>')[-1].split('<')[0].strip() if '<' in raw else raw.strip()

        self.image.undo_group_start()
        g = Gimp.GroupLayer.new(self.image)
        g.set_name(f"fx: {dn}")
        g.set_mode(Gimp.LayerMode.PASS_THROUGH)
        self.image.insert_layer(g, target.get_parent(), self.image.get_item_position(target))
        
        d = Gimp.Layer.new(self.image, "DUMMY", self.image.get_width(), self.image.get_height(), Gimp.ImageType.RGBA_IMAGE, 100.0, Gimp.LayerMode.NORMAL)
        d.fill(getattr(Gimp.FillType, 'TRANSPARENT', 3))
        self.image.insert_layer(d, g, 0)
        
        try:
            p_clear = Gimp.get_pdb().lookup_procedure('gimp-drawable-edit-clear')
            if p_clear:
                c_clear = p_clear.create_config()
                c_clear.set_property('drawable', d)
                p_clear.run(c_clear)
        except Exception: pass
        
        try:
            p = Gimp.get_pdb().lookup_procedure('gimp-selection-is-empty')
            c = p.create_config(); c.set_property('image', self.image)
            if not p.run(c).index(1):
                m = g.create_mask(Gimp.AddMaskType.SELECTION); g.add_mask(m)
                pn = Gimp.get_pdb().lookup_procedure('gimp-selection-none')
                cn = pn.create_config(); cn.set_property('image', self.image); pn.run(cn)
        except Exception: pass

        try:
            fn = Gimp.DrawableFilter.new(g, self.selected_op_name, dn)
            g.append_filter(fn)
        except Exception:
            self.image.remove_layer(g)
            self.image.undo_group_end()
            return
        
        try: g.set_expanded(False)
        except Exception: pass
        
        if self.selected_op_name in self.history: self.history.remove(self.selected_op_name)
        self.history.insert(0, self.selected_op_name)
        self.history = self.history[:10]
        self.save_json(self.hist_file, self.history)
        
        self.image.undo_group_end()
        Gimp.displays_flush()
        
        if self.config["auto_close"]: Gtk.main_quit()
        else: self.refresh_tree()

    def get_op_name_for_dialog(self, op):
        tr = self.config["translate_active"]
        if op in self.current_translation["filters"]: 
            return self.current_translation["filters"][op]["local" if tr else "en"]
            
        # Othersフォルダなどの未知のフィルタにNamespaceを表示させる処理
        if ":" in op:
            namespace, name = op.split(':', 1)
            formatted_name = name.replace('-', ' ').title()
            if namespace not in ["gimp", "gegl"]:
                return f"{namespace}: {formatted_name}"
            return formatted_name
            
        return op.replace('-', ' ').title()
        
    def on_translate_toggled(self, sw, ps): self.config["translate_active"] = sw.get_active(); self.save_json(self.config_file, self.config); self.refresh_tree()
    def on_autoclose_toggled(self, sw, ps): self.config["auto_close"] = sw.get_active(); self.save_json(self.config_file, self.config)
    def on_search_changed(self, se): 
        self.filter_model.refilter()
        if se.get_text(): self.treeview.expand_all() 
        else: self.treeview.collapse_all()
    
    def filter_tree_visible(self, m, i, d):
        q = self.search_entry.get_text().lower()
        if not q: return True
        
        txt = m.get_value(i, 0).lower()
        op = (m.get_value(i, 1) or "").lower()
        
        # 子要素がマッチするか再帰的にチェック
        ci = m.iter_children(i)
        while ci:
            if self.filter_tree_visible(m, ci, d):
                return True
            ci = m.iter_next(ci)
            
        # 自身がマッチするか（フォルダそのものは検索対象から外す）
        is_folder = not op
        if not is_folder and (q in txt or q in op):
            return True
            
        return False

    def on_tree_button_press(self, tv, ev):
        if ev.button == 3:
            pi = tv.get_path_at_pos(int(ev.x), int(ev.y))
            if pi:
                tv.set_cursor(pi[0], pi[1], 0)
                res = tv.get_selection().get_selected()
                if res and res[1] and res[0].get_value(res[1], 1):
                    op, m = res[0].get_value(res[1], 1), Gtk.Menu()
                    f = Gtk.MenuItem(label="❌ Remove Fav" if op in self.favorites else "⭐ Add Fav")
                    f.connect("activate", lambda w, o: (self.favorites.remove(o) if o in self.favorites else self.favorites.append(o), self.save_json(self.fav_file, self.favorites), self.refresh_tree())[1], op); m.append(f)
                    m.append(Gtk.SeparatorMenuItem())
                    h = Gtk.MenuItem(label="♻️ Restore" if op in self.hidden_filters else "🌚 Hide")
                    h.connect("activate", lambda w, o: (self.hidden_filters.remove(o) if o in self.hidden_filters else self.hidden_filters.append(o), self.save_json(self.hidden_file, self.hidden_filters), self.refresh_tree())[1], op); m.append(h)
                    m.show_all(); m.popup_at_pointer(ev)
            return True
        return False

    def refresh_tree(self):
        expanded_names = []
        model = self.treeview.get_model()
        if model:
            def save_expanded(m, path, it, data):
                if self.treeview.row_expanded(path):
                    val = m.get_value(it, 0).replace("🔽", "▶️").replace("⏬", "⏩")
                    expanded_names.append(val)
            model.foreach(save_expanded, None)

        self.populate_tree()
        self.filter_model.refilter()

        model = self.treeview.get_model()
        if model and expanded_names:
            def restore_expanded(m, path, it, data):
                if m.get_value(it, 0) in expanded_names:
                    self.treeview.expand_row(path, False)
            model.foreach(restore_expanded, None)
    
    def on_reset_filters_clicked(self, w):
        dialog = Gtk.MessageDialog(transient_for=self.window, flags=Gtk.DialogFlags.MODAL, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.OK_CANCEL, text="Reset List?")
        dialog.format_secondary_text("This will re-initialise the filter list and reload translations. It may take a few seconds.")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            raw_filters = self.fetch_and_save_filters()
            valid_filters = []
            temp_image = Gimp.Image.new(10, 10, Gimp.ImageBaseType.RGB)
            for op in raw_filters:
                if op.startswith("gimp:"):
                    valid_filters.append(op)
                    continue
                try:
                    temp_group = Gimp.GroupLayer.new(temp_image)
                    temp_image.insert_layer(temp_group, None, 0)
                    temp_dummy = Gimp.Layer.new(temp_image, "DUMMY", 10, 10, Gimp.ImageType.RGBA_IMAGE, 100.0, Gimp.LayerMode.NORMAL)
                    temp_dummy.fill(getattr(Gimp.FillType, 'TRANSPARENT', 3))
                    temp_image.insert_layer(temp_dummy, temp_group, 0)
                    test_node = Gimp.DrawableFilter.new(temp_group, op, op)
                    temp_group.append_filter(test_node)
                    if len(temp_group.get_filters()) > 0: valid_filters.append(op)
                except Exception: pass
                finally:
                    try: temp_image.remove_layer(temp_group)
                    except Exception: pass
            temp_image.delete()
            self.available_filters = valid_filters
            self.save_json(self.filters_file, self.available_filters)
            
            self.favorites = [f for f in self.favorites if f in valid_filters]
            self.save_json(self.fav_file, self.favorites)
            self.history = [f for f in self.history if f in valid_filters]
            self.save_json(self.hist_file, self.history)
            self.hidden_filters = [f for f in self.hidden_filters if f in valid_filters]
            self.save_json(self.hidden_file, self.hidden_filters)
            
            self.current_translation = self.load_or_generate_translation(self.config["target_lang"])
            self.refresh_tree()
            info = Gtk.MessageDialog(transient_for=self.window, flags=Gtk.DialogFlags.MODAL, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Process Complete")
            info.run()
            info.destroy()

    def on_select_language_clicked(self, w):
        dialog = Gtk.Dialog(title="Language", transient_for=self.window, flags=Gtk.DialogFlags.MODAL)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL); dialog.add_button("OK", Gtk.ResponseType.OK); dialog.set_default_size(300, 450)
        lang_list = [("ar", "Arabic"), ("ast", "Asturian"), ("az", "Azerbaijani"), ("be", "Belarusian"), ("bg", "Bulgarian"), ("br", "Breton"), ("bs", "Bosnian"), ("ca", "Catalan"), ("cs", "Czech"), ("da", "Danish"), ("de", "German"), ("dz", "Dzongkha"), ("el", "Greek"), ("en_CA", "English (CA)"), ("en_GB", "English (GB)"), ("eo", "Esperanto"), ("es", "Spanish"), ("et", "Estonian"), ("eu", "Basque"), ("fa", "Persian"), ("fi", "Finnish"), ("fr", "French"), ("ga", "Irish"), ("gl", "Galician"), ("gu", "Gujarati"), ("he", "Hebrew"), ("hi", "Hindi"), ("hr", "Croatian"), ("hu", "Hungarian"), ("id", "Indonesian"), ("is", "Icelandic"), ("it", "Italian"), ("ja", "Japanese"), ("ka", "Georgian"), ("kab", "Kabyle"), ("kk", "Kazakh"), ("km", "Khmer"), ("kn", "Kannada"), ("ko", "Korean"), ("lt", "Lithuanian"), ("lv", "Latvian"), ("mk", "Macedonian"), ("mr", "Marathi"), ("ms", "Malay"), ("my", "Burmese"), ("nb", "Norwegian (Bokmål)"), ("ne", "Nepali"), ("nl", "Dutch"), ("nn", "Norwegian (Nynorsk)"), ("oc", "Occitan"), ("pa", "Punjabi"), ("pl", "Polish"), ("pt", "Portuguese"), ("pt_BR", "Portuguese (Brazil)"), ("ro", "Romanian"), ("ru", "Russian"), ("rw", "Kinyarwanda"), ("sk", "Slovak"), ("sl", "Slovenian"), ("sr", "Serbian"), ("sv", "Swedish"), ("ta", "Tamil"), ("te", "Telugu"), ("th", "Thai"), ("tr", "Turkish"), ("uk", "Ukrainian"), ("vi", "Vietnamese"), ("zh_CN", "Chinese (Simplified)"), ("zh_HK", "Chinese (Hong Kong)"), ("zh_TW", "Chinese (Traditional)")]
        store = Gtk.ListStore(str, str)
        for code, name in lang_list: store.append([code, name])
        tree = Gtk.TreeView(model=store); tree.append_column(Gtk.TreeViewColumn("Language", Gtk.CellRendererText(), text=1))
        scroll = Gtk.ScrolledWindow(); scroll.add(tree); dialog.get_content_area().pack_start(scroll, True, True, 0); dialog.get_content_area().show_all()
        if dialog.run() == Gtk.ResponseType.OK:
            m, ti = tree.get_selection().get_selected()
            if ti:
                self.config["target_lang"] = m.get_value(ti, 0); self.save_json(self.config_file, self.config)
                self.current_translation = self.load_or_generate_translation(self.config["target_lang"])
                if self.config["translate_active"]: self.refresh_tree()
        dialog.destroy()

if __name__ == '__main__': Gimp.main(PseudoAdjustmentLayer.__gtype__, sys.argv)