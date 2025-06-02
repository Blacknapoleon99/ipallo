import ipaddress
import json
import random
from typing import List, Optional, Tuple, Dict, Set
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import IPPool, IPAllocation, IPLease, AllocationLog

class AllocationStrategy:
    """Base class for allocation strategies"""
    
    @staticmethod
    def allocate(available_ips: List[str], allocated_ips: Set[str]) -> Optional[str]:
        """Allocate an IP address using the strategy"""
        raise NotImplementedError

class FirstFitStrategy(AllocationStrategy):
    """Allocate the first available IP address"""
    
    @staticmethod
    def allocate(available_ips: List[str], allocated_ips: Set[str]) -> Optional[str]:
        for ip in available_ips:
            if ip not in allocated_ips:
                return ip
        return None

class RandomStrategy(AllocationStrategy):
    """Allocate a random available IP address"""
    
    @staticmethod
    def allocate(available_ips: List[str], allocated_ips: Set[str]) -> Optional[str]:
        available = [ip for ip in available_ips if ip not in allocated_ips]
        return random.choice(available) if available else None

class SequentialStrategy(AllocationStrategy):
    """Allocate IPs sequentially from last allocated"""
    
    @staticmethod
    def allocate(available_ips: List[str], allocated_ips: Set[str]) -> Optional[str]:
        # For sequential, we'll use the same as first fit for simplicity
        # In a more advanced implementation, we'd track the last allocated IP
        return FirstFitStrategy.allocate(available_ips, allocated_ips)

class LoadBalancedStrategy(AllocationStrategy):
    """Allocate IPs to balance load across the range"""
    
    @staticmethod
    def allocate(available_ips: List[str], allocated_ips: Set[str]) -> Optional[str]:
        available = [ip for ip in available_ips if ip not in allocated_ips]
        if not available:
            return None
        
        # Choose an IP from the middle of available range for load balancing
        mid_index = len(available) // 2
        return available[mid_index]

