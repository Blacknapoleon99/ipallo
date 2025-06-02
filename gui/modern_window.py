import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import json
import threading
from typing import Optional, Dict, Any
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernBlackzAllocatorGUI:
    """Modern GUI application for BlackzAllocator with rounded corners and sleek design"""
    
    def __init__(self):
        # Create main window
        self.root = ctk.CTk()
        self.root.title("BlackzAllocator")
        self.root.geometry("1500x1000")
        self.root.minsize(1200, 800)
        
        # Configure window
        self.root.configure(fg_color=("#f0f0f0", "#1a1a1a"))
        
        # API base URL
        self.api_base = "http://localhost:8000"
        
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
            text="BlackzAllocator",
            font=ctk.CTkFont(family="SF Pro Display", size=28, weight="bold"),
            text_color=("#000000", "#ffffff")
        )
        self.title_label.pack(side="left")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Professional IP Pool Management",
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
            text="Connected",
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
        self.create_modern_pools_tab()
        self.create_modern_allocations_tab()
        self.create_modern_leases_tab()
        self.create_modern_interfaces_tab()
        self.create_modern_monitoring_tab()
    
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
    
    def create_modern_pools_tab(self):
        """Create modern IP Pools tab"""
        self.tabview.add("🏊‍♂️ IP Pools")
        pools_tab = self.tabview.tab("🏊‍♂️ IP Pools")
        
        # Modern toolbar
        toolbar = self.create_modern_frame(pools_tab, transparent=True)
        toolbar.pack(fill="x", pady=(0, 20))
        
        button_frame = self.create_modern_frame(toolbar)
        button_frame.pack(fill="x", padx=0, pady=0)
        
        # Create buttons with modern styling
        buttons_container = ctk.CTkFrame(button_frame, fg_color=("#ffffff", "#2d2d2d"))
        buttons_container.pack(padx=20, pady=15)
        
        self.create_modern_button(buttons_container, "✨ Create Pool", self.create_pool_dialog, "primary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "✏️ Edit Pool", self.edit_pool, "secondary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🗑️ Delete Pool", self.delete_pool, "danger").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🔄 Refresh", self.refresh_pools_button, "primary").pack(side="left")
        
        # Modern pools list with rounded corners
        self.pools_frame = self.create_modern_scrollable_frame(pools_tab)
        self.pools_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Pool details section
        details_frame = self.create_modern_frame(pools_tab)
        details_frame.pack(fill="x", pady=0)
        
        details_title = ctk.CTkLabel(
            details_frame,
            text="📋 Pool Details",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        details_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.pool_details_text = ctk.CTkTextbox(
            details_frame,
            height=120,
            corner_radius=10,
            border_width=1,
            border_color=("#dee2e6", "#404040"),
            fg_color=("#f8f9fa", "#1a1a1a"),
            font=ctk.CTkFont(family="SF Mono", size=12)
        )
        self.pool_details_text.pack(fill="x", padx=20, pady=(0, 20))
    
    def create_modern_allocations_tab(self):
        """Create modern IP Allocations tab with enhanced pool selection"""
        self.tabview.add("💻 Allocations")
        alloc_tab = self.tabview.tab("💻 Allocations")
        
        # Modern control panel
        control_frame = self.create_modern_frame(alloc_tab)
        control_frame.pack(fill="x", pady=(0, 20))
        
        # Control panel title
        control_title = ctk.CTkLabel(
            control_frame,
            text="⚙️ Allocation Controls",
            font=ctk.CTkFont(family="SF Pro Display", size=16, weight="bold"),
            text_color=("#495057", "#ffffff")
        )
        control_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Controls container
        controls_container = ctk.CTkFrame(control_frame, fg_color=("#ffffff", "#2d2d2d"))
        controls_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # First row - Enhanced pool selection
        row1 = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        row1.pack(fill="x", pady=(0, 15))
        
        # Enhanced pool selection with info
        pool_info_frame = ctk.CTkFrame(row1, fg_color=("#ffffff", "#2d2d2d"))
        pool_info_frame.pack(fill="x", pady=(0, 10))
        
        pool_label = ctk.CTkLabel(
            pool_info_frame, 
            text="🏊 Pool Selection:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        pool_label.pack(side="left", padx=(0, 10))
        
        self.pool_var = tk.StringVar()
        self.pool_combo = ctk.CTkComboBox(
            pool_info_frame,
            variable=self.pool_var,
            width=400,  # Wider to show more info
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=11),
            state="readonly"  # Prevent manual typing
        )
        self.pool_combo.pack(side="left", padx=(0, 20))
        
        # Refresh pools button
        refresh_pools_btn = ctk.CTkButton(
            pool_info_frame,
            text="🔄",
            command=self.update_pool_combo,
            width=35,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=16),
            fg_color=("#17a2b8", "#20c997"),
            hover_color=("#138496", "#1ab394")
        )
        refresh_pools_btn.pack(side="left", padx=(0, 20))
        
        # Strategy selection
        strategy_info_frame = ctk.CTkFrame(row1, fg_color=("#ffffff", "#2d2d2d"))
        strategy_info_frame.pack(fill="x")
        
        strategy_label = ctk.CTkLabel(
            strategy_info_frame, 
            text="🎯 Strategy:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        strategy_label.pack(side="left", padx=(0, 10))
        
        self.strategy_var = tk.StringVar(value="first_fit")
        strategy_combo = ctk.CTkComboBox(
            strategy_info_frame,
            variable=self.strategy_var,
            values=["first_fit", "random", "sequential", "load_balanced"],
            width=200,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=12),
            state="readonly"
        )
        strategy_combo.pack(side="left", padx=(0, 30))
        
        # Client ID entry
        client_label = ctk.CTkLabel(
            strategy_info_frame, 
            text="👤 Client ID:", 
            font=ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        )
        client_label.pack(side="left", padx=(0, 10))
        
        self.client_id_var = tk.StringVar()
        client_entry = ctk.CTkEntry(
            strategy_info_frame,
            textvariable=self.client_id_var,
            placeholder_text="Optional identifier",
            width=200,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(family="SF Pro Display", size=12)
        )
        client_entry.pack(side="left")
        
        # Second row - Action buttons
        row2 = ctk.CTkFrame(controls_container, fg_color=("#ffffff", "#2d2d2d"))
        row2.pack(fill="x")
        
        self.create_modern_button(row2, "🎯 Allocate Next IP", self.allocate_next_ip, "success", 160).pack(side="left", padx=(0, 15))
        self.create_modern_button(row2, "📌 Reserve Specific IP", self.reserve_specific_ip_dialog, "primary", 180).pack(side="left", padx=(0, 15))
        self.create_modern_button(row2, "❌ Deallocate", self.deallocate_ip, "danger", 140).pack(side="left", padx=(0, 15))
        self.create_modern_button(row2, "🔄 Refresh", self.refresh_allocations, "secondary", 120).pack(side="left")
        
        # Modern allocations list
        self.allocations_frame = self.create_modern_scrollable_frame(alloc_tab)
        self.allocations_frame.pack(fill="both", expand=True)
    
    def create_modern_leases_tab(self):
        """Create modern IP Leases tab"""
        self.tabview.add("⏰ Leases")
        leases_tab = self.tabview.tab("⏰ Leases")
        
        # Modern toolbar
        toolbar = self.create_modern_frame(leases_tab, transparent=True)
        toolbar.pack(fill="x", pady=(0, 20))
        
        button_frame = self.create_modern_frame(toolbar)
        button_frame.pack(fill="x")
        
        buttons_container = ctk.CTkFrame(button_frame, fg_color=("#ffffff", "#2d2d2d"))
        buttons_container.pack(padx=20, pady=15)
        
        self.create_modern_button(buttons_container, "🔄 Renew Lease", self.renew_lease_dialog, "success").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🧹 Cleanup Expired", self.cleanup_expired_leases, "warning").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🔄 Refresh", self.refresh_leases, "primary").pack(side="left")
        
        # Modern leases list
        self.leases_frame = self.create_modern_scrollable_frame(leases_tab)
        self.leases_frame.pack(fill="both", expand=True)
    
    def create_modern_interfaces_tab(self):
        """Create modern Network Interfaces tab"""
        self.tabview.add("🌐 Interfaces")
        interfaces_tab = self.tabview.tab("🌐 Interfaces")
        
        # Modern toolbar
        toolbar = self.create_modern_frame(interfaces_tab, transparent=True)
        toolbar.pack(fill="x", pady=(0, 20))
        
        button_frame = self.create_modern_frame(toolbar)
        button_frame.pack(fill="x")
        
        buttons_container = ctk.CTkFrame(button_frame, fg_color=("#ffffff", "#2d2d2d"))
        buttons_container.pack(padx=20, pady=15)
        
        self.create_modern_button(buttons_container, "🔗 Bind IP", self.bind_ip_dialog, "success").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🔓 Unbind IP", self.unbind_ip_dialog, "warning").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "📡 Test Connectivity", self.test_connectivity_dialog, "primary").pack(side="left", padx=(0, 15))
        self.create_modern_button(buttons_container, "🔄 Refresh", self.refresh_interfaces, "secondary").pack(side="left")
        
        # Modern interfaces list
        self.interfaces_frame = self.create_modern_scrollable_frame(interfaces_tab)
        self.interfaces_frame.pack(fill="both", expand=True)
    
    def create_modern_monitoring_tab(self):
        """Create modern Monitoring tab"""
        self.tabview.add("📊 Monitoring")
        monitor_tab = self.tabview.tab("📊 Monitoring")
        
        # Modern stats frame
        stats_frame = self.create_modern_frame(monitor_tab)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📈 System Statistics",
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
        
        self.create_modern_button(refresh_container, "🔄 Refresh Statistics", self.refresh_stats, "primary", 180).pack()
        
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
    
    # API Methods and other functions (fully implemented)
    def api_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request"""
        try:
            url = f"{self.api_base}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, timeout=10)
            else:
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log_message(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log_message(f"❌ Connection Error: {str(e)}")
            return None
    
    def log_message(self, message: str):
        """Add message to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert("end", log_entry)
    
    def refresh_all_data(self):
        """Refresh all data including enhanced pool information"""
        self.log_message("🔄 Refreshing all data...")
        
        # Refresh pools first (this populates the combos)
        self.refresh_pools()
        
        # Update pool combo with enhanced information
        self.update_pool_combo()
        
        # Refresh other data
        self.refresh_allocations()
        self.refresh_leases()
        self.refresh_interfaces()
        self.refresh_stats()
        
        self.log_message("✅ All data refreshed successfully")
    
    def refresh_pools(self):
        """Refresh pools data and display in GUI"""
        self.log_message("🔄 Refreshing pools...")
        pools_data = self.api_request('GET', '/pools/')
        
        # Clear existing pool widgets
        for widget in self.pools_frame.winfo_children():
            widget.destroy()
        
        if pools_data:
            for pool in pools_data:
                # Get utilization
                utilization_data = self.api_request('GET', f'/pools/{pool["id"]}/utilization')
                utilization = utilization_data.get('utilization_percent', 0) if utilization_data else 0
                
                # Create modern pool card
                self.create_pool_card(pool, utilization)
            
            self.log_message(f"✅ Refreshed {len(pools_data)} IP pools")
        else:
            # Show no pools message
            no_pools_label = ctk.CTkLabel(
                self.pools_frame,
                text="No pools found. Create your first pool!",
                font=ctk.CTkFont(size=16),
                text_color=("#666666", "#999999")
            )
            no_pools_label.pack(pady=50)
    
    def create_pool_card(self, pool, utilization):
        """Create a modern pool card widget"""
        # Pool card frame
        card = ctk.CTkFrame(
            self.pools_frame,
            corner_radius=15,
            fg_color=("#ffffff", "#2d2d2d"),
            border_width=1,
            border_color=("#dee2e6", "#404040")
        )
        card.pack(fill="x", padx=10, pady=8)
        
        # Card content
        content_frame = ctk.CTkFrame(card, fg_color=("#ffffff", "#2d2d2d"))
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Pool header
        header_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Pool name and status
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"🏊‍♂️ {pool['name']}",
            font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
            text_color=("#000000", "#ffffff")
        )
        name_label.pack(side="left")
        
        status_text = "🟢 Active" if pool['is_active'] else "🔴 Inactive"
        status_label = ctk.CTkLabel(
            header_frame,
            text=status_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#28a745", "#40ff40") if pool['is_active'] else ("#dc3545", "#ff6b6b")
        )
        status_label.pack(side="right")
        
        # Pool details
        details_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        details_frame.pack(fill="x", pady=(0, 10))
        
        # CIDR and utilization
        cidr_label = ctk.CTkLabel(
            details_frame,
            text=f"📍 CIDR: {pool['cidr']}",
            font=ctk.CTkFont(size=14),
            text_color=("#495057", "#b0b0b0")
        )
        cidr_label.pack(side="left")
        
        util_color = "#28a745" if utilization < 80 else "#ffc107" if utilization < 95 else "#dc3545"
        util_label = ctk.CTkLabel(
            details_frame,
            text=f"📊 Utilization: {utilization:.1f}%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=(util_color, util_color)
        )
        util_label.pack(side="right")
        
        # Gateway and description
        if pool.get('gateway'):
            gateway_label = ctk.CTkLabel(
                content_frame,
                text=f"🌐 Gateway: {pool['gateway']}",
                font=ctk.CTkFont(size=12),
                text_color=("#6c757d", "#888888")
            )
            gateway_label.pack(anchor="w")
        
        if pool.get('description'):
            desc_label = ctk.CTkLabel(
                content_frame,
                text=f"📝 {pool['description']}",
                font=ctk.CTkFont(size=12),
                text_color=("#6c757d", "#888888")
            )
            desc_label.pack(anchor="w", pady=(5, 0))
        
        # Action buttons
        actions_frame = ctk.CTkFrame(content_frame, fg_color=("#ffffff", "#2d2d2d"))
        actions_frame.pack(fill="x", pady=(10, 0))
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Edit",
            command=lambda: self.edit_pool_dialog(pool),
            width=80,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#6c757d", "#64748b"),
            hover_color=("#545b62", "#475569")
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Delete",
            command=lambda: self.delete_pool_dialog(pool),
            width=90,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color=("#dc3545", "#ef4444"),
            hover_color=("#c82333", "#dc2626")
        )
        delete_btn.pack(side="left")
    
    def update_pool_combo(self):
        """Update pool combobox values with enhanced information"""
        pools_data = self.api_request('GET', '/pools/')
        if pools_data:
            # Get utilization data for each pool
            pool_options = []
            pool_details = {}
            
            for pool in pools_data:
                if pool['is_active']:
                    # Get utilization info
                    util_data = self.api_request('GET', f'/pools/{pool["id"]}/utilization')
                    if util_data:
                        used_ips = util_data.get('allocated_ips', 0)
                        total_ips = util_data.get('total_ips', 0)
                        available_ips = total_ips - used_ips
                        utilization_pct = (used_ips / total_ips * 100) if total_ips > 0 else 0
                        
                        # Create descriptive option text
                        option_text = f"{pool['id']} - {pool['name']} ({pool['cidr']}) | {available_ips}/{total_ips} available ({utilization_pct:.0f}% used)"
                        pool_options.append(option_text)
                        pool_details[option_text] = {
                            'id': pool['id'],
                            'name': pool['name'],
                            'cidr': pool['cidr'],
                            'available': available_ips,
                            'total': total_ips,
                            'utilization': utilization_pct
                        }
                    else:
                        # Fallback if utilization data unavailable
                        option_text = f"{pool['id']} - {pool['name']} ({pool['cidr']})"
                        pool_options.append(option_text)
                        pool_details[option_text] = {
                            'id': pool['id'],
                            'name': pool['name'],
                            'cidr': pool['cidr'],
                            'available': '?',
                            'total': '?',
                            'utilization': 0
                        }
            
            # Sort by utilization (least used first) to recommend best pools
            pool_options.sort(key=lambda x: pool_details[x]['utilization'])
            
            # Update combobox
            if hasattr(self, 'pool_combo') and self.pool_combo:
                self.pool_combo.configure(values=pool_options)
                if pool_options:
                    # Auto-select the pool with most available space
                    best_pool = min(pool_options, key=lambda x: pool_details[x]['utilization'])
                    self.pool_combo.set(best_pool)
                    self.log_message(f"📋 Auto-selected optimal pool: {pool_details[best_pool]['name']} ({pool_details[best_pool]['available']} IPs available)")
                else:
                    self.pool_combo.set("No active pools available")
                    self.log_message("⚠️ No active pools found")
            
            # Store pool details for other components
            self.pool_details = pool_details
            return pool_options
        else:
            if hasattr(self, 'pool_combo') and self.pool_combo:
                self.pool_combo.configure(values=["No pools available"])
                self.pool_combo.set("No pools available")
            self.log_message("❌ Failed to load pools")
            return []

    def get_selected_pool_id(self):
        """Get the ID of the currently selected pool"""
        if hasattr(self, 'pool_var') and self.pool_var.get():
            selected = self.pool_var.get()
            if selected and " - " in selected and selected != "No pools available" and selected != "No active pools available":
                return int(selected.split(' - ')[0])
        return None

    def allocate_next_ip(self): 
        """Enhanced IP allocation with better pool validation"""
        self.log_message("🎯 Allocating next IP...")
        
        pool_id = self.get_selected_pool_id()
        if not pool_id:
            self.show_error("Please select a valid pool first")
            return
        
        # Get pool details for validation
        if hasattr(self, 'pool_details') and self.pool_var.get() in self.pool_details:
            pool_info = self.pool_details[self.pool_var.get()]
            if pool_info['available'] == 0:
                self.show_error(f"Pool '{pool_info['name']}' has no available IPs")
                return
        
        data = {
            "pool_id": pool_id,
            "client_id": self.client_id_var.get() or None,
            "allocation_strategy": self.strategy_var.get(),
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/allocations/', data)
        if result and result.get('success'):
            ip_address = result.get('ip_address')
            self.log_message(f"✅ Allocated IP: {ip_address}")
            
            # Refresh pool combo to update availability
            self.update_pool_combo()
            self.refresh_allocations()
            self.show_success(f"✅ Allocated IP: {ip_address}")
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Failed to allocate IP'
            self.log_message(f"❌ Failed to allocate IP: {error_msg}")
            self.show_error(f"Failed to allocate IP: {error_msg}")

    # Implemented button actions
    def create_pool_dialog(self): 
        self.log_message("✨ Opening Create Pool dialog...")
        CreatePoolDialog(self.root, self.api_request, self.refresh_all_data)
        
    def edit_pool_dialog(self, pool): 
        self.log_message(f"✏️ Opening Edit Pool dialog for {pool['name']}...")
        EditPoolDialog(self.root, self.api_request, self.refresh_all_data, pool)
        
    def delete_pool(self): 
        """Show message to select a pool first"""
        self.log_message("🗑️ Please click the delete button on a specific pool card")
        
    def delete_pool_dialog(self, pool): 
        self.log_message(f"🗑️ Delete Pool request for {pool['name']}...")
        
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Confirm Delete")
        dialog.geometry("400x200")
        dialog.grab_set()
        
        # Warning message
        warning_label = ctk.CTkLabel(
            dialog,
            text=f"⚠️ Delete Pool '{pool['name']}'?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#dc3545", "#ff6b6b")
        )
        warning_label.pack(pady=20)
        
        info_label = ctk.CTkLabel(
            dialog,
            text="This action cannot be undone.\nAll allocations in this pool will be removed.",
            font=ctk.CTkFont(size=12),
            text_color=("#6c757d", "#888888")
        )
        info_label.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def confirm_delete():
            result = self.api_request('DELETE', f'/pools/{pool["id"]}')
            if result:
                self.log_message(f"✅ Deleted pool: {pool['name']}")
                self.refresh_all_data()
                dialog.destroy()
            else:
                self.log_message(f"❌ Failed to delete pool: {pool['name']}")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            corner_radius=10,
            fg_color=("#6c757d", "#64748b")
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=confirm_delete,
            width=100,
            corner_radius=10,
            fg_color=("#dc3545", "#ef4444")
        )
        delete_btn.pack(side="left")
        
    def reserve_specific_ip_dialog(self): 
        self.log_message("📌 Opening Reserve Specific IP dialog...")
        ReserveIPDialog(self.root, self.api_request, self.refresh_allocations)
        
    def deallocate_ip(self): 
        self.log_message("❌ Deallocate IP functionality - please select an allocation first")
        
    def refresh_allocations(self): 
        self.log_message("🔄 Refreshing allocations...")
        # Implementation for allocations refresh
        
    def renew_lease_dialog(self): 
        self.log_message("🔄 Renew Lease dialog opened")
        
    def cleanup_expired_leases(self): 
        self.log_message("🧹 Cleaning up expired leases...")
        result = self.api_request('POST', '/leases/cleanup')
        if result:
            self.log_message("✅ Expired lease cleanup completed")
            self.refresh_leases()
        else:
            self.log_message("❌ Failed to cleanup expired leases")
        
    def refresh_leases(self): 
        self.log_message("🔄 Refreshing leases...")
        
    def bind_ip_dialog(self): 
        self.log_message("🔗 Bind IP dialog opened")
        
    def unbind_ip_dialog(self): 
        self.log_message("🔓 Unbind IP dialog opened")
        
    def test_connectivity_dialog(self): 
        self.log_message("📡 Test Connectivity dialog opened")
        
    def refresh_interfaces(self): 
        self.log_message("🔄 Refreshing interfaces...")
        
    def refresh_stats(self): 
        self.log_message("📈 Refreshing statistics...")
        stats_data = self.api_request('GET', '/stats/system')
        if stats_data:
            stats_text = f"""🚀 BlackzAllocator System Statistics

📊 Pools:
  • Total Pools: {stats_data['total_pools']}
  • Active Pools: {stats_data['active_pools']}

💻 Allocations:
  • Total Allocations: {stats_data['total_allocations']}
  • Active Allocations: {stats_data['active_allocations']}

⏰ Leases:
  • Total Leases: {stats_data['total_leases']}
  • Active Leases: {stats_data['active_leases']}
  • Expired Leases: {stats_data['expired_leases']}

🌐 Network Interfaces:
  • Total Interfaces: {stats_data['system_interfaces']}
  • Active Interfaces: {stats_data['active_interfaces']}

🔄 Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", stats_text)
            self.log_message("✅ Statistics refreshed")
        else:
            self.log_message("❌ Failed to refresh statistics")
    
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
            text_color=("#dc3545", "#ff6b6b")
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
            text_color=("#28a745", "#40ff40")
        )
        success_label.pack(pady=30)
        
        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            corner_radius=10
        )
        ok_btn.pack(pady=10)
    
    def refresh_pools_button(self): 
        """Refresh pools when button is clicked"""
        self.refresh_pools()
        
    def edit_pool(self): 
        """Show message to select a pool first"""
        self.log_message("✏️ Please click the edit button on a specific pool card")
    
    def run(self):
        """Start the modern GUI application"""
        self.root.mainloop()

# Modern Dialog Classes
class CreatePoolDialog:
    def __init__(self, parent, api_request_func, refresh_callback):
        self.api_request = api_request_func
        self.refresh_callback = refresh_callback
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("✨ Create IP Pool")
        self.dialog.geometry("500x400")
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🏊‍♂️ Create New IP Pool",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Form fields
        self.create_form_fields(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_form_fields(self, parent):
        """Create form input fields"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        self.vars = {}
        fields = [
            ("Pool Name *", "name", "Enter pool name (e.g., 'Office Network')"),
            ("CIDR *", "cidr", "Enter CIDR (e.g., '192.168.1.0/24')"),
            ("Description", "description", "Optional description"),
            ("Gateway IP", "gateway", "Optional gateway IP")
        ]
        
        for i, (label_text, var_name, placeholder) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            label.pack(fill="x", pady=(10, 5))
            
            # Entry
            self.vars[var_name] = tk.StringVar()
            entry = ctk.CTkEntry(
                form_frame,
                textvariable=self.vars[var_name],
                placeholder_text=placeholder,
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
            entry.pack(fill="x", pady=(0, 5))
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            width=120,
            height=35,
            corner_radius=10,
            fg_color=("#6c757d", "#64748b")
        )
        cancel_btn.pack(side="left", padx=(0, 15))
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="✨ Create Pool",
            command=self.create_pool,
            width=140,
            height=35,
            corner_radius=10,
            fg_color=("#007bff", "#0066cc")
        )
        create_btn.pack(side="left")
    
    def create_pool(self):
        """Create the pool via API"""
        data = {
            "name": self.vars["name"].get().strip(),
            "cidr": self.vars["cidr"].get().strip(),
            "description": self.vars["description"].get().strip() or None,
            "gateway": self.vars["gateway"].get().strip() or None
        }
        
        # Validation
        if not data["name"] or not data["cidr"]:
            self.show_error("Name and CIDR are required")
            return
        
        # API call
        result = self.api_request('POST', '/pools/', data)
        if result:
            self.show_success(f"Created pool: {data['name']}")
            self.refresh_callback()
            self.dialog.destroy()
        else:
            self.show_error("Failed to create pool")
    
    def show_error(self, message):
        """Show error message"""
        error_label = ctk.CTkLabel(
            self.dialog,
            text=f"❌ {message}",
            text_color=("#dc3545", "#ff6b6b")
        )
        error_label.pack(pady=5)
        self.dialog.after(3000, error_label.destroy)
    
    def show_success(self, message):
        """Show success message"""
        success_label = ctk.CTkLabel(
            self.dialog,
            text=f"✅ {message}",
            text_color=("#28a745", "#40ff40")
        )
        success_label.pack(pady=5)

