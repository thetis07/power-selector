#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class PowerProfileSelector(Gtk.Window):
    def __init__(self):
        super().__init__(title="Güç Profili Seçici")
        self.set_default_size(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER)  # Pencereyi ekranın ortasında aç
        
        # Ana dikey kutu
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_valign(Gtk.Align.CENTER)  # Dikeyde ortala
        vbox.set_halign(Gtk.Align.CENTER)  # Yatayda ortala
        self.add(vbox)
        
        # Mevcut profil etiketi (ortalanmış)
        self.current_label = Gtk.Label(label="Current Profile: Loading...")
        self.current_label.set_halign(Gtk.Align.CENTER)  # Yatayda ortala
        vbox.pack_start(self.current_label, False, False, 0)
        
        # Butonlar için dikey kutu
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        btn_box.set_valign(Gtk.Align.CENTER)
        btn_box.set_halign(Gtk.Align.CENTER)
        
        profiles = [
            ("Balanced", "balanced"),
            ("Power Saver", "power-saver"),
            ("Performance", "performance")
        ]
        
        # Butonları oluştur ve ortala
        for name, profile in profiles:
            btn = Gtk.Button(label=name)
            btn.set_halign(Gtk.Align.CENTER)  # Buton içeriğini ortala
            btn.set_size_request(150, 40)  # Buton boyutunu ayarla
            btn.connect("clicked", self.on_profile_selected, profile)
            btn_box.pack_start(btn, False, False, 5)
        
        vbox.pack_start(btn_box, False, False, 0)
        self.update_current_profile()
    
    def update_current_profile(self):
        try:
            output = GLib.spawn_command_line_sync("powerprofilesctl get")[1].decode().strip()
            self.current_label.set_markup(f"<b>Current Profile:</b> {output}")
        except:
            self.current_label.set_text("Profil alınamadı")
    
    def on_profile_selected(self, button, profile):
        GLib.spawn_command_line_async(f"powerprofilesctl set {profile}")
        self.update_current_profile()

win = PowerProfileSelector()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