class IPAllocator:
    """Main IP Allocation Engine"""
    
    STRATEGIES = {
        "first_fit": FirstFitStrategy,
        "random": RandomStrategy,
        "sequential": SequentialStrategy,
        "load_balanced": LoadBalancedStrategy
    }
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_pool_utilization(self, pool_id: int) -> Dict[str, any]:
        """Get pool utilization statistics"""
        pool = self.db.query(IPPool).filter(IPPool.id == pool_id).first()
        if not pool:
            raise ValueError(f"Pool {pool_id} not found")
        
        network = ipaddress.IPv4Network(pool.cidr, strict=False)
        total_ips = int(network.num_addresses)
        
        # Subtract network and broadcast addresses
        usable_ips = total_ips - 2
        
        # Count reserved IPs
        reserved_count = 0
        if pool.reserved_ranges:
            reserved_ranges = json.loads(pool.reserved_ranges)
            for range_def in reserved_ranges:
                start_ip = ipaddress.IPv4Address(range_def["start"])
                end_ip = ipaddress.IPv4Address(range_def["end"])
                reserved_count += int(end_ip) - int(start_ip) + 1
        
        # Count allocated IPs
        allocated_count = self.db.query(IPAllocation).filter(
            IPAllocation.pool_id == pool_id,
            IPAllocation.is_active == True
        ).count()
        
        available_count = usable_ips - reserved_count - allocated_count
        utilization_percent = (allocated_count / max(1, usable_ips - reserved_count)) * 100
        
        return {
            "pool_name": pool.name,
            "cidr": pool.cidr,
            "total_ips": total_ips,
            "usable_ips": usable_ips,
            "reserved_ips": reserved_count,
            "allocated_ips": allocated_count,
            "available_ips": available_count,
            "utilization_percent": round(utilization_percent, 2)
        }
    
    def get_available_ips(self, pool_id: int) -> List[str]:
        """Get all available IP addresses in a pool"""
        pool = self.db.query(IPPool).filter(IPPool.id == pool_id).first()
        if not pool:
            raise ValueError(f"Pool {pool_id} not found")
        
        network = ipaddress.IPv4Network(pool.cidr, strict=False)
        all_ips = [str(ip) for ip in network.hosts()]  # Exclude network and broadcast
        
        # Get reserved IPs
        reserved_ips = set()
        if pool.reserved_ranges:
            reserved_ranges = json.loads(pool.reserved_ranges)
            for range_def in reserved_ranges:
                start_ip = ipaddress.IPv4Address(range_def["start"])
                end_ip = ipaddress.IPv4Address(range_def["end"])
                for i in range(int(start_ip), int(end_ip) + 1):
                    reserved_ips.add(str(ipaddress.IPv4Address(i)))
        
        # Get allocated IPs
        allocated_ips = set()
        allocations = self.db.query(IPAllocation).filter(
            IPAllocation.pool_id == pool_id,
            IPAllocation.is_active == True
        ).all()
        
        for allocation in allocations:
            allocated_ips.add(allocation.ip_address)
        
        # Return available IPs
        unavailable = reserved_ips | allocated_ips
        return [ip for ip in all_ips if ip not in unavailable]
    
    def allocate_next_ip(
        self,
        pool_id: int,
        client_id: Optional[str] = None,
        client_name: Optional[str] = None,
        strategy: str = "first_fit",
        lease_duration: int = 86400  # 24 hours default
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Allocate the next available IP address
        
        Returns: (success, message, ip_address)
        """
        try:
            pool = self.db.query(IPPool).filter(IPPool.id == pool_id).first()
            if not pool:
                return False, f"Pool {pool_id} not found", None
            
            if not pool.is_active:
                return False, f"Pool {pool.name} is inactive", None
            
            # Get available IPs
            available_ips = self.get_available_ips(pool_id)
            if not available_ips:
                return False, "No available IP addresses in pool", None
            
            # Get allocated IPs for strategy
            allocations = self.db.query(IPAllocation).filter(
                IPAllocation.pool_id == pool_id,
                IPAllocation.is_active == True
            ).all()
            allocated_ips = {alloc.ip_address for alloc in allocations}
            
            # Apply allocation strategy
            strategy_class = self.STRATEGIES.get(strategy, FirstFitStrategy)
            allocated_ip = strategy_class.allocate(available_ips, allocated_ips)
            
            if not allocated_ip:
                return False, "Failed to allocate IP using specified strategy", None
            
            # Create allocation record
            allocation = IPAllocation(
                pool_id=pool_id,
                ip_address=allocated_ip,
                client_id=client_id,
                client_name=client_name,
                allocation_type="dynamic",
                allocation_strategy=strategy,
                assigned_at=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                is_active=True
            )
            
            self.db.add(allocation)
            self.db.flush()  # Get the allocation ID
            
            # Create lease
            lease = IPLease(
                pool_id=pool_id,
                allocation_id=allocation.id,
                lease_duration=lease_duration,
                lease_start=datetime.utcnow(),
                lease_end=datetime.utcnow() + timedelta(seconds=lease_duration)
            )
            
            self.db.add(lease)
            
            # Log the allocation
            log_entry = AllocationLog(
                pool_id=pool_id,
                ip_address=allocated_ip,
                action="allocate",
                client_id=client_id,
                details=json.dumps({
                    "strategy": strategy,
                    "lease_duration": lease_duration,
                    "client_name": client_name
                }),
                success=True
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
            return True, f"Successfully allocated {allocated_ip}", allocated_ip
            
        except Exception as e:
            self.db.rollback()
            error_msg = f"Error allocating IP: {str(e)}"
            
            # Log the error
            log_entry = AllocationLog(
                pool_id=pool_id,
                action="allocate",
                client_id=client_id,
                success=False,
                error_message=error_msg
            )
            self.db.add(log_entry)
            self.db.commit()
            
            return False, error_msg, None
    
    def reserve_specific_ip(
        self,
        pool_id: int,
        ip_address: str,
        client_id: Optional[str] = None,
        client_name: Optional[str] = None,
        lease_duration: int = 86400
    ) -> Tuple[bool, str]:
        """
        Reserve a specific IP address
        
        Returns: (success, message)
        """
        try:
            pool = self.db.query(IPPool).filter(IPPool.id == pool_id).first()
            if not pool:
                return False, f"Pool {pool_id} not found"
            
            # Validate IP is in pool range
            network = ipaddress.IPv4Network(pool.cidr, strict=False)
            try:
                target_ip = ipaddress.IPv4Address(ip_address)
                if target_ip not in network:
                    return False, f"IP {ip_address} is not in pool range {pool.cidr}"
            except ipaddress.AddressValueError:
                return False, f"Invalid IP address: {ip_address}"
            
            # Check if IP is available
            available_ips = self.get_available_ips(pool_id)
            if ip_address not in available_ips:
                return False, f"IP {ip_address} is not available (allocated or reserved)"
            
            # Create allocation record
            allocation = IPAllocation(
                pool_id=pool_id,
                ip_address=ip_address,
                client_id=client_id,
                client_name=client_name,
                allocation_type="static",
                allocation_strategy="manual",
                assigned_at=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                is_active=True
            )
            
            self.db.add(allocation)
            self.db.flush()
            
            # Create lease
            lease = IPLease(
                pool_id=pool_id,
                allocation_id=allocation.id,
                lease_duration=lease_duration,
                lease_start=datetime.utcnow(),
                lease_end=datetime.utcnow() + timedelta(seconds=lease_duration)
            )
            
            self.db.add(lease)
            
            # Log the reservation
            log_entry = AllocationLog(
                pool_id=pool_id,
                ip_address=ip_address,
                action="reserve",
                client_id=client_id,
                details=json.dumps({
                    "lease_duration": lease_duration,
                    "client_name": client_name
                }),
                success=True
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
            return True, f"Successfully reserved {ip_address}"
            
        except Exception as e:
            self.db.rollback()
            error_msg = f"Error reserving IP: {str(e)}"
            
            # Log the error
            log_entry = AllocationLog(
                pool_id=pool_id,
                ip_address=ip_address,
                action="reserve",
                client_id=client_id,
                success=False,
                error_message=error_msg
            )
            self.db.add(log_entry)
            self.db.commit()
            
            return False, error_msg
    
    def deallocate_ip(self, allocation_id: int) -> Tuple[bool, str]:
        """
        Deallocate an IP address
        
        Returns: (success, message)
        """
        try:
            allocation = self.db.query(IPAllocation).filter(
                IPAllocation.id == allocation_id
            ).first()
            
            if not allocation:
                return False, f"Allocation {allocation_id} not found"
            
            if not allocation.is_active:
                return False, f"Allocation {allocation_id} is already inactive"
            
            # Deactivate allocation
            allocation.is_active = False
            
            # Expire lease if exists
            if allocation.lease:
                allocation.lease.is_expired = True
            
            # Log the deallocation
            log_entry = AllocationLog(
                pool_id=allocation.pool_id,
                ip_address=allocation.ip_address,
                action="deallocate",
                client_id=allocation.client_id,
                success=True
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
            return True, f"Successfully deallocated {allocation.ip_address}"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error deallocating IP: {str(e)}"
    
    def renew_lease(self, lease_id: int, extension_seconds: int = 86400) -> Tuple[bool, str]:
        """
        Renew an IP lease
        
        Returns: (success, message)
        """
        try:
            lease = self.db.query(IPLease).filter(IPLease.id == lease_id).first()
            if not lease:
                return False, f"Lease {lease_id} not found"
            
            if lease.renewal_count >= lease.max_renewals:
                return False, f"Maximum renewals ({lease.max_renewals}) reached"
            
            # Extend lease
            lease.lease_end = datetime.utcnow() + timedelta(seconds=extension_seconds)
            lease.renewal_count += 1
            lease.is_expired = False
            
            # Update allocation last seen
            if lease.allocation:
                lease.allocation.last_seen = datetime.utcnow()
            
            self.db.commit()
            
            return True, f"Lease renewed until {lease.lease_end}"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error renewing lease: {str(e)}"
    
    def cleanup_expired_leases(self) -> int:
        """
        Clean up expired leases and deallocate their IPs
        
        Returns: Number of leases cleaned up
        """
        try:
            # Find expired leases
            expired_leases = self.db.query(IPLease).filter(
                IPLease.lease_end < datetime.utcnow(),
                IPLease.is_expired == False
            ).all()
            
            cleaned_count = 0
            for lease in expired_leases:
                # Mark lease as expired
                lease.is_expired = True
                
                # Deactivate allocation
                if lease.allocation and lease.allocation.is_active:
                    lease.allocation.is_active = False
                    
                    # Log the expiration
                    log_entry = AllocationLog(
                        pool_id=lease.pool_id,
                        ip_address=lease.allocation.ip_address,
                        action="expire",
                        client_id=lease.allocation.client_id,
                        details=json.dumps({"lease_id": lease.id}),
                        success=True
                    )
                    self.db.add(log_entry)
                    
                    cleaned_count += 1
            
            self.db.commit()
            return cleaned_count
            
        except Exception as e:
            self.db.rollback()
            raise e 