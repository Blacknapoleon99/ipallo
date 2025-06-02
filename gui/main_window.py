import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import threading
from typing import Optional, Dict, Any
from datetime import datetime
import asyncio

class BlackzAllocatorGUI:
    """Main GUI application for BlackzAllocator"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BlackzAllocator - Professional IP Pool Management")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        self.root.minsize(1200, 800)
        
        # API base URL
        self.api_base = "http://localhost:8000"
        
        # Configure modern style
        self.setup_modern_styles()
        
        # Create main interface
        self.create_widgets()
        
        # Initialize data
        self.refresh_all_data()
    
    def setup_modern_styles(self):
        """Setup modern dark theme styles with smooth appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern dark color scheme
        colors = {
            'bg_primary': '#1e1e1e',      # Main background
            'bg_secondary': '#2d2d2d',    # Secondary background
            'bg_tertiary': '#3d3d3d',     # Tertiary background
            'accent_blue': '#0078d4',     # Primary accent
            'accent_green': '#00d26a',    # Success/connected
            'accent_orange': '#ff8c00',   # Warning
            'accent_red': '#ff6b6b',      # Error/danger
            'text_primary': '#ffffff',    # Primary text
            'text_secondary': '#b0b0b0',  # Secondary text
            'border': '#404040'           # Border color
        }
        
        # Configure modern button styles
        style.configure('Modern.TButton',
                       background='#0078d4',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', '#106ebe'), ('pressed', '#005a9e')])
        
        style.configure('Success.TButton',
                       background='#00d26a',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Success.TButton',
                 background=[('active', '#00b359'), ('pressed', '#009946')])
        
        style.configure('Warning.TButton',
                       background='#ff8c00',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Warning.TButton',
                 background=[('active', '#e67c00'), ('pressed', '#cc6f00')])
        
        style.configure('Danger.TButton',
                       background='#ff6b6b',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Danger.TButton',
                 background=[('active', '#ff5252'), ('pressed', '#ff3939')])
        
        # Modern labels
        style.configure('Title.TLabel', 
                       foreground='#ffffff', 
                       background='#1e1e1e',
                       font=('Segoe UI', 18, 'bold'))
        
        style.configure('Heading.TLabel',
                       foreground='#ffffff',
                       background='#1e1e1e',
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Status.TLabel',
                       foreground='#00d26a',
                       background='#1e1e1e',
                       font=('Segoe UI', 11))
        
        # Modern notebook (tabs)
        style.configure('TNotebook',
                       background='#1e1e1e',
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background='#2d2d2d',
                       foreground='#b0b0b0',
                       padding=(20, 12),
                       font=('Segoe UI', 10),
                       borderwidth=0)
        
        style.map('TNotebook.Tab',
                 background=[('selected', '#3d3d3d'), ('active', '#353535')],
                 foreground=[('selected', '#ffffff'), ('active', '#ffffff')])
        
        # Modern treeview
        style.configure('Treeview',
                       background='#2d2d2d',
                       foreground='#ffffff',
                       fieldbackground='#2d2d2d',
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure('Treeview.Heading',
                       background='#3d3d3d',
                       foreground='#ffffff',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Treeview',
                 background=[('selected', '#0078d4')],
                 foreground=[('selected', '#ffffff')])
        
        # Modern frames
        style.configure('TFrame',
                       background='#1e1e1e',
                       borderwidth=0)
        
        # Modern entry and combobox
        style.configure('TEntry',
                       fieldbackground='#2d2d2d',
                       foreground='#ffffff',
                       borderwidth=1,
                       insertcolor='#ffffff')
        
        style.configure('TCombobox',
                       fieldbackground='#2d2d2d',
                       foreground='#ffffff',
                       borderwidth=1)
    
    def create_widgets(self):
        """Create the main GUI widgets with modern styling"""
        # Modern header with gradient-like appearance
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title section with modern typography
        title_section = tk.Frame(header_frame, bg='#1e1e1e')
        title_section.pack(fill='both', expand=True, padx=30, pady=20)
        
        title_label = ttk.Label(title_section, text="BlackzAllocator", style='Title.TLabel')
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(title_section, 
                                 text="Professional IP Pool Management", 
                                 bg='#1e1e1e', 
                                 fg='#b0b0b0',
                                 font=('Segoe UI', 12))
        subtitle_label.pack(side='left', padx=(20, 0))
        
        # Modern status indicator
        status_frame = tk.Frame(title_section, bg='#1e1e1e')
        status_frame.pack(side='right')
        
        # Status indicator with modern design
        status_container = tk.Frame(status_frame, bg='#2d2d2d', relief='flat', bd=0)
        status_container.pack(padx=10, pady=5)
        
        # Status dot
        self.status_dot = tk.Label(status_container, text="●", 
                                  bg='#2d2d2d', fg='#00d26a', 
                                  font=('Segoe UI', 16))
        self.status_dot.pack(side='left', padx=(10, 5))
        
        self.status_label = tk.Label(status_container, text="Ready", 
                                    bg='#2d2d2d', fg='#00d26a',
                                    font=('Segoe UI', 11, 'bold'))
        self.status_label.pack(side='left', padx=(0, 10), pady=8)
        
        # Separator line
        separator = tk.Frame(self.root, height=1, bg='#404040')
        separator.pack(fill='x', pady=(0, 1))
        
        # Create modern notebook for tabs
        notebook_frame = tk.Frame(self.root, bg='#1e1e1e')
        notebook_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs with modern styling
        self.create_pools_tab()
        self.create_allocations_tab()
        self.create_leases_tab()
        self.create_interfaces_tab()
        self.create_monitoring_tab()
    
    def create_modern_toolbar(self, parent, buttons):
        """Create a modern toolbar with styled buttons"""
        toolbar = tk.Frame(parent, bg='#2d2d2d', height=60)
        toolbar.pack(fill='x', padx=0, pady=(0, 20))
        toolbar.pack_propagate(False)
        
        # Create button container with padding
        button_container = tk.Frame(toolbar, bg='#2d2d2d')
        button_container.pack(side='left', padx=20, pady=15)
        
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_container, text=text, command=command, style=style)
            btn.pack(side='left', padx=(0, 15) if i < len(buttons)-1 else 0)
        
        return toolbar
    
    def create_modern_treeview_container(self, parent, columns, headings):
        """Create a modern treeview with styling"""
        # Container with subtle border
        container = tk.Frame(parent, bg='#404040', bd=1, relief='solid')
        container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Inner frame
        inner_frame = tk.Frame(container, bg='#2d2d2d')
        inner_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Treeview
        tree = ttk.Treeview(inner_frame, columns=columns, show='headings')
        
        # Configure headings
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=150, minwidth=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(inner_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        return tree
    
    def create_pools_tab(self):
        """Create IP Pools management tab"""
        pools_frame = ttk.Frame(self.notebook)
        self.notebook.add(pools_frame, text="IP Pools")
        
        # Modern toolbar
        toolbar = self.create_modern_toolbar(pools_frame, [
            ("Create Pool", self.create_pool_dialog, 'Modern.TButton'),
            ("Edit Pool", self.edit_pool, 'Modern.TButton'),
            ("Delete Pool", self.delete_pool, 'Danger.TButton'),
            ("Refresh", self.refresh_pools, 'Modern.TButton')
        ])
        
        # Modern pools treeview
        self.pools_tree = self.create_modern_treeview_container(
            pools_frame, 
            ('ID', 'Name', 'CIDR', 'Gateway', 'Active', 'Utilization'), 
            ['ID', 'Pool Name', 'CIDR', 'Gateway', 'Active', 'Utilization %']
        )
        
        # Configure column widths
        self.pools_tree.column('ID', width=60, minwidth=50)
        self.pools_tree.column('Name', width=180, minwidth=150)
        self.pools_tree.column('CIDR', width=140, minwidth=120)
        self.pools_tree.column('Gateway', width=140, minwidth=120)
        self.pools_tree.column('Active', width=80, minwidth=80)
        self.pools_tree.column('Utilization', width=120, minwidth=100)
        
        # Modern pool details frame
        details_frame = tk.LabelFrame(pools_frame, text="Pool Details", 
                                     bg='#2d2d2d', fg='#ffffff',
                                     font=('Segoe UI', 10, 'bold'),
                                     bd=1, relief='solid')
        details_frame.pack(fill='x', padx=0, pady=(20, 0))
        
        self.pool_details_text = tk.Text(details_frame, height=6, 
                                        bg='#1e1e1e', fg='#ffffff', 
                                        wrap='word', bd=0,
                                        font=('Segoe UI', 10),
                                        insertbackground='#ffffff')
        self.pool_details_text.pack(fill='x', padx=15, pady=15)
        
        # Bind selection event
        self.pools_tree.bind('<<TreeviewSelect>>', self.on_pool_select)
    
    def create_allocations_tab(self):
        """Create IP Allocations management tab"""
        alloc_frame = ttk.Frame(self.notebook)
        self.notebook.add(alloc_frame, text="IP Allocations")
        
        # Modern control panel
        control_panel = tk.Frame(alloc_frame, bg='#2d2d2d', height=80)
        control_panel.pack(fill='x', padx=0, pady=(0, 20))
        control_panel.pack_propagate(False)
        
        # Control panel content
        control_content = tk.Frame(control_panel, bg='#2d2d2d')
        control_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # First row - Pool and Strategy selection
        row1 = tk.Frame(control_content, bg='#2d2d2d')
        row1.pack(fill='x', pady=(0, 10))
        
        tk.Label(row1, text="Pool:", bg='#2d2d2d', fg='#ffffff', 
                font=('Segoe UI', 10)).pack(side='left', padx=(0, 10))
        self.pool_var = tk.StringVar()
        self.pool_combo = ttk.Combobox(row1, textvariable=self.pool_var, 
                                      state='readonly', width=25, font=('Segoe UI', 10))
        self.pool_combo.pack(side='left', padx=(0, 30))
        
        tk.Label(row1, text="Strategy:", bg='#2d2d2d', fg='#ffffff',
                font=('Segoe UI', 10)).pack(side='left', padx=(0, 10))
        self.strategy_var = tk.StringVar(value="first_fit")
        strategy_combo = ttk.Combobox(row1, textvariable=self.strategy_var, 
                                    values=["first_fit", "random", "sequential", "load_balanced"], 
                                    state='readonly', width=20, font=('Segoe UI', 10))
        strategy_combo.pack(side='left', padx=(0, 30))
        
        tk.Label(row1, text="Client ID:", bg='#2d2d2d', fg='#ffffff',
                font=('Segoe UI', 10)).pack(side='left', padx=(0, 10))
        self.client_id_var = tk.StringVar()
        client_entry = ttk.Entry(row1, textvariable=self.client_id_var, width=20,
                               font=('Segoe UI', 10))
        client_entry.pack(side='left')
        
        # Second row - Action buttons
        row2 = tk.Frame(control_content, bg='#2d2d2d')
        row2.pack(fill='x')
        
        ttk.Button(row2, text="Allocate Next IP", command=self.allocate_next_ip, 
                  style='Success.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(row2, text="Reserve Specific IP", command=self.reserve_specific_ip_dialog, 
                  style='Modern.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(row2, text="Deallocate", command=self.deallocate_ip, 
                  style='Danger.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(row2, text="Refresh", command=self.refresh_allocations, 
                  style='Modern.TButton').pack(side='left')
        
        # Modern allocations treeview
        self.allocations_tree = self.create_modern_treeview_container(
            alloc_frame,
            ('ID', 'Pool', 'IP', 'Client', 'Type', 'Strategy', 'Interface', 'Status', 'Assigned'),
            ['ID', 'Pool ID', 'IP Address', 'Client ID', 'Type', 'Strategy', 'Interface', 'Status', 'Assigned At']
        )
    
    def create_leases_tab(self):
        """Create IP Leases management tab"""
        leases_frame = ttk.Frame(self.notebook)
        self.notebook.add(leases_frame, text="IP Leases")
        
        # Modern toolbar
        toolbar = self.create_modern_toolbar(leases_frame, [
            ("Renew Lease", self.renew_lease_dialog, 'Success.TButton'),
            ("Cleanup Expired", self.cleanup_expired_leases, 'Warning.TButton'),
            ("Refresh", self.refresh_leases, 'Modern.TButton')
        ])
        
        # Modern leases treeview
        self.leases_tree = self.create_modern_treeview_container(
            leases_frame,
            ('ID', 'Pool', 'IP', 'Start', 'End', 'Duration', 'Renewals', 'Remaining', 'Status'),
            ['ID', 'Pool ID', 'IP Address', 'Start Time', 'End Time', 'Duration (h)', 'Renewals', 'Time Remaining', 'Status']
        )
    
    def create_interfaces_tab(self):
        """Create Network Interfaces management tab"""
        interfaces_frame = ttk.Frame(self.notebook)
        self.notebook.add(interfaces_frame, text="Network Interfaces")
        
        # Modern toolbar
        toolbar = self.create_modern_toolbar(interfaces_frame, [
            ("Bind IP", self.bind_ip_dialog, 'Success.TButton'),
            ("Unbind IP", self.unbind_ip_dialog, 'Warning.TButton'),
            ("Test Connectivity", self.test_connectivity_dialog, 'Modern.TButton'),
            ("Refresh", self.refresh_interfaces, 'Modern.TButton')
        ])
        
        # Modern interfaces treeview
        self.interfaces_tree = self.create_modern_treeview_container(
            interfaces_frame,
            ('Name', 'Description', 'MAC', 'IPs', 'Active', 'Virtual', 'Binding'),
            ['Interface Name', 'Description', 'MAC Address', 'Current IPs', 'Active', 'Virtual', 'Supports Binding']
        )
    
    def create_monitoring_tab(self):
        """Create monitoring and statistics tab"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="Monitoring")
        
        # Modern stats frame
        stats_frame = tk.LabelFrame(monitor_frame, text="System Statistics", 
                                   bg='#2d2d2d', fg='#ffffff',
                                   font=('Segoe UI', 10, 'bold'),
                                   bd=1, relief='solid')
        stats_frame.pack(fill='x', padx=0, pady=(0, 20))
        
        self.stats_text = tk.Text(stats_frame, height=12, 
                                 bg='#1e1e1e', fg='#ffffff', 
                                 wrap='word', bd=0,
                                 font=('Segoe UI', 10),
                                 insertbackground='#ffffff')
        self.stats_text.pack(fill='x', padx=15, pady=15)
        
        # Modern refresh button
        refresh_frame = tk.Frame(monitor_frame, bg='#1e1e1e')
        refresh_frame.pack(pady=(0, 20))
        
        ttk.Button(refresh_frame, text="Refresh Statistics", 
                  command=self.refresh_stats, style='Modern.TButton').pack()
        
        # Modern logs frame
        logs_frame = tk.LabelFrame(monitor_frame, text="Activity Log", 
                                  bg='#2d2d2d', fg='#ffffff',
                                  font=('Segoe UI', 10, 'bold'),
                                  bd=1, relief='solid')
        logs_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.logs_text = tk.Text(logs_frame, bg='#1e1e1e', fg='#ffffff', 
                                wrap='word', bd=0,
                                font=('Segoe UI', 10),
                                insertbackground='#ffffff')
        self.logs_text.pack(fill='both', expand=True, padx=15, pady=15)
    
    # API Methods
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
                self.log_message(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log_message(f"Connection Error: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to API server: {str(e)}")
            return None
    
    def log_message(self, message: str):
        """Add message to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    # Data refresh methods
    def refresh_all_data(self):
        """Refresh all data"""
        self.refresh_pools()
        self.refresh_allocations()
        self.refresh_leases()
        self.refresh_interfaces()
        self.refresh_stats()
        self.update_pool_combo()
    
    def refresh_pools(self):
        """Refresh pools data"""
        pools_data = self.api_request('GET', '/pools/')
        if pools_data:
            # Clear existing items
            for item in self.pools_tree.get_children():
                self.pools_tree.delete(item)
            
            # Add pools
            for pool in pools_data:
                # Get utilization
                utilization_data = self.api_request('GET', f'/pools/{pool["id"]}/utilization')
                utilization = utilization_data.get('utilization_percent', 0) if utilization_data else 0
                
                self.pools_tree.insert('', tk.END, values=(
                    pool['id'],
                    pool['name'],
                    pool['cidr'],
                    pool.get('gateway', 'N/A'),
                    'Yes' if pool['is_active'] else 'No',
                    f"{utilization:.1f}%"
                ))
            
            self.log_message(f"Refreshed {len(pools_data)} IP pools")
    
    def refresh_allocations(self):
        """Refresh allocations data"""
        allocations_data = self.api_request('GET', '/allocations/')
        if allocations_data:
            # Clear existing items
            for item in self.allocations_tree.get_children():
                self.allocations_tree.delete(item)
            
            # Add allocations
            for alloc in allocations_data:
                assigned_at = alloc['assigned_at'].split('T')[0] if alloc['assigned_at'] else 'N/A'
                self.allocations_tree.insert('', tk.END, values=(
                    alloc['id'],
                    alloc['pool_id'],
                    alloc['ip_address'],
                    alloc.get('client_id', 'N/A'),
                    alloc['allocation_type'],
                    alloc['allocation_strategy'],
                    alloc.get('network_interface', 'N/A'),
                    alloc['binding_status'],
                    assigned_at
                ))
            
            self.log_message(f"Refreshed {len(allocations_data)} IP allocations")
    
    def refresh_leases(self):
        """Refresh leases data"""
        leases_data = self.api_request('GET', '/leases/')
        if leases_data:
            # Clear existing items
            for item in self.leases_tree.get_children():
                self.leases_tree.delete(item)
            
            # Add leases
            for lease in leases_data:
                start_time = lease['lease_start'].split('T')[0] if lease['lease_start'] else 'N/A'
                end_time = lease['lease_end'].split('T')[0] if lease['lease_end'] else 'N/A'
                duration_hours = lease['lease_duration'] / 3600
                
                time_remaining = "Expired" if lease['is_expired'] else f"{lease.get('time_remaining_seconds', 0) // 3600}h"
                status = "Expired" if lease['is_expired'] else "Active"
                
                # Get allocation IP
                allocation_data = self.api_request('GET', f'/allocations/?skip=0&limit=1000')
                ip_address = "N/A"
                if allocation_data:
                    for alloc in allocation_data:
                        if alloc['id'] == lease['allocation_id']:
                            ip_address = alloc['ip_address']
                            break
                
                self.leases_tree.insert('', tk.END, values=(
                    lease['id'],
                    lease['pool_id'],
                    ip_address,
                    start_time,
                    end_time,
                    f"{duration_hours:.1f}",
                    lease['renewal_count'],
                    time_remaining,
                    status
                ))
            
            self.log_message(f"Refreshed {len(leases_data)} IP leases")
    
    def refresh_interfaces(self):
        """Refresh interfaces data"""
        interfaces_data = self.api_request('GET', '/interfaces/')
        if interfaces_data:
            # Clear existing items
            for item in self.interfaces_tree.get_children():
                self.interfaces_tree.delete(item)
            
            # Add interfaces
            for iface in interfaces_data:
                current_ips = ', '.join(iface['current_ips']) if iface['current_ips'] else 'None'
                self.interfaces_tree.insert('', tk.END, values=(
                    iface['name'],
                    iface['description'],
                    iface['mac_address'],
                    current_ips,
                    'Yes' if iface['is_active'] else 'No',
                    'Yes' if iface['is_virtual'] else 'No',
                    'Yes' if iface['supports_binding'] else 'No'
                ))
            
            self.log_message(f"Refreshed {len(interfaces_data)} network interfaces")
    
    def refresh_stats(self):
        """Refresh system statistics"""
        stats_data = self.api_request('GET', '/stats/system')
        if stats_data:
            stats_text = f"""System Statistics:

Pools:
  • Total Pools: {stats_data['total_pools']}
  • Active Pools: {stats_data['active_pools']}

Allocations:
  • Total Allocations: {stats_data['total_allocations']}
  • Active Allocations: {stats_data['active_allocations']}

Leases:
  • Total Leases: {stats_data['total_leases']}
  • Active Leases: {stats_data['active_leases']}
  • Expired Leases: {stats_data['expired_leases']}

Network Interfaces:
  • Total Interfaces: {stats_data['system_interfaces']}
  • Active Interfaces: {stats_data['active_interfaces']}
"""
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.log_message("Refreshed system statistics")
    
    def update_pool_combo(self):
        """Update pool combobox values"""
        pools_data = self.api_request('GET', '/pools/')
        if pools_data:
            pool_names = [f"{pool['id']} - {pool['name']}" for pool in pools_data if pool['is_active']]
            self.pool_combo['values'] = pool_names
            if pool_names:
                self.pool_combo.set(pool_names[0])
    
    # Event handlers
    def on_pool_select(self, event):
        """Handle pool selection"""
        selection = self.pools_tree.selection()
        if selection:
            item = self.pools_tree.item(selection[0])
            pool_id = item['values'][0]
            
            # Get detailed pool information
            pool_data = self.api_request('GET', f'/pools/{pool_id}')
            if pool_data:
                details = f"""Pool Details:

Name: {pool_data['name']}
CIDR: {pool_data['cidr']}
Description: {pool_data.get('description', 'N/A')}
Gateway: {pool_data.get('gateway', 'N/A')}
DNS Servers: {pool_data.get('dns_servers', 'N/A')}
Reserved Ranges: {pool_data.get('reserved_ranges', 'N/A')}
Created: {pool_data['created_at'].split('T')[0]}
Active: {'Yes' if pool_data['is_active'] else 'No'}
"""
                
                self.pool_details_text.delete(1.0, tk.END)
                self.pool_details_text.insert(1.0, details)
    
    # Dialog methods (simplified implementations)
    def create_pool_dialog(self):
        """Create new pool dialog"""
        dialog = PoolCreateDialog(self.root, self.api_request)
        if dialog.result:
            self.refresh_pools()
            self.update_pool_combo()
    
    def edit_pool(self):
        """Edit selected pool"""
        messagebox.showinfo("Info", "Pool editing feature coming soon!")
    
    def delete_pool(self):
        """Delete selected pool"""
        selection = self.pools_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pool to delete")
            return
        
        item = self.pools_tree.item(selection[0])
        pool_id = item['values'][0]
        pool_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete pool '{pool_name}'?"):
            result = self.api_request('DELETE', f'/pools/{pool_id}')
            if result and result.get('success'):
                self.log_message(f"Deleted pool: {pool_name}")
                self.refresh_pools()
                self.update_pool_combo()
            else:
                messagebox.showerror("Error", "Failed to delete pool")
    
    def allocate_next_ip(self):
        """Allocate next available IP"""
        if not self.pool_var.get():
            messagebox.showwarning("Warning", "Please select a pool")
            return
        
        pool_id = int(self.pool_var.get().split(' - ')[0])
        
        data = {
            "pool_id": pool_id,
            "client_id": self.client_id_var.get() or None,
            "allocation_strategy": self.strategy_var.get(),
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/allocations/', data)
        if result and result.get('success'):
            self.log_message(f"Allocated IP: {result.get('ip_address')}")
            self.refresh_allocations()
            messagebox.showinfo("Success", f"Allocated IP: {result.get('ip_address')}")
        else:
            messagebox.showerror("Error", "Failed to allocate IP")
    
    def reserve_specific_ip_dialog(self):
        """Reserve specific IP dialog"""
        dialog = IPReservationDialog(self.root, self.api_request)
        if dialog.result:
            self.refresh_allocations()
    
    def deallocate_ip(self):
        """Deallocate selected IP"""
        selection = self.allocations_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an allocation to deallocate")
            return
        
        item = self.allocations_tree.item(selection[0])
        allocation_id = item['values'][0]
        ip_address = item['values'][2]
        
        if messagebox.askyesno("Confirm Deallocation", f"Deallocate IP {ip_address}?"):
            result = self.api_request('DELETE', f'/allocations/{allocation_id}')
            if result and result.get('success'):
                self.log_message(f"Deallocated IP: {ip_address}")
                self.refresh_allocations()
                messagebox.showinfo("Success", f"Deallocated IP: {ip_address}")
            else:
                messagebox.showerror("Error", "Failed to deallocate IP")
    
    def renew_lease_dialog(self):
        """Renew lease dialog"""
        messagebox.showinfo("Info", "Lease renewal feature coming soon!")
    
    def cleanup_expired_leases(self):
        """Cleanup expired leases"""
        result = self.api_request('POST', '/leases/cleanup')
        if result and result.get('success'):
            self.log_message("Expired lease cleanup scheduled")
            self.refresh_leases()
            messagebox.showinfo("Success", "Expired lease cleanup scheduled")
        else:
            messagebox.showerror("Error", "Failed to schedule cleanup")
    
    def bind_ip_dialog(self):
        """Bind IP to interface dialog"""
        messagebox.showinfo("Info", "IP binding feature coming soon!")
    
    def unbind_ip_dialog(self):
        """Unbind IP from interface dialog"""
        messagebox.showinfo("Info", "IP unbinding feature coming soon!")
    
    def test_connectivity_dialog(self):
        """Test connectivity dialog"""
        target_ip = simpledialog.askstring("Test Connectivity", "Enter target IP address:")
        if target_ip:
            data = {"target_ip": target_ip}
            result = self.api_request('POST', '/connectivity/test', data)
            if result:
                status = "Success" if result.get('ping_success') else "Failed"
                time_ms = result.get('ping_time_ms', 0)
                messagebox.showinfo("Connectivity Test", f"Target: {target_ip}\nStatus: {status}\nTime: {time_ms:.2f}ms")
            else:
                messagebox.showerror("Error", "Failed to test connectivity")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

# Dialog classes for creating pools and reservations
class PoolCreateDialog:
    def __init__(self, parent, api_request_func):
        self.api_request = api_request_func
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create IP Pool")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#2b2b2b')
        self.dialog.grab_set()
        
        # Form fields
        fields = [
            ("Pool Name:", "name"),
            ("CIDR (e.g. 192.168.1.0/24):", "cidr"),
            ("Description:", "description"),
            ("Gateway IP:", "gateway")
        ]
        
        self.vars = {}
        for i, (label, var_name) in enumerate(fields):
            tk.Label(self.dialog, text=label, bg='#2b2b2b', fg='white').grid(row=i, column=0, sticky='w', padx=10, pady=5)
            self.vars[var_name] = tk.StringVar()
            tk.Entry(self.dialog, textvariable=self.vars[var_name], width=30).grid(row=i, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='#2b2b2b')
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Create", command=self.create_pool, bg='#0078d4', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, bg='#d13438', fg='white').pack(side='left', padx=5)
        
        self.dialog.wait_window()
    
    def create_pool(self):
        data = {
            "name": self.vars["name"].get(),
            "cidr": self.vars["cidr"].get(),
            "description": self.vars["description"].get() or None,
            "gateway": self.vars["gateway"].get() or None
        }
        
        if not data["name"] or not data["cidr"]:
            messagebox.showerror("Error", "Name and CIDR are required")
            return
        
        result = self.api_request('POST', '/pools/', data)
        if result:
            self.result = result
            messagebox.showinfo("Success", f"Created pool: {data['name']}")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to create pool")

class IPReservationDialog:
    def __init__(self, parent, api_request_func):
        self.api_request = api_request_func
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Reserve Specific IP")
        self.dialog.geometry("350x200")
        self.dialog.configure(bg='#2b2b2b')
        self.dialog.grab_set()
        
        # Get pools for selection
        pools_data = self.api_request('GET', '/pools/')
        pool_options = [f"{pool['id']} - {pool['name']}" for pool in pools_data if pool['is_active']] if pools_data else []
        
        # Form fields
        tk.Label(self.dialog, text="Pool:", bg='#2b2b2b', fg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.pool_var = tk.StringVar()
        pool_combo = ttk.Combobox(self.dialog, textvariable=self.pool_var, values=pool_options, state='readonly', width=25)
        pool_combo.grid(row=0, column=1, padx=10, pady=5)
        if pool_options:
            pool_combo.set(pool_options[0])
        
        tk.Label(self.dialog, text="IP Address:", bg='#2b2b2b', fg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.ip_var = tk.StringVar()
        tk.Entry(self.dialog, textvariable=self.ip_var, width=25).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.dialog, text="Client ID:", bg='#2b2b2b', fg='white').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.client_var = tk.StringVar()
        tk.Entry(self.dialog, textvariable=self.client_var, width=25).grid(row=2, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg='#2b2b2b')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Reserve", command=self.reserve_ip, bg='#0078d4', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, bg='#d13438', fg='white').pack(side='left', padx=5)
        
        self.dialog.wait_window()
    
    def reserve_ip(self):
        if not self.pool_var.get() or not self.ip_var.get():
            messagebox.showerror("Error", "Pool and IP address are required")
            return
        
        pool_id = int(self.pool_var.get().split(' - ')[0])
        
        data = {
            "pool_id": pool_id,
            "ip_address": self.ip_var.get(),
            "client_id": self.client_var.get() or None,
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/reservations/', data)
        if result and result.get('success'):
            self.result = result
            messagebox.showinfo("Success", f"Reserved IP: {data['ip_address']}")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to reserve IP")

if __name__ == "__main__":
    app = BlackzAllocatorGUI()
    app.run() 