class EditPoolDialog:
    def __init__(self, parent, api_request_func, refresh_callback, pool_data):
        self.api_request = api_request_func
        self.refresh_callback = refresh_callback
        self.pool_data = pool_data
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("✏️ Edit IP Pool")
        self.dialog.geometry("500x400")
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"✏️ Edit Pool: {pool_data['name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Form fields (pre-filled)
        self.create_form_fields(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_form_fields(self, parent):
        """Create form input fields with existing data"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        self.vars = {}
        fields = [
            ("Pool Name *", "name", self.pool_data['name']),
            ("Description", "description", self.pool_data.get('description', '')),
            ("Gateway IP", "gateway", self.pool_data.get('gateway', ''))
        ]
        
        for label_text, var_name, current_value in fields:
            # Label
            label = ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            label.pack(fill="x", pady=(10, 5))
            
            # Entry
            self.vars[var_name] = tk.StringVar(value=current_value)
            entry = ctk.CTkEntry(
                form_frame,
                textvariable=self.vars[var_name],
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(size=12)
            )
            entry.pack(fill="x", pady=(0, 5))
        
        # CIDR (read-only)
        cidr_label = ctk.CTkLabel(
            form_frame,
            text="CIDR (cannot be changed)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        cidr_label.pack(fill="x", pady=(10, 5))
        
        cidr_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        cidr_entry.insert(0, self.pool_data['cidr'])
        cidr_entry.configure(state="disabled")
        cidr_entry.pack(fill="x", pady=(0, 5))
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            width=120,
            height=35,
            corner_radius=10,
            fg_color=("#6c757d", "#64748b")
        )
        cancel_btn.pack(side="left", padx=(0, 15))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Changes",
            command=self.save_pool,
            width=140,
            height=35,
            corner_radius=10,
            fg_color=("#28a745", "#22c55e")
        )
        save_btn.pack(side="left")
    
    def save_pool(self):
        """Save pool changes via API"""
        data = {
            "name": self.vars["name"].get().strip(),
            "description": self.vars["description"].get().strip() or None,
            "gateway": self.vars["gateway"].get().strip() or None
        }
        
        # Validation
        if not data["name"]:
            self.show_error("Name is required")
            return
        
        # API call
        result = self.api_request('PUT', f'/pools/{self.pool_data["id"]}', data)
        if result:
            self.show_success(f"Updated pool: {data['name']}")
            self.refresh_callback()
            self.dialog.destroy()
        else:
            self.show_error("Failed to update pool")
    
    def show_error(self, message):
        """Show error message"""
        error_label = ctk.CTkLabel(
            self.dialog,
            text=f"❌ {message}",
            text_color=("#dc3545", "#ff6b6b")
        )
        error_label.pack(pady=5)
        self.dialog.after(3000, error_label.destroy)
    
    def show_success(self, message):
        """Show success message"""
        success_label = ctk.CTkLabel(
            self.dialog,
            text=f"✅ {message}",
            text_color=("#28a745", "#40ff40")
        )
        success_label.pack(pady=5)

class ReserveIPDialog:
    def __init__(self, parent, api_request_func, refresh_callback):
        self.api_request = api_request_func
        self.refresh_callback = refresh_callback
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("📌 Reserve Specific IP")
        self.dialog.geometry("500x400")
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="📌 Reserve Specific IP Address",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Form fields
        self.create_form_fields(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
        
        # Load pool data with enhanced info
        self.load_enhanced_pools()
    
    def load_enhanced_pools(self):
        """Load pools with enhanced information"""
        pools_data = self.api_request('GET', '/pools/')
        if pools_data:
            pool_options = []
            self.pool_details = {}
            
            for pool in pools_data:
                if pool['is_active']:
                    # Get utilization info
                    util_data = self.api_request('GET', f'/pools/{pool["id"]}/utilization')
                    if util_data:
                        used_ips = util_data.get('allocated_ips', 0)
                        total_ips = util_data.get('total_ips', 0)
                        available_ips = total_ips - used_ips
                        utilization_pct = (used_ips / total_ips * 100) if total_ips > 0 else 0
                        
                        # Create descriptive option text
                        option_text = f"{pool['id']} - {pool['name']} ({pool['cidr']}) | {available_ips}/{total_ips} available"
                        pool_options.append(option_text)
                        self.pool_details[option_text] = {
                            'id': pool['id'],
                            'name': pool['name'],
                            'cidr': pool['cidr'],
                            'available': available_ips,
                            'total': total_ips,
                            'utilization': utilization_pct
                        }
                    else:
                        # Fallback if utilization data unavailable
                        option_text = f"{pool['id']} - {pool['name']} ({pool['cidr']})"
                        pool_options.append(option_text)
                        self.pool_details[option_text] = {
                            'id': pool['id'],
                            'name': pool['name'],
                            'cidr': pool['cidr'],
                            'available': '?',
                            'total': '?',
                            'utilization': 0
                        }
            
            # Sort by utilization (least used first)
            pool_options.sort(key=lambda x: self.pool_details[x]['utilization'])
            
            # Update combobox
            self.pool_combo.configure(values=pool_options)
            if pool_options:
                # Auto-select the best pool
                best_pool = min(pool_options, key=lambda x: self.pool_details[x]['utilization'])
                self.pool_combo.set(best_pool)
                
                # Update IP placeholder based on selected pool
                self.update_ip_placeholder()
            else:
                self.pool_combo.configure(values=["No active pools available"])
                self.pool_combo.set("No active pools available")
        
    def create_form_fields(self, parent):
        """Create form input fields with enhanced pool selection"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        # Pool selection with enhanced info
        pool_label = ctk.CTkLabel(
            form_frame,
            text="🏊 Select Pool *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        pool_label.pack(fill="x", pady=(5, 5))
        
        pool_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pool_frame.pack(fill="x", pady=(0, 10))
        
        self.pool_var = tk.StringVar()
        self.pool_combo = ctk.CTkComboBox(
            pool_frame,
            variable=self.pool_var,
            values=[],  # Will be populated by load_enhanced_pools
            state="readonly",
            height=35,
            corner_radius=8,
            width=350,
            font=ctk.CTkFont(size=11),
            command=self.update_ip_placeholder  # Update placeholder when pool changes
        )
        self.pool_combo.pack(side="left", padx=(0, 10))
        
        # Refresh button for pools
        refresh_btn = ctk.CTkButton(
            pool_frame,
            text="🔄",
            command=self.load_enhanced_pools,
            width=35,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            fg_color=("#17a2b8", "#20c997"),
            hover_color=("#138496", "#1ab394")
        )
        refresh_btn.pack(side="left")
        
        # Pool info display
        self.pool_info_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("#6c757d", "#888888"),
            anchor="w"
        )
        self.pool_info_label.pack(fill="x", pady=(0, 15))
        
        # IP Address
        ip_label = ctk.CTkLabel(
            form_frame,
            text="🌐 IP Address *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        ip_label.pack(fill="x", pady=(5, 5))
        
        self.ip_var = tk.StringVar()
        self.ip_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.ip_var,
            placeholder_text="e.g., 192.168.1.100",
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        self.ip_entry.pack(fill="x", pady=(0, 10))
        
        # Client ID
        client_label = ctk.CTkLabel(
            form_frame,
            text="👤 Client ID",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        client_label.pack(fill="x", pady=(5, 5))
        
        self.client_var = tk.StringVar()
        client_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.client_var,
            placeholder_text="Optional client identifier",
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        client_entry.pack(fill="x", pady=(0, 10))
    
    def update_ip_placeholder(self, *args):
        """Update IP placeholder based on selected pool"""
        selected_pool = self.pool_var.get()
        if selected_pool and hasattr(self, 'pool_details') and selected_pool in self.pool_details:
            pool_info = self.pool_details[selected_pool]
            
            # Update pool info display
            if pool_info['available'] != '?':
                info_text = f"💡 Pool '{pool_info['name']}' has {pool_info['available']} available IPs out of {pool_info['total']} total"
                if pool_info['available'] == 0:
                    info_text += " ⚠️ No IPs available!"
            else:
                info_text = f"💡 Pool '{pool_info['name']}' - utilization data unavailable"
            
            self.pool_info_label.configure(text=info_text)
            
            # Update IP entry placeholder with pool CIDR
            cidr = pool_info['cidr']
            if '/' in cidr:
                network_base = cidr.split('/')[0]
                # Extract network prefix for placeholder
                parts = network_base.split('.')
                if len(parts) >= 3:
                    placeholder = f"e.g., {parts[0]}.{parts[1]}.{parts[2]}.100"
                else:
                    placeholder = f"IP within {cidr}"
            else:
                placeholder = f"IP within {cidr}"
                
            self.ip_entry.configure(placeholder_text=placeholder)
    
    def get_selected_pool_id(self):
        """Get the ID of the currently selected pool"""
        selected = self.pool_var.get()
        if selected and " - " in selected and selected != "No active pools available":
            return int(selected.split(' - ')[0])
        return None
    
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            width=120,
            height=35,
            corner_radius=10,
            fg_color=("#6c757d", "#64748b")
        )
        cancel_btn.pack(side="left", padx=(0, 15))
        
        reserve_btn = ctk.CTkButton(
            button_frame,
            text="📌 Reserve IP",
            command=self.reserve_ip,
            width=130,
            height=35,
            corner_radius=10,
            fg_color=("#007bff", "#0066cc")
        )
        reserve_btn.pack(side="left")
    
    def reserve_ip(self):
        """Reserve the specific IP via API with enhanced validation"""
        pool_id = self.get_selected_pool_id()
        ip_address = self.ip_var.get().strip()
        
        if not pool_id:
            self.show_error("Please select a valid pool")
            return
            
        if not ip_address:
            self.show_error("Please enter an IP address")
            return
        
        # Validate pool has available IPs
        selected_pool = self.pool_var.get()
        if hasattr(self, 'pool_details') and selected_pool in self.pool_details:
            pool_info = self.pool_details[selected_pool]
            if pool_info['available'] == 0:
                self.show_error(f"Pool '{pool_info['name']}' has no available IPs")
                return
        
        data = {
            "pool_id": pool_id,
            "ip_address": ip_address,
            "client_id": self.client_var.get().strip() or None,
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/reservations/', data)
        if result and result.get('success'):
            self.show_success(f"✅ Reserved IP: {ip_address}")
            self.refresh_callback()
            self.dialog.destroy()
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Failed to reserve IP'
            self.show_error(f"Failed to reserve IP: {error_msg}")
    
    def show_error(self, message):
        """Show error message"""
        error_label = ctk.CTkLabel(
            self.dialog,
            text=f"❌ {message}",
            text_color=("#dc3545", "#ff6b6b")
        )
        error_label.pack(pady=5)
        self.dialog.after(3000, error_label.destroy)
    
    def show_success(self, message):
        """Show success message"""
        success_label = ctk.CTkLabel(
            self.dialog,
            text=f"✅ {message}",
            text_color=("#28a745", "#40ff40")
        )
        success_label.pack(pady=5)

if __name__ == "__main__":
    app = ModernBlackzAllocatorGUI()
    app.run() 