import subprocess
import psutil
import socket
import platform
from typing import List, Dict, Optional, Tuple
import json
import logging
from dataclasses import dataclass

@dataclass
class NetworkInterfaceInfo:
    """Network interface information"""
    name: str
    display_name: str
    description: str
    mac_address: str
    current_ips: List[str]
    is_active: bool
    is_virtual: bool
    supports_binding: bool

class NetworkInterfaceManager:
    """Manager for network interface operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platform = platform.system().lower()
    
    def get_network_interfaces(self) -> List[NetworkInterfaceInfo]:
        """Get list of all network interfaces"""
        interfaces = []
        
        try:
            # Get interface statistics
            net_if_stats = psutil.net_if_stats()
            net_if_addrs = psutil.net_if_addrs()
            
            for interface_name, addrs in net_if_addrs.items():
                # Skip loopback
                if interface_name.lower() in ['lo', 'loopback']:
                    continue
                
                # Get interface stats
                stats = net_if_stats.get(interface_name)
                is_active = stats.isup if stats else False
                
                # Extract IP addresses and MAC
                ipv4_addresses = []
                mac_address = ""
                
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        ipv4_addresses.append(addr.address)
                    elif addr.family == psutil.AF_LINK:  # MAC address
                        mac_address = addr.address
                
                # Determine if virtual interface
                is_virtual = self._is_virtual_interface(interface_name)
                
                interface_info = NetworkInterfaceInfo(
                    name=interface_name,
                    display_name=interface_name,
                    description=f"Network Interface: {interface_name}",
                    mac_address=mac_address,
                    current_ips=ipv4_addresses,
                    is_active=is_active,
                    is_virtual=is_virtual,
                    supports_binding=is_active and not is_virtual
                )
                
                interfaces.append(interface_info)
                
        except Exception as e:
            self.logger.error(f"Error getting network interfaces: {e}")
        
        return interfaces
    
    def _is_virtual_interface(self, interface_name: str) -> bool:
        """Check if interface is virtual"""
        virtual_keywords = [
            'virtual', 'vm', 'veth', 'docker', 'br-', 'vbox',
            'vmware', 'hyper-v', 'loopback', 'teredo'
        ]
        
        name_lower = interface_name.lower()
        return any(keyword in name_lower for keyword in virtual_keywords)
    
    def ping_ip(self, ip_address: str, timeout: int = 2) -> bool:
        """Ping an IP address to check connectivity"""
        try:
            if self.platform == "windows":
                cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_address]
            else:
                cmd = ["ping", "-c", "1", "-W", str(timeout), ip_address]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 2
            )
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"Error pinging {ip_address}: {e}")
            return False
    
    def validate_ip_availability(self, ip_address: str) -> Tuple[bool, str]:
        """
        Validate if an IP address is available for binding
        
        Returns: (is_available, message)
        """
        try:
            # First, ping the IP to check if it's responding
            if self.ping_ip(ip_address):
                return False, f"IP {ip_address} is already in use (responds to ping)"
            
            # Check if IP is already assigned to any interface
            net_if_addrs = psutil.net_if_addrs()
            for interface_name, addrs in net_if_addrs.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.address == ip_address:
                        return False, f"IP {ip_address} is already assigned to interface {interface_name}"
            
            return True, f"IP {ip_address} appears to be available"
            
        except Exception as e:
            return False, f"Error validating IP availability: {str(e)}"
    
    def bind_ip_to_interface(
        self,
        interface_name: str,
        ip_address: str,
        subnet_mask: str = "255.255.255.0",
        persistent: bool = False
    ) -> Tuple[bool, str]:
        """
        Bind an IP address to a network interface
        
        Returns: (success, message)
        """
        try:
            # Validate interface exists
            if not self._interface_exists(interface_name):
                return False, f"Interface {interface_name} does not exist"
            
            # Validate IP availability
            is_available, validation_msg = self.validate_ip_availability(ip_address)
            if not is_available:
                return False, validation_msg
            
            if self.platform == "windows":
                return self._bind_ip_windows(interface_name, ip_address, subnet_mask, persistent)
            else:
                return self._bind_ip_linux(interface_name, ip_address, subnet_mask, persistent)
                
        except Exception as e:
            error_msg = f"Error binding IP {ip_address} to {interface_name}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def _interface_exists(self, interface_name: str) -> bool:
        """Check if network interface exists"""
        net_if_stats = psutil.net_if_stats()
        return interface_name in net_if_stats
    
    def _bind_ip_windows(
        self,
        interface_name: str,
        ip_address: str,
        subnet_mask: str,
        persistent: bool
    ) -> Tuple[bool, str]:
        """Bind IP on Windows using netsh"""
        try:
            # Get interface index for Windows
            interface_index = self._get_windows_interface_index(interface_name)
            if not interface_index:
                return False, f"Could not get interface index for {interface_name}"
            
            # Add IP address using netsh
            cmd = [
                "netsh", "interface", "ipv4", "add", "address",
                f"name={interface_name}",
                f"address={ip_address}",
                f"mask={subnet_mask}"
            ]
            
            if not persistent:
                cmd.append("store=active")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, f"Successfully bound {ip_address} to {interface_name}"
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"Failed to bind IP: {error_msg}"
                
        except Exception as e:
            return False, f"Windows IP binding error: {str(e)}"
    
    def _bind_ip_linux(
        self,
        interface_name: str,
        ip_address: str,
        subnet_mask: str,
        persistent: bool
    ) -> Tuple[bool, str]:
        """Bind IP on Linux using ip command"""
        try:
            # Convert subnet mask to CIDR notation
            cidr = self._subnet_mask_to_cidr(subnet_mask)
            
            # Add IP address using ip command
            cmd = [
                "ip", "addr", "add",
                f"{ip_address}/{cidr}",
                "dev", interface_name
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                success_msg = f"Successfully bound {ip_address} to {interface_name}"
                
                # For persistent binding, we'd need to modify network configuration files
                if persistent:
                    success_msg += " (Note: Persistent configuration not implemented)"
                
                return True, success_msg
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"Failed to bind IP: {error_msg}"
                
        except Exception as e:
            return False, f"Linux IP binding error: {str(e)}"
    
    def _get_windows_interface_index(self, interface_name: str) -> Optional[str]:
        """Get Windows interface index by name"""
        try:
            cmd = ["netsh", "interface", "show", "interface"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if interface_name in line and "Connected" in line:
                        parts = line.split()
                        if len(parts) > 3:
                            return parts[2]  # Interface index is typically the 3rd column
            
            return None
            
        except Exception:
            return None
    
    def _subnet_mask_to_cidr(self, subnet_mask: str) -> int:
        """Convert subnet mask to CIDR notation"""
        try:
            # Convert subnet mask to binary and count 1s
            mask_parts = subnet_mask.split('.')
            binary = ''.join(format(int(part), '08b') for part in mask_parts)
            return binary.count('1')
        except Exception:
            return 24  # Default to /24
    
    def unbind_ip_from_interface(
        self,
        interface_name: str,
        ip_address: str
    ) -> Tuple[bool, str]:
        """
        Unbind an IP address from a network interface
        
        Returns: (success, message)
        """
        try:
            if self.platform == "windows":
                return self._unbind_ip_windows(interface_name, ip_address)
            else:
                return self._unbind_ip_linux(interface_name, ip_address)
                
        except Exception as e:
            error_msg = f"Error unbinding IP {ip_address} from {interface_name}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def _unbind_ip_windows(self, interface_name: str, ip_address: str) -> Tuple[bool, str]:
        """Unbind IP on Windows using netsh"""
        try:
            cmd = [
                "netsh", "interface", "ipv4", "delete", "address",
                f"name={interface_name}",
                f"address={ip_address}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, f"Successfully unbound {ip_address} from {interface_name}"
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"Failed to unbind IP: {error_msg}"
                
        except Exception as e:
            return False, f"Windows IP unbinding error: {str(e)}"
    
    def _unbind_ip_linux(self, interface_name: str, ip_address: str) -> Tuple[bool, str]:
        """Unbind IP on Linux using ip command"""
        try:
            # Find the IP with its CIDR and remove it
            cmd = ["ip", "addr", "show", "dev", interface_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return False, f"Could not query interface {interface_name}"
            
            # Parse output to find the specific IP with CIDR
            lines = result.stdout.split('\n')
            target_line = None
            for line in lines:
                if f"inet {ip_address}/" in line:
                    target_line = line.strip()
                    break
            
            if not target_line:
                return False, f"IP {ip_address} not found on interface {interface_name}"
            
            # Extract IP with CIDR
            parts = target_line.split()
            ip_with_cidr = None
            for part in parts:
                if part.startswith(ip_address + "/"):
                    ip_with_cidr = part
                    break
            
            if not ip_with_cidr:
                return False, f"Could not determine CIDR for IP {ip_address}"
            
            # Remove the IP
            cmd = ["ip", "addr", "del", ip_with_cidr, "dev", interface_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return True, f"Successfully unbound {ip_address} from {interface_name}"
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return False, f"Failed to unbind IP: {error_msg}"
                
        except Exception as e:
            return False, f"Linux IP unbinding error: {str(e)}"
    
    def get_routing_table(self) -> List[Dict[str, str]]:
        """Get system routing table"""
        routes = []
        
        try:
            if self.platform == "windows":
                cmd = ["route", "print", "-4"]
            else:
                cmd = ["ip", "route", "show"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse routing table (simplified)
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Kernel') and not line.startswith('Destination'):
                        routes.append({"route": line.strip()})
            
        except Exception as e:
            self.logger.error(f"Error getting routing table: {e}")
        
        return routes
    
    def test_connectivity(self, target_ip: str, source_interface: str = None) -> Dict[str, any]:
        """
        Test network connectivity to a target IP
        
        Returns: Dictionary with connectivity test results
        """
        results = {
            "target_ip": target_ip,
            "ping_success": False,
            "ping_time_ms": None,
            "traceroute_hops": [],
            "source_interface": source_interface,
            "timestamp": str(datetime.utcnow())
        }
        
        try:
            # Ping test
            ping_start = time.time()
            ping_success = self.ping_ip(target_ip, timeout=5)
            ping_time = (time.time() - ping_start) * 1000
            
            results["ping_success"] = ping_success
            results["ping_time_ms"] = round(ping_time, 2)
            
            # Simple traceroute (limited implementation)
            if ping_success:
                results["traceroute_hops"] = ["Direct connectivity confirmed"]
            
        except Exception as e:
            results["error"] = str(e)
        
        return results

# Import required modules for connectivity testing
import time
from datetime import datetime 