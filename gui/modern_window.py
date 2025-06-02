import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import psutil
import json
import os
import threading
from typing import Optional, Dict, Any, List
from datetime import datetime
import configparser

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernForceBindIPGUI:
    """Modern GUI application for ForceBindIP with rounded corners and sleek design"""
    
    def __init__(self):
        # Create main window
        self.root = ctk.CTk()
        self.root.title("ForceBindIP Launcher")
        self.root.geometry("1500x1000")
        self.root.minsize(1200, 800)
        
        # Configure window
        self.root.configure(fg_color=("#f0f0f0", "#1a1a1a"))
        
        # Application data
        self.config_file = "forcebindip_config.json"
        self.forcebindip_path = ""
        self.network_interfaces = []
        self.saved_configs = []
        
        # Load configuration
        self.load_configuration()
        
        # Create modern interface
        self.create_modern_widgets()
        
        # Initialize data
        self.refresh_all_data()
    
    def create_modern_widgets(self):
        """Create the modern GUI widgets with rounded corners"""
        
        # Modern header with gradient-like appearance
        self.header_frame = ctk.CTkFrame(
            self.root,
            height=80,
            corner_radius=0,
            fg_color=("#ffffff", "#2b2b2b"),
            border_width=0
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Title section
        self.title_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color=("#ffffff", "#2b2b2b")
        )
        self.title_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Main title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="🌐 ForceBindIP Launcher",
            font=ctk.CTkFont(family="SF Pro Display", size=28, weight="bold"),
            text_color=("#000000", "#ffffff")
        )
        self.title_label.pack(side="left")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Force Applications to Use Specific Network Interfaces",
            font=ctk.CTkFont(family="SF Pro Display", size=14),
            text_color=("#666666", "#999999")
        )
        self.subtitle_label.pack(side="left", padx=(20, 0))
        
        # Modern status indicator
        self.status_frame = ctk.CTkFrame(
            self.title_frame,
            fg_color=("#e8f5e8", "#1a3d1a"),
            corner_radius=20,
            border_width=1,
            border_color=("#d4edda", "#28a745")
        )
        self.status_frame.pack(side="right", padx=10)
        
        # Status indicator with modern design
        self.status_container = ctk.CTkFrame(
            self.status_frame,
            fg_color=("#e8f5e8", "#1a3d1a")
        )
        self.status_container.pack(padx=15, pady=8)
        
        # Status dot
        self.status_dot = ctk.CTkLabel(
            self.status_container,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color=("#28a745", "#40ff40")
        )
        self.status_dot.pack(side="left", padx=(0, 8))
        
        self.status_label = ctk.CTkLabel(
            self.status_container,
            text="Ready",
            font=ctk.CTkFont(family="SF Pro Display", size=12, weight="bold"),
            text_color=("#28a745", "#40ff40")
        )
        self.status_label.pack(side="left")
        
        # Main content area with rounded corners
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color=("#f8f9fa", "#1e1e1e"),
            border_width=1,
            border_color=("#e9ecef", "#404040")
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Modern tabview with rounded corners
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            corner_radius=15,
            border_width=0,
            fg_color=("#f8f9fa", "#1e1e1e"),
            segmented_button_fg_color=("#e9ecef", "#2d2d2d"),
            segmented_button_selected_color=("#007bff", "#0066cc"),
            segmented_button_selected_hover_color=("#0056b3", "#004999"),
            text_color=("#495057", "#ffffff"),
            text_color_disabled=("#6c757d", "#666666")
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create modern tabs
        self.create_launcher_tab()
        self.create_interfaces_tab()
        self.create_configurations_tab()
        self.create_settings_tab()
        self.create_monitoring_tab()
    
    def create_modern_button(self, parent, text, command, style="primary", width=140, height=35):
        """Create a modern button with rounded corners"""
        colors = {
            "primary": ("#007bff", "#0066cc"),
            "success": ("#28a745", "#22c55e"),
            "warning": ("#ffc107", "#f59e0b"),
            "danger": ("#dc3545", "#ef4444"),
            "secondary": ("#6c757d", "#64748b")
        }
        
        hover_colors = {
            "primary": ("#0056b3", "#004999"),
            "success": ("#1e7e34", "#16a34a"),
            "warning": ("#e0a800", "#d97706"),
            "danger": ("#c82333", "#dc2626"),
            "secondary": ("#545b62", "#475569")
        }
        
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=12,
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold"),
            fg_color=colors.get(style, colors["primary"]),
            hover_color=hover_colors.get(style, hover_colors["primary"]),
            border_width=0
        )
    
    def create_modern_frame(self, parent, transparent=False):
        """Create a modern frame with rounded corners"""
        if transparent:
            return ctk.CTkFrame(
                parent,
                fg_color=("#f8f9fa", "#1e1e1e"),
                corner_radius=0
            )
        else:
            return ctk.CTkFrame(
                parent,
                corner_radius=15,
                fg_color=("#ffffff", "#2d2d2d"),
                border_width=1,
                border_color=("#dee2e6", "#404040")
            )
    
    def create_modern_scrollable_frame(self, parent):
        """Create a modern scrollable frame"""
        return ctk.CTkScrollableFrame(
            parent,
            corner_radius=15,
            fg_color=("#ffffff", "#2d2d2d"),
            border_width=1,
            border_color=("#dee2e6", "#404040"),
            scrollbar_fg_color=("#f8f9fa", "#1e1e1e"),
            scrollbar_button_color=("#6c757d", "#64748b"),
            scrollbar_button_hover_color=("#495057", "#475569")
        )

    def create_launcher_tab(self):
        """Create application launcher tab"""
        self.tabview.add("🚀 Launcher")
        launcher_tab = self.tabview.tab("🚀 Launcher")
        
        # Modern control panel
        control_frame = self.create_modern_frame(launcher_tab)
        control_frame.pack(fill="x", pady=(0, 20))
        
        # Control panel title
        control_title = ctk.CTkLabel(
            control_frame,
            text="🎮 Application Launcher",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        control_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Controls container
        controls_container = ctk.CTkFrame(control_frame, fg_color=("#ffffff", "#2d2d2d"))
        controls_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Application selection row
        app_row = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        app_row.pack(fill="x", pady=(15, 10))
        
        app_label = ctk.CTkLabel(
            app_row, 
            text="📱 Application:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        app_label.pack(side="left", padx=(0, 10))
        
        self.app_path_var = tk.StringVar()
        self.app_entry = ctk.CTkEntry(
            app_row,
            textvariable=self.app_path_var,
            placeholder_text="Select an application to launch...",
            width=400,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=11)
        )
        self.app_entry.pack(side="left", padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            app_row,
            text="📁 Browse",
            command=self.browse_application,
            width=100,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#17a2b8", "#20c997"),
            hover_color=("#138496", "#1ab394")
        )
        browse_btn.pack(side="left", padx=(0, 10))
        
        # Network interface selection row
        interface_row = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        interface_row.pack(fill="x", pady=(0, 10))
        
        interface_label = ctk.CTkLabel(
            interface_row, 
            text="🌐 Network Interface:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        interface_label.pack(side="left", padx=(0, 10))
        
        self.interface_var = tk.StringVar()
        self.interface_combo = ctk.CTkComboBox(
            interface_row,
            variable=self.interface_var,
            width=350,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=11),
            state="readonly"
        )
        self.interface_combo.pack(side="left", padx=(0, 20))
        
        # Refresh interfaces button
        refresh_interfaces_btn = ctk.CTkButton(
            interface_row,
            text="🔄",
            command=self.refresh_network_interfaces,
            width=35,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=16),
            fg_color=("#17a2b8", "#20c997"),
            hover_color=("#138496", "#1ab394")
        )
        refresh_interfaces_btn.pack(side="left", padx=(0, 20))
        
        # Arguments and options row
        options_row = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        options_row.pack(fill="x", pady=(0, 15))
        
        args_label = ctk.CTkLabel(
            options_row, 
            text="⚙️ Arguments:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        args_label.pack(side="left", padx=(0, 10))
        
        self.args_var = tk.StringVar()
        args_entry = ctk.CTkEntry(
            options_row,
            textvariable=self.args_var,
            placeholder_text="Optional command line arguments",
            width=200,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=11)
        )
        args_entry.pack(side="left", padx=(0, 20))
        
        # Architecture selection
        arch_label = ctk.CTkLabel(
            options_row, 
            text="🏗️ Architecture:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        arch_label.pack(side="left", padx=(0, 10))
        
        self.arch_var = tk.StringVar(value="x64")
        arch_combo = ctk.CTkComboBox(
            options_row,
            variable=self.arch_var,
            values=["x86", "x64"],
            width=100,
            corner_radius=8,
            font=ctk.CTkFont(family="SF Pro Display", size=11),
            state="readonly"
        )
        arch_combo.pack(side="left", padx=(0, 20))
        
        # Delayed injection checkbox
        self.delayed_injection_var = tk.BooleanVar()
        delayed_check = ctk.CTkCheckBox(
            options_row,
            text="Delayed Injection (-i)",
            variable=self.delayed_injection_var,
            font=ctk.CTkFont(family="SF Pro Display", size=11)
        )
        delayed_check.pack(side="left")
        
        # Action buttons row
        actions_row = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        actions_row.pack(fill="x", pady=(0, 15))
        
        self.create_modern_button(actions_row, "🚀 Launch App", self.launch_application, "success", 140).pack(side="left", padx=(0, 15))
        self.create_modern_button(actions_row, "💾 Save Config", self.save_configuration_dialog, "primary", 140).pack(side="left", padx=(0, 15))
        self.create_modern_button(actions_row, "🔄 Refresh All", self.refresh_all_data, "secondary", 120).pack(side="left")
        
        # Recent launches section
        recent_frame = self.create_modern_frame(launcher_tab)
        recent_frame.pack(fill="both", expand=True)
        
        recent_title = ctk.CTkLabel(
            recent_frame,
            text="📋 Quick Launch (Saved Configurations)",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        recent_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.quick_launch_frame = self.create_modern_scrollable_frame(recent_frame)
        self.quick_launch_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_interfaces_tab(self):
        """Create network interfaces tab"""
        self.tabview.add("🌐 Interfaces")
        interfaces_tab = self.tabview.tab("🌐 Interfaces")
        
        # Modern toolbar
        toolbar = self.create_modern_frame(interfaces_tab, transparent=True)
        toolbar.pack(fill="x", pady=(0, 20))
        
        button_frame = self.create_modern_frame(toolbar)
        button_frame.pack(fill="x")
        
        buttons_container = ctk.CTkFrame(button_frame, fg_color=("#ffffff", "#2d2d2d"))
        buttons_container.pack(padx=20, pady=15)
        
        self.create_modern_button(buttons_container, "🔄 Refresh Interfaces", self.refresh_network_interfaces, "primary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "📊 Show Details", self.show_interface_details, "secondary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🧪 Test Connection", self.test_interface_connection, "warning").pack(side="left")
        
        # Modern interfaces list
        self.interfaces_frame = self.create_modern_scrollable_frame(interfaces_tab)
        self.interfaces_frame.pack(fill="both", expand=True)

    def create_configurations_tab(self):
        """Create saved configurations tab"""
        self.tabview.add("💾 Configurations")
        config_tab = self.tabview.tab("💾 Configurations")
        
        # Modern toolbar
        toolbar = self.create_modern_frame(config_tab, transparent=True)
        toolbar.pack(fill="x", pady=(0, 20))
        
        button_frame = self.create_modern_frame(toolbar)
        button_frame.pack(fill="x")
        
        buttons_container = ctk.CTkFrame(button_frame, fg_color=("#ffffff", "#2d2d2d"))
        buttons_container.pack(padx=20, pady=15)
        
        self.create_modern_button(buttons_container, "➕ Add Configuration", self.add_configuration_dialog, "success").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "✏️ Edit Selected", self.edit_configuration, "primary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🗑️ Delete Selected", self.delete_configuration, "danger").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🔄 Refresh", self.refresh_configurations, "secondary").pack(side="left")
        
        # Modern configurations list
        self.configurations_frame = self.create_modern_scrollable_frame(config_tab)
        self.configurations_frame.pack(fill="both", expand=True)

    def create_settings_tab(self):
        """Create settings tab"""
        self.tabview.add("⚙️ Settings")
        settings_tab = self.tabview.tab("⚙️ Settings")
        
        # Settings frame
        settings_frame = self.create_modern_frame(settings_tab)
        settings_frame.pack(fill="x", pady=(0, 20))
        
        settings_title = ctk.CTkLabel(
            settings_frame,
            text="🔧 ForceBindIP Settings",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        settings_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # ForceBindIP path setting
        path_frame = ctk.CTkFrame(settings_frame, fg_color=("#ffffff", "#2d2d2d"))
        path_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="📂 ForceBindIP Path:",
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        path_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        path_entry_frame = ctk.CTkFrame(path_frame, fg_color=("#ffffff", "#2d2d2d"))
        path_entry_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.forcebindip_path_var = tk.StringVar(value=self.forcebindip_path)
        path_entry = ctk.CTkEntry(
            path_entry_frame,
            textvariable=self.forcebindip_path_var,
            placeholder_text="Path to ForceBindIP.exe or ForceBindIP64.exe",
            width=400,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        path_entry.pack(side="left", padx=(0, 10))
        
        browse_path_btn = ctk.CTkButton(
            path_entry_frame,
            text="📁 Browse",
            command=self.browse_forcebindip_path,
            width=100,
            height=35,
            corner_radius=8
        )
        browse_path_btn.pack(side="left", padx=(0, 10))
        
        test_path_btn = ctk.CTkButton(
            path_entry_frame,
            text="🧪 Test",
            command=self.test_forcebindip_path,
            width=80,
            height=35,
            corner_radius=8,
            fg_color=("#28a745", "#22c55e")
        )
        test_path_btn.pack(side="left")
        
        # Auto-detect section
        detect_frame = ctk.CTkFrame(settings_frame, fg_color=("#ffffff", "#2d2d2d"))
        detect_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        detect_label = ctk.CTkLabel(
            detect_frame,
            text="🔍 Auto-Detection:",
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        detect_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        detect_buttons = ctk.CTkFrame(detect_frame, fg_color=("#ffffff", "#2d2d2d"))
        detect_buttons.pack(fill="x", padx=15, pady=(0, 15))
        
        self.create_modern_button(detect_buttons, "🔍 Auto-Detect ForceBindIP", self.auto_detect_forcebindip, "primary", 200).pack(side="left", padx=(0, 15))
        self.create_modern_button(detect_buttons, "📥 Download ForceBindIP", self.download_forcebindip_dialog, "warning", 180).pack(side="left")

    def create_monitoring_tab(self):
        """Create monitoring tab"""
        self.tabview.add("📊 Monitoring")
        monitor_tab = self.tabview.tab("📊 Monitoring")
        
        # Modern stats frame
        stats_frame = self.create_modern_frame(monitor_tab)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📈 System Information",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        stats_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.stats_text = ctk.CTkTextbox(
            stats_frame,
            height=200,
            corner_radius=10,
            border_width=1,
            border_color=("#dee2e6", "#404040"),
            fg_color=("#f8f9fa", "#1a1a1a"),
            font=ctk.CTkFont(family="SF Mono", size=12)
        )
        self.stats_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Refresh button
        refresh_container = ctk.CTkFrame(monitor_tab, fg_color=("#f8f9fa", "#1e1e1e"))
        refresh_container.pack(pady=(0, 20))
        
        self.create_modern_button(refresh_container, "🔄 Refresh System Info", self.refresh_system_info, "primary", 180).pack()
        
        # Modern logs frame
        logs_frame = self.create_modern_frame(monitor_tab)
        logs_frame.pack(fill="both", expand=True)
        
        logs_title = ctk.CTkLabel(
            logs_frame,
            text="📝 Activity Log",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        logs_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.logs_text = ctk.CTkTextbox(
            logs_frame,
            corner_radius=10,
            border_width=1,
            border_color=("#dee2e6", "#404040"),
            fg_color=("#f8f9fa", "#1a1a1a"),
            font=ctk.CTkFont(family="SF Mono", size=11)
        )
        self.logs_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Core functionality methods
    def log_message(self, message: str):
        """Add message to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert("end", log_entry)
        
    def load_configuration(self):
        """Load application configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.forcebindip_path = config.get('forcebindip_path', '')
                    self.saved_configs = config.get('saved_configs', [])
                    self.log_message("✅ Configuration loaded successfully")
            else:
                self.log_message("⚠️ No configuration file found, using defaults")
        except Exception as e:
            self.log_message(f"❌ Error loading configuration: {str(e)}")
    
    def save_configuration_to_file(self):
        """Save application configuration to file"""
        try:
            config = {
                'forcebindip_path': self.forcebindip_path,
                'saved_configs': self.saved_configs
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.log_message("✅ Configuration saved successfully")
        except Exception as e:
            self.log_message(f"❌ Error saving configuration: {str(e)}")
    
    def refresh_all_data(self):
        """Refresh all data"""
        self.log_message("🔄 Refreshing all data...")
        self.refresh_network_interfaces()
        self.refresh_configurations()
        self.refresh_system_info()
        self.log_message("✅ All data refreshed successfully")
    
    def refresh_network_interfaces(self):
        """Refresh network interfaces list"""
        self.log_message("🔄 Refreshing network interfaces...")
        try:
            interfaces = []
            for interface_name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == 2:  # IPv4
                        interfaces.append(f"{addr.address} - {interface_name}")
            
            self.network_interfaces = interfaces
            
            # Update interface combo
            if hasattr(self, 'interface_combo'):
                self.interface_combo.configure(values=interfaces)
                if interfaces:
                    self.interface_combo.set(interfaces[0])
            
            # Update interface display
            self.update_interfaces_display()
            
            self.log_message(f"✅ Found {len(interfaces)} network interfaces")
        except Exception as e:
            self.log_message(f"❌ Error refreshing interfaces: {str(e)}")
    
    def update_interfaces_display(self):
        """Update the interfaces display in the interfaces tab"""
        # Clear existing interface widgets
        for widget in self.interfaces_frame.winfo_children():
            widget.destroy()
        
        for interface in self.network_interfaces:
            ip_address, interface_name = interface.split(" - ", 1)
            self.create_interface_card(ip_address, interface_name)
    
    def create_interface_card(self, ip_address: str, interface_name: str):
        """Create a modern interface card widget"""
        card = ctk.CTkFrame(
            self.interfaces_frame,
            corner_radius=15,
            fg_color=("#ffffff", "#2d2d2d"),
            border_width=1,
            border_color=("#dee2e6", "#404040")
        )
        card.pack(fill="x", padx=10, pady=8)
        
        content_frame = ctk.CTkFrame(card, fg_color=("#ffffff", "#2d2d2d"))
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Interface header
        header_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        header_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"🌐 {interface_name}",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#000000", "#ffffff")
        )
        name_label.pack(side="left")
        
        # IP address
        ip_label = ctk.CTkLabel(
            content_frame,
            text=f"📍 IP Address: {ip_address}",
            font=ctk.CTkFont(size=14),
            text_color=("#495057", "#b0b0b0")
        )
        ip_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        actions_frame.pack(fill="x", pady=(10, 0))
        
        use_btn = ctk.CTkButton(
            actions_frame,
            text="✅ Use This Interface",
            command=lambda: self.select_interface(f"{ip_address} - {interface_name}"),
            width=150,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#28a745", "#22c55e"),
            hover_color=("#1e7e34", "#16a34a")
        )
        use_btn.pack(side="left", padx=(0, 10))
        
        test_btn = ctk.CTkButton(
            actions_frame,
            text="🧪 Test",
            command=lambda: self.test_specific_interface(ip_address),
            width=80,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#ffc107", "#f59e0b"),
            hover_color=("#e0a800", "#d97706")
        )
        test_btn.pack(side="left")

    # Continue with remaining methods...
    
    # ForceBindIP functionality methods
    def browse_application(self):
        """Browse for application to launch"""
        self.log_message("📁 Opening application browser...")
        filetypes = [
            ("Executable files", "*.exe"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Application to Launch",
            filetypes=filetypes,
            initialdir=os.path.expanduser("~")
        )
        
        if filename:
            self.app_path_var.set(filename)
            self.log_message(f"📱 Selected application: {os.path.basename(filename)}")
    
    def select_interface(self, interface: str):
        """Select an interface for binding"""
        self.interface_var.set(interface)
        self.log_message(f"✅ Selected interface: {interface}")
        # Switch back to launcher tab
        self.tabview.set("🚀 Launcher")
    
    def test_specific_interface(self, ip_address: str):
        """Test connectivity on specific interface"""
        self.log_message(f"🧪 Testing interface {ip_address}...")
        
        def test_thread():
            try:
                # Simple ping test
                result = subprocess.run(
                    ["ping", "-n", "1", "-S", ip_address, "8.8.8.8"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.log_message(f"✅ Interface {ip_address} test successful")
                else:
                    self.log_message(f"❌ Interface {ip_address} test failed")
            except Exception as e:
                self.log_message(f"❌ Interface test error: {str(e)}")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def launch_application(self):
        """Launch application with ForceBindIP"""
        app_path = self.app_path_var.get().strip()
        interface = self.interface_var.get().strip()
        args = self.args_var.get().strip()
        arch = self.arch_var.get()
        delayed = self.delayed_injection_var.get()
        
        if not app_path:
            self.show_error("Please select an application to launch")
            return
            
        if not interface:
            self.show_error("Please select a network interface")
            return
            
        if not self.forcebindip_path:
            self.show_error("Please configure ForceBindIP path in Settings")
            return
        
        # Extract IP from interface string
        ip_address = interface.split(" - ")[0]
        
        # Build ForceBindIP command
        forcebindip_exe = self.forcebindip_path
        if arch == "x64" and "64" not in forcebindip_exe:
            # Try to find x64 version
            dir_path = os.path.dirname(forcebindip_exe)
            x64_path = os.path.join(dir_path, "ForceBindIP64.exe")
            if os.path.exists(x64_path):
                forcebindip_exe = x64_path
        
        cmd = [forcebindip_exe]
        
        if delayed:
            cmd.append("-i")
        
        cmd.extend([ip_address, app_path])
        
        if args:
            cmd.extend(args.split())
        
        self.log_message(f"🚀 Launching: {os.path.basename(app_path)} bound to {ip_address}")
        
        def launch_thread():
            try:
                # Launch the application
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                self.log_message(f"✅ Application launched successfully (PID: {process.pid})")
                
                # Wait a moment to check if it fails immediately
                try:
                    stdout, stderr = process.communicate(timeout=2)
                    if process.returncode != 0 and stderr:
                        self.log_message(f"❌ Launch error: {stderr}")
                except subprocess.TimeoutExpired:
                    # Process is still running, which is good
                    self.log_message(f"✅ Application is running with network binding")
                    
            except Exception as e:
                self.log_message(f"❌ Launch failed: {str(e)}")
        
        threading.Thread(target=launch_thread, daemon=True).start()
    
    def save_configuration_dialog(self):
        """Save current configuration dialog"""
        app_path = self.app_path_var.get().strip()
        interface = self.interface_var.get().strip()
        args = self.args_var.get().strip()
        arch = self.arch_var.get()
        delayed = self.delayed_injection_var.get()
        
        if not app_path or not interface:
            self.show_error("Please select an application and interface first")
            return
        
        # Create save dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("💾 Save Configuration")
        dialog.geometry("400x300")
        dialog.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="💾 Save Application Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Configuration name
        name_label = ctk.CTkLabel(
            main_frame,
            text="Configuration Name:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        name_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        name_var = tk.StringVar(value=os.path.basename(app_path).replace('.exe', ''))
        name_entry = ctk.CTkEntry(
            main_frame,
            textvariable=name_var,
            width=300,
            height=35,
            corner_radius=8
        )
        name_entry.pack(padx=20, pady=(0, 20))
        
        # Configuration preview
        preview_label = ctk.CTkLabel(
            main_frame,
            text="Configuration Preview:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        preview_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        preview_text = f"""Application: {os.path.basename(app_path)}
Interface: {interface}
Arguments: {args or 'None'}
Architecture: {arch}
Delayed Injection: {'Yes' if delayed else 'No'}"""
        
        preview_box = ctk.CTkTextbox(
            main_frame,
            height=100,
            corner_radius=8
        )
        preview_box.pack(fill="x", padx=20, pady=(0, 20))
        preview_box.insert("1.0", preview_text)
        preview_box.configure(state="disabled")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        def save_config():
            name = name_var.get().strip()
            if not name:
                return
                
            config = {
                'name': name,
                'app_path': app_path,
                'interface': interface,
                'args': args,
                'architecture': arch,
                'delayed_injection': delayed,
                'created': datetime.now().isoformat()
            }
            
            self.saved_configs.append(config)
            self.save_configuration_to_file()
            self.refresh_configurations()
            self.refresh_quick_launch()
            self.log_message(f"✅ Saved configuration: {name}")
            dialog.destroy()
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color=("#6c757d", "#64748b")
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=save_config,
            width=100,
            height=35,
            fg_color=("#28a745", "#22c55e")
        )
        save_btn.pack(side="left")
    
    def refresh_configurations(self):
        """Refresh the configurations display"""
        self.log_message("🔄 Refreshing configurations...")
        
        # Clear existing configuration widgets
        for widget in self.configurations_frame.winfo_children():
            widget.destroy()
        
        if not self.saved_configs:
            no_configs_label = ctk.CTkLabel(
                self.configurations_frame,
                text="No saved configurations. Create one from the Launcher tab!",
                font=ctk.CTkFont(size=16),
                text_color=("#666666", "#999999")
            )
            no_configs_label.pack(pady=50)
            return
        
        for i, config in enumerate(self.saved_configs):
            self.create_configuration_card(config, i)
    
    def create_configuration_card(self, config: dict, index: int):
        """Create a configuration card widget"""
        card = ctk.CTkFrame(
            self.configurations_frame,
            corner_radius=15,
            fg_color=("#ffffff", "#2d2d2d"),
            border_width=1,
            border_color=("#dee2e6", "#404040")
        )
        card.pack(fill="x", padx=10, pady=8)
        
        content_frame = ctk.CTkFrame(card, fg_color=("#ffffff", "#2d2d2d"))
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Configuration header
        header_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        header_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"🎮 {config['name']}",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#000000", "#ffffff")
        )
        name_label.pack(side="left")
        
        created_label = ctk.CTkLabel(
            header_frame,
            text=f"Created: {config.get('created', 'Unknown')[:10]}",
            font=ctk.CTkFont(size=11),
            text_color=("#6c757d", "#888888")
        )
        created_label.pack(side="right")
        
        # Configuration details
        app_label = ctk.CTkLabel(
            content_frame,
            text=f"📱 App: {os.path.basename(config['app_path'])}",
            font=ctk.CTkFont(size=12),
            text_color=("#495057", "#b0b0b0")
        )
        app_label.pack(anchor="w")
        
        interface_label = ctk.CTkLabel(
            content_frame,
            text=f"🌐 Interface: {config['interface']}",
            font=ctk.CTkFont(size=12),
            text_color=("#495057", "#b0b0b0")
        )
        interface_label.pack(anchor="w")
        
        if config.get('args'):
            args_label = ctk.CTkLabel(
                content_frame,
                text=f"⚙️ Args: {config['args']}",
                font=ctk.CTkFont(size=12),
                text_color=("#495057", "#b0b0b0")
            )
            args_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        actions_frame.pack(fill="x", pady=(10, 0))
        
        launch_btn = ctk.CTkButton(
            actions_frame,
            text="🚀 Launch",
            command=lambda: self.launch_from_config(config),
            width=100,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#28a745", "#22c55e"),
            hover_color=("#1e7e34", "#16a34a")
        )
        launch_btn.pack(side="left", padx=(0, 10))
        
        load_btn = ctk.CTkButton(
            actions_frame,
            text="📥 Load",
            command=lambda: self.load_configuration(config),
            width=80,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#007bff", "#0066cc"),
            hover_color=("#0056b3", "#004999")
        )
        load_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            command=lambda: self.delete_configuration_at_index(index),
            width=40,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#dc3545", "#ef4444"),
            hover_color=("#c82333", "#dc2626")
        )
        delete_btn.pack(side="left")
    
    def launch_from_config(self, config: dict):
        """Launch application from saved configuration"""
        self.log_message(f"🚀 Launching from config: {config['name']}")
        
        # Load configuration into launcher
        self.app_path_var.set(config['app_path'])
        self.interface_var.set(config['interface'])
        self.args_var.set(config.get('args', ''))
        self.arch_var.set(config.get('architecture', 'x64'))
        self.delayed_injection_var.set(config.get('delayed_injection', False))
        
        # Launch the application
        self.launch_application()
    
    def load_configuration(self, config: dict):
        """Load configuration into launcher tab"""
        self.app_path_var.set(config['app_path'])
        self.interface_var.set(config['interface'])
        self.args_var.set(config.get('args', ''))
        self.arch_var.set(config.get('architecture', 'x64'))
        self.delayed_injection_var.set(config.get('delayed_injection', False))
        
        self.log_message(f"📥 Loaded configuration: {config['name']}")
        
        # Switch to launcher tab
        self.tabview.set("🚀 Launcher")
    
    def delete_configuration_at_index(self, index: int):
        """Delete configuration at specific index"""
        if 0 <= index < len(self.saved_configs):
            config_name = self.saved_configs[index]['name']
            
            # Create confirmation dialog
            dialog = ctk.CTkToplevel(self.root)
            dialog.title("Confirm Delete")
            dialog.geometry("300x150")
            dialog.grab_set()
            
            warning_label = ctk.CTkLabel(
                dialog,
                text=f"Delete '{config_name}'?",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            warning_label.pack(pady=20)
            
            button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            button_frame.pack(pady=10)
            
            def confirm_delete():
                del self.saved_configs[index]
                self.save_configuration_to_file()
                self.refresh_configurations()
                self.refresh_quick_launch()
                self.log_message(f"🗑️ Deleted configuration: {config_name}")
                dialog.destroy()
            
            cancel_btn = ctk.CTkButton(
                button_frame,
                text="Cancel",
                command=dialog.destroy,
                width=80,
                fg_color=("#6c757d", "#64748b")
            )
            cancel_btn.pack(side="left", padx=(0, 10))
            
            delete_btn = ctk.CTkButton(
                button_frame,
                text="Delete",
                command=confirm_delete,
                width=80,
                fg_color=("#dc3545", "#ef4444")
            )
            delete_btn.pack(side="left")
    
    def refresh_quick_launch(self):
        """Refresh quick launch buttons"""
        # Clear existing quick launch widgets
        for widget in self.quick_launch_frame.winfo_children():
            widget.destroy()
        
        if not self.saved_configs:
            no_configs_label = ctk.CTkLabel(
                self.quick_launch_frame,
                text="Save configurations to see quick launch buttons here!",
                font=ctk.CTkFont(size=14),
                text_color=("#666666", "#999999")
            )
            no_configs_label.pack(pady=30)
            return
        
        # Create quick launch buttons
        for config in self.saved_configs[:8]:  # Limit to 8 for clean layout
            btn_frame = ctk.CTkFrame(
                self.quick_launch_frame,
                corner_radius=10,
                fg_color=("#f8f9fa", "#2d2d2d"),
                border_width=1,
                border_color=("#dee2e6", "#404040")
            )
            btn_frame.pack(fill="x", padx=5, pady=5)
            
            content_frame = ctk.CTkFrame(btn_frame, fg_color=("#f8f9fa", "#2d2d2d"))
            content_frame.pack(fill="x", padx=10, pady=10)
            
            name_label = ctk.CTkLabel(
                content_frame,
                text=f"🎮 {config['name']}",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            name_label.pack(fill="x")
            
            details_label = ctk.CTkLabel(
                content_frame,
                text=f"{os.path.basename(config['app_path'])} → {config['interface'].split(' - ')[0]}",
                font=ctk.CTkFont(size=11),
                text_color=("#6c757d", "#888888"),
                anchor="w"
            )
            details_label.pack(fill="x", pady=(2, 8))
            
            launch_btn = ctk.CTkButton(
                content_frame,
                text="🚀 Quick Launch",
                command=lambda c=config: self.launch_from_config(c),
                height=30,
                corner_radius=8,
                font=ctk.CTkFont(size=12),
                fg_color=("#28a745", "#22c55e"),
                hover_color=("#1e7e34", "#16a34a")
            )
            launch_btn.pack(fill="x")
    
    # Settings tab methods
    def browse_forcebindip_path(self):
        """Browse for ForceBindIP executable"""
        self.log_message("📁 Browsing for ForceBindIP executable...")
        
        filetypes = [
            ("ForceBindIP executables", "ForceBindIP*.exe"),
            ("Executable files", "*.exe"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select ForceBindIP Executable",
            filetypes=filetypes,
            initialdir=os.path.expanduser("~")
        )
        
        if filename:
            self.forcebindip_path = filename
            self.forcebindip_path_var.set(filename)
            self.save_configuration_to_file()
            self.log_message(f"📂 ForceBindIP path set: {filename}")
    
    def test_forcebindip_path(self):
        """Test if ForceBindIP path is valid"""
        path = self.forcebindip_path_var.get().strip()
        
        if not path:
            self.show_error("Please enter or browse for ForceBindIP path")
            return
        
        if not os.path.exists(path):
            self.show_error("ForceBindIP executable not found at specified path")
            return
        
        try:
            # Test by running with help flag
            result = subprocess.run([path], capture_output=True, text=True, timeout=5)
            
            # ForceBindIP typically returns usage info when run without args
            if "ForceBindIP" in result.stderr or "usage" in result.stderr.lower():
                self.forcebindip_path = path
                self.save_configuration_to_file()
                self.show_success("ForceBindIP executable is valid!")
                self.log_message("✅ ForceBindIP test successful")
            else:
                self.show_error("File does not appear to be ForceBindIP")
                
        except Exception as e:
            self.show_error(f"Error testing ForceBindIP: {str(e)}")
    
    def auto_detect_forcebindip(self):
        """Auto-detect ForceBindIP installation"""
        self.log_message("🔍 Auto-detecting ForceBindIP...")
        
        # Common locations to check
        search_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "ForceBindIP"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "ForceBindIP"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.getcwd()
        ]
        
        found_paths = []
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if file.lower().startswith("forcebindip") and file.lower().endswith(".exe"):
                            full_path = os.path.join(root, file)
                            found_paths.append(full_path)
        
        if found_paths:
            # Prefer 64-bit version
            best_path = None
            for path in found_paths:
                if "64" in path:
                    best_path = path
                    break
            
            if not best_path:
                best_path = found_paths[0]
            
            self.forcebindip_path = best_path
            self.forcebindip_path_var.set(best_path)
            self.save_configuration_to_file()
            self.log_message(f"✅ Auto-detected ForceBindIP: {best_path}")
            self.show_success(f"Found ForceBindIP at: {os.path.basename(best_path)}")
        else:
            self.log_message("❌ ForceBindIP not found in common locations")
            self.show_error("ForceBindIP not found. Please download and install it first.")
    
    def download_forcebindip_dialog(self):
        """Show download ForceBindIP dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("📥 Download ForceBindIP")
        dialog.geometry("500x300")
        dialog.grab_set()
        
        main_frame = ctk.CTkFrame(dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📥 Download ForceBindIP",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        info_text = """ForceBindIP is required to use this application.
        
You can download it from the official source:
https://r1ch.net/projects/forcebindip

After downloading:
1. Extract the files to a folder
2. Use the Settings tab to set the path to ForceBindIP.exe or ForceBindIP64.exe
3. Test the path to ensure it works

The application supports both x86 and x64 versions."""
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=20, pady=20)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        def open_download_page():
            import webbrowser
            webbrowser.open("https://r1ch.net/projects/forcebindip")
            self.log_message("🌐 Opened ForceBindIP download page")
        
        download_btn = ctk.CTkButton(
            button_frame,
            text="🌐 Open Download Page",
            command=open_download_page,
            width=180,
            height=35,
            fg_color=("#007bff", "#0066cc")
        )
        download_btn.pack(side="left", padx=(0, 10))
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=dialog.destroy,
            width=80,
            height=35,
            fg_color=("#6c757d", "#64748b")
        )
        close_btn.pack(side="left")
    
    # Interface management methods
    def show_interface_details(self):
        """Show detailed interface information"""
        self.log_message("📊 Showing interface details...")
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("🌐 Network Interface Details")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        main_frame = ctk.CTkFrame(dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌐 Network Interface Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        details_text = ctk.CTkTextbox(
            main_frame,
            corner_radius=10,
            font=ctk.CTkFont(family="SF Mono", size=11)
        )
        details_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Gather detailed interface information
        try:
            info_lines = []
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            for interface_name, addrs in interfaces.items():
                info_lines.append(f"🌐 Interface: {interface_name}")
                info_lines.append("-" * 50)
                
                # Get stats if available
                if interface_name in stats:
                    stat = stats[interface_name]
                    info_lines.append(f"  📊 Status: {'Up' if stat.isup else 'Down'}")
                    info_lines.append(f"  🔗 MTU: {stat.mtu}")
                    info_lines.append(f"  🏃 Speed: {stat.speed} Mbps" if stat.speed > 0 else "  🏃 Speed: Unknown")
                
                # Get addresses
                for addr in addrs:
                    if addr.family == 2:  # IPv4
                        info_lines.append(f"  📍 IPv4: {addr.address}")
                        if addr.netmask:
                            info_lines.append(f"  🎭 Netmask: {addr.netmask}")
                    elif addr.family == 17 and addr.address:  # MAC
                        info_lines.append(f"  🏷️ MAC: {addr.address}")
                
                info_lines.append("")
            
            details_text.insert("1.0", "\n".join(info_lines))
            
        except Exception as e:
            details_text.insert("1.0", f"❌ Error gathering interface details: {str(e)}")
        
        details_text.configure(state="disabled")
        
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=dialog.destroy,
            width=100,
            height=35
        )
        close_btn.pack(pady=10)
    
    def test_interface_connection(self):
        """Test connection on all interfaces"""
        self.log_message("🧪 Testing all interface connections...")
        
        def test_all_thread():
            for interface in self.network_interfaces:
                ip_address = interface.split(" - ")[0]
                self.test_specific_interface(ip_address)
        
        threading.Thread(target=test_all_thread, daemon=True).start()
    
    def refresh_system_info(self):
        """Refresh system information display"""
        self.log_message("📈 Refreshing system information...")
        
        try:
            # Gather system information
            info_lines = []
            
            # System info
            info_lines.append("🖥️ SYSTEM INFORMATION")
            info_lines.append("=" * 50)
            info_lines.append(f"Platform: {os.name} {os.sys.platform}")
            
            # CPU info
            info_lines.append(f"CPU Usage: {psutil.cpu_percent(interval=1):.1f}%")
            info_lines.append(f"CPU Count: {psutil.cpu_count()} cores")
            
            # Memory info
            memory = psutil.virtual_memory()
            info_lines.append(f"Memory Usage: {memory.percent:.1f}% ({memory.used // (1024**3)} GB / {memory.total // (1024**3)} GB)")
            
            # Network interfaces count
            info_lines.append(f"Network Interfaces: {len(self.network_interfaces)} detected")
            
            info_lines.append("")
            info_lines.append("🌐 NETWORK INTERFACES")
            info_lines.append("=" * 50)
            
            for interface in self.network_interfaces:
                ip_address, interface_name = interface.split(" - ", 1)
                info_lines.append(f"• {interface_name}: {ip_address}")
            
            info_lines.append("")
            info_lines.append("🔧 FORCEBINDIP CONFIGURATION")
            info_lines.append("=" * 50)
            info_lines.append(f"ForceBindIP Path: {self.forcebindip_path or 'Not configured'}")
            info_lines.append(f"Saved Configurations: {len(self.saved_configs)}")
            
            info_lines.append("")
            info_lines.append(f"🔄 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Update display
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", "\n".join(info_lines))
            
            self.log_message("✅ System information refreshed")
            
        except Exception as e:
            self.log_message(f"❌ Error refreshing system info: {str(e)}")
    
    # Configuration management methods
    def add_configuration_dialog(self):
        """Add new configuration dialog"""
        self.log_message("➕ Opening add configuration dialog...")
        self.save_configuration_dialog()
    
    def edit_configuration(self):
        """Edit selected configuration"""
        self.log_message("✏️ Edit configuration - please use the edit buttons on configuration cards")
    
    def delete_configuration(self):
        """Delete selected configuration"""
        self.log_message("🗑️ Delete configuration - please use the delete buttons on configuration cards")
    
    # Utility methods
    def show_error(self, message):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Error")
        dialog.geometry("300x150")
        dialog.grab_set()
        
        error_label = ctk.CTkLabel(
            dialog,
            text=f"❌ {message}",
            font=ctk.CTkFont(size=14),
            text_color=("#dc3545", "#ff6b6b"),
            wraplength=250
        )
        error_label.pack(pady=30)
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            corner_radius=10
        )
        ok_btn.pack(pady=10)
    
    def show_success(self, message):
        """Show success dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Success")
        dialog.geometry("300x150")
        dialog.grab_set()
        
        success_label = ctk.CTkLabel(
            dialog,
            text=f"✅ {message}",
            font=ctk.CTkFont(size=14),
            text_color=("#28a745", "#40ff40"),
            wraplength=250
        )
        success_label.pack(pady=30)
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            corner_radius=10
        )
        ok_btn.pack(pady=10)

if __name__ == "__main__":
    app = ModernForceBindIPGUI()
    
    # Initialize with data refresh
    app.refresh_all_data()
    app.refresh_quick_launch()
    
    # Run the application
    app.root.mainloop() 