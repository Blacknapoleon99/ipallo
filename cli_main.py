#!/usr/bin/env python3
"""
BlackzAllocator Command Line Interface

Simple CLI for basic IP allocation operations without GUI.
"""

import sys
import os
import argparse
import requests
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class BlackzAllocatorCLI:
    def __init__(self, api_base="http://localhost:8000"):
        self.api_base = api_base
    
    def api_request(self, method, endpoint, data=None):
        """Make API request"""
        try:
            url = f"{self.api_base}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, timeout=10)
            else:
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {str(e)}")
            print("Make sure the API server is running (python api_server.py)")
            return None
    
    def list_pools(self):
        """List all IP pools"""
        pools = self.api_request('GET', '/pools/')
        if pools:
            print("\nIP Pools:")
            print("-" * 80)
            print(f"{'ID':<4} {'Name':<20} {'CIDR':<18} {'Gateway':<15} {'Active':<8} {'Util %':<8}")
            print("-" * 80)
            
            for pool in pools:
                # Get utilization
                util_data = self.api_request('GET', f'/pools/{pool["id"]}/utilization')
                utilization = util_data.get('utilization_percent', 0) if util_data else 0
                
                print(f"{pool['id']:<4} {pool['name']:<20} {pool['cidr']:<18} "
                      f"{pool.get('gateway', 'N/A'):<15} "
                      f"{'Yes' if pool['is_active'] else 'No':<8} {utilization:<8.1f}")
        else:
            print("No pools found or API error")
    
    def create_pool(self, name, cidr, description=None, gateway=None):
        """Create a new IP pool"""
        data = {
            "name": name,
            "cidr": cidr,
            "description": description,
            "gateway": gateway
        }
        
        result = self.api_request('POST', '/pools/', data)
        if result:
            print(f"✓ Created pool '{name}' with CIDR {cidr}")
        else:
            print(f"✗ Failed to create pool '{name}'")
    
    def delete_pool(self, pool_id):
        """Delete an IP pool"""
        result = self.api_request('DELETE', f'/pools/{pool_id}')
        if result and result.get('success'):
            print(f"✓ Deleted pool {pool_id}")
        else:
            print(f"✗ Failed to delete pool {pool_id}")
    
    def list_allocations(self, pool_id=None):
        """List IP allocations"""
        endpoint = '/allocations/'
        if pool_id:
            endpoint += f'?pool_id={pool_id}'
        
        allocations = self.api_request('GET', endpoint)
        if allocations:
            print("\nIP Allocations:")
            print("-" * 100)
            print(f"{'ID':<4} {'Pool':<6} {'IP Address':<15} {'Client ID':<20} {'Type':<8} {'Status':<10} {'Assigned':<12}")
            print("-" * 100)
            
            for alloc in allocations:
                assigned_date = alloc['assigned_at'].split('T')[0] if alloc['assigned_at'] else 'N/A'
                print(f"{alloc['id']:<4} {alloc['pool_id']:<6} {alloc['ip_address']:<15} "
                      f"{alloc.get('client_id', 'N/A'):<20} {alloc['allocation_type']:<8} "
                      f"{alloc['binding_status']:<10} {assigned_date:<12}")
        else:
            print("No allocations found or API error")
    
    def allocate_ip(self, pool_id, client_id=None, strategy="first_fit"):
        """Allocate next available IP"""
        data = {
            "pool_id": pool_id,
            "client_id": client_id,
            "allocation_strategy": strategy,
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/allocations/', data)
        if result and result.get('success'):
            print(f"✓ Allocated IP: {result.get('ip_address')} from pool {pool_id}")
        else:
            print(f"✗ Failed to allocate IP from pool {pool_id}")
    
    def reserve_ip(self, pool_id, ip_address, client_id=None):
        """Reserve specific IP address"""
        data = {
            "pool_id": pool_id,
            "ip_address": ip_address,
            "client_id": client_id,
            "lease_duration": 86400
        }
        
        result = self.api_request('POST', '/reservations/', data)
        if result and result.get('success'):
            print(f"✓ Reserved IP: {ip_address} in pool {pool_id}")
        else:
            print(f"✗ Failed to reserve IP {ip_address} in pool {pool_id}")
    
    def deallocate_ip(self, allocation_id):
        """Deallocate an IP address"""
        result = self.api_request('DELETE', f'/allocations/{allocation_id}')
        if result and result.get('success'):
            print(f"✓ Deallocated allocation {allocation_id}")
        else:
            print(f"✗ Failed to deallocate allocation {allocation_id}")
    
    def show_stats(self):
        """Show system statistics"""
        stats = self.api_request('GET', '/stats/system')
        if stats:
            print("\nSystem Statistics:")
            print("-" * 40)
            print(f"Total Pools:        {stats['total_pools']}")
            print(f"Active Pools:       {stats['active_pools']}")
            print(f"Total Allocations:  {stats['total_allocations']}")
            print(f"Active Allocations: {stats['active_allocations']}")
            print(f"Total Leases:       {stats['total_leases']}")
            print(f"Active Leases:      {stats['active_leases']}")
            print(f"Expired Leases:     {stats['expired_leases']}")
            print(f"Network Interfaces: {stats['system_interfaces']}")
        else:
            print("Failed to get system statistics")
    
    def ping_test(self, ip_address):
        """Test ping to IP address"""
        result = self.api_request('GET', f'/connectivity/ping/{ip_address}')
        if result:
            status = "SUCCESS" if result.get('ping_success') else "FAILED"
            print(f"Ping test to {ip_address}: {status}")
        else:
            print(f"Failed to test connectivity to {ip_address}")

def main():
    parser = argparse.ArgumentParser(description='BlackzAllocator CLI')
    parser.add_argument('--api-url', default='http://localhost:8000', help='API server URL')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Pool commands
    pool_parser = subparsers.add_parser('pools', help='Pool management')
    pool_subparsers = pool_parser.add_subparsers(dest='pool_action')
    
    pool_subparsers.add_parser('list', help='List pools')
    
    create_pool_parser = pool_subparsers.add_parser('create', help='Create pool')
    create_pool_parser.add_argument('name', help='Pool name')
    create_pool_parser.add_argument('cidr', help='CIDR notation (e.g., 192.168.1.0/24)')
    create_pool_parser.add_argument('--description', help='Pool description')
    create_pool_parser.add_argument('--gateway', help='Gateway IP address')
    
    delete_pool_parser = pool_subparsers.add_parser('delete', help='Delete pool')
    delete_pool_parser.add_argument('pool_id', type=int, help='Pool ID to delete')
    
    # Allocation commands
    alloc_parser = subparsers.add_parser('allocations', help='Allocation management')
    alloc_subparsers = alloc_parser.add_subparsers(dest='alloc_action')
    
    list_alloc_parser = alloc_subparsers.add_parser('list', help='List allocations')
    list_alloc_parser.add_argument('--pool-id', type=int, help='Filter by pool ID')
    
    allocate_parser = alloc_subparsers.add_parser('allocate', help='Allocate next IP')
    allocate_parser.add_argument('pool_id', type=int, help='Pool ID')
    allocate_parser.add_argument('--client-id', help='Client identifier')
    allocate_parser.add_argument('--strategy', default='first_fit', 
                                choices=['first_fit', 'random', 'sequential', 'load_balanced'],
                                help='Allocation strategy')
    
    reserve_parser = alloc_subparsers.add_parser('reserve', help='Reserve specific IP')
    reserve_parser.add_argument('pool_id', type=int, help='Pool ID')
    reserve_parser.add_argument('ip_address', help='IP address to reserve')
    reserve_parser.add_argument('--client-id', help='Client identifier')
    
    dealloc_parser = alloc_subparsers.add_parser('deallocate', help='Deallocate IP')
    dealloc_parser.add_argument('allocation_id', type=int, help='Allocation ID')
    
    # Utility commands
    subparsers.add_parser('stats', help='Show system statistics')
    
    ping_parser = subparsers.add_parser('ping', help='Test connectivity')
    ping_parser.add_argument('ip_address', help='IP address to ping')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = BlackzAllocatorCLI(args.api_url)
    
    try:
        if args.command == 'pools':
            if args.pool_action == 'list':
                cli.list_pools()
            elif args.pool_action == 'create':
                cli.create_pool(args.name, args.cidr, args.description, args.gateway)
            elif args.pool_action == 'delete':
                cli.delete_pool(args.pool_id)
        
        elif args.command == 'allocations':
            if args.alloc_action == 'list':
                cli.list_allocations(args.pool_id if hasattr(args, 'pool_id') else None)
            elif args.alloc_action == 'allocate':
                cli.allocate_ip(args.pool_id, args.client_id, args.strategy)
            elif args.alloc_action == 'reserve':
                cli.reserve_ip(args.pool_id, args.ip_address, args.client_id)
            elif args.alloc_action == 'deallocate':
                cli.deallocate_ip(args.allocation_id)
        
        elif args.command == 'stats':
            cli.show_stats()
        
        elif args.command == 'ping':
            cli.ping_test(args.ip_address)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 