from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from typing import Optional

Base = declarative_base()

class IPPool(Base):
    """IP Pool model for managing network ranges"""
    __tablename__ = "ip_pools"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), unique=True, index=True, nullable=False)
    cidr: str = Column(String(18), nullable=False)  # e.g., "192.168.1.0/24"
    description: str = Column(Text, nullable=True)
    gateway: str = Column(String(15), nullable=True)  # Reserved gateway IP
    dns_servers: str = Column(Text, nullable=True)  # JSON array of DNS servers
    reserved_ranges: str = Column(Text, nullable=True)  # JSON array of reserved ranges
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True)
    
    # Relationships
    allocations = relationship("IPAllocation", back_populates="pool", cascade="all, delete-orphan")
    leases = relationship("IPLease", back_populates="pool", cascade="all, delete-orphan")

class IPAllocation(Base):
    """IP Allocation model for tracking assigned IPs"""
    __tablename__ = "ip_allocations"
    
    id: int = Column(Integer, primary_key=True, index=True)
    pool_id: int = Column(Integer, ForeignKey("ip_pools.id"), nullable=False)
    ip_address: str = Column(String(15), nullable=False, index=True)
    client_id: str = Column(String(255), nullable=True)  # MAC address, hostname, etc.
    client_name: str = Column(String(255), nullable=True)
    allocation_type: str = Column(String(20), default="dynamic")  # dynamic, static, reserved
    allocation_strategy: str = Column(String(20), default="first_fit")  # first_fit, random, sequential
    assigned_at: datetime = Column(DateTime, default=datetime.utcnow)
    last_seen: datetime = Column(DateTime, default=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True)
    network_interface: str = Column(String(255), nullable=True)
    binding_status: str = Column(String(20), default="unbound")  # unbound, bound, failed
    
    # Relationships
    pool = relationship("IPPool", back_populates="allocations")
    lease = relationship("IPLease", back_populates="allocation", uselist=False)

class IPLease(Base):
    """IP Lease model for time-based allocations"""
    __tablename__ = "ip_leases"
    
    id: int = Column(Integer, primary_key=True, index=True)
    pool_id: int = Column(Integer, ForeignKey("ip_pools.id"), nullable=False)
    allocation_id: int = Column(Integer, ForeignKey("ip_allocations.id"), nullable=False)
    lease_start: datetime = Column(DateTime, default=datetime.utcnow)
    lease_duration: int = Column(Integer, default=86400)  # Duration in seconds (default 24 hours)
    lease_end: datetime = Column(DateTime)
    renewal_count: int = Column(Integer, default=0)
    max_renewals: int = Column(Integer, default=3)
    is_expired: bool = Column(Boolean, default=False)
    auto_renew: bool = Column(Boolean, default=True)
    
    # Relationships
    pool = relationship("IPPool", back_populates="leases")
    allocation = relationship("IPAllocation", back_populates="lease")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.lease_end:
            self.lease_end = self.lease_start + timedelta(seconds=self.lease_duration)
    
    @property
    def is_lease_expired(self) -> bool:
        """Check if lease has expired"""
        return datetime.utcnow() > self.lease_end
    
    @property
    def time_remaining(self) -> timedelta:
        """Get remaining lease time"""
        return max(timedelta(0), self.lease_end - datetime.utcnow())

class NetworkInterface(Base):
    """Network Interface model for binding management"""
    __tablename__ = "network_interfaces"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False, unique=True)
    display_name: str = Column(String(255), nullable=True)
    description: str = Column(Text, nullable=True)
    mac_address: str = Column(String(17), nullable=True)  # XX:XX:XX:XX:XX:XX
    current_ip: str = Column(String(15), nullable=True)
    is_active: bool = Column(Boolean, default=True)
    is_virtual: bool = Column(Boolean, default=False)
    supports_binding: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AllocationLog(Base):
    """Allocation Log model for audit trail"""
    __tablename__ = "allocation_logs"
    
    id: int = Column(Integer, primary_key=True, index=True)
    pool_id: int = Column(Integer, ForeignKey("ip_pools.id"), nullable=True)
    ip_address: str = Column(String(15), nullable=True)
    action: str = Column(String(50), nullable=False)  # allocate, deallocate, bind, unbind, etc.
    client_id: str = Column(String(255), nullable=True)
    details: str = Column(Text, nullable=True)  # JSON details
    success: bool = Column(Boolean, default=True)
    error_message: str = Column(Text, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    user_agent: str = Column(String(255), nullable=True)
    source_ip: str = Column(String(15), nullable=True) 