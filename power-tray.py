#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib, AppIndicator3, GObject
import signal

class PowerProfileTrayApp:
    def __init__(self):
        self.app = 'power_profile_selector'
        self.indicator = AppIndicator3.Indicator.new(
            self.app,
            "preferences-system-power",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # Tray menüsü oluştur
        self.menu = Gtk.Menu()
        
        # Mevcut profil öğesi
        self.current_item = Gtk.MenuItem(label="Mevcut Profil: Yükleniyor...")
        self.current_item.set_sensitive(False)  # Tıklanamaz yap
        self.menu.append(self.current_item)
        
        # Ayırıcı
        separator = Gtk.SeparatorMenuItem()
        self.menu.append(separator)
        
        # Profil seçenekleri
        profiles = [
            ("Dengeli", "balanced"),
            ("Güç Tasarrufu", "power-saver"),
            ("Yüksek Performans", "performance")
        ]
        
        for name, profile in profiles:
            item = Gtk.MenuItem(label=name)
            item.connect("activate", self.on_profile_selected, profile)
            self.menu.append(item)
        
        # Çıkış öğesi
        exit_item = Gtk.MenuItem(label="Çıkış")
        exit_item.connect("activate", self.on_exit)
        self.menu.append(exit_item)
        
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        # Başlangıçta mevcut profili güncelle
        self.update_current_profile()
        
        # 30 saniyede bir otomatik güncelleme
        GObject.timeout_add_seconds(30, self.update_current_profile)
    
    def update_current_profile(self, *args):
        try:
            output = GLib.spawn_command_line_sync("powerprofilesctl get")[1].decode().strip()
            self.current_item.set_label(f"Mevcut Profil: {output}")
        except:
            self.current_item.set_label("Profil alınamadı")
        return True  # Timeout'un devam etmesi için
    
    def on_profile_selected(self, widget, profile):
        GLib.spawn_command_line_async(f"powerprofilesctl set {profile}")
        self.update_current_profile()
    
    def on_exit(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Ctrl+C için
    PowerProfileTrayApp()
    Gtk.main()
