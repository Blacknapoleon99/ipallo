from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import ipaddress

# IP Pool Schemas
class IPPoolCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Pool name")
    cidr: str = Field(..., description="CIDR notation (e.g., 192.168.1.0/24)")
    description: Optional[str] = Field(None, max_length=1000, description="Pool description")
    gateway: Optional[str] = Field(None, description="Gateway IP address")
    dns_servers: Optional[List[str]] = Field(default_factory=list, description="DNS server IPs")
    reserved_ranges: Optional[List[Dict[str, str]]] = Field(
        default_factory=list, 
        description="Reserved IP ranges [{'start': '192.168.1.1', 'end': '192.168.1.10'}]"
    )
    
    @validator('cidr')
    def validate_cidr(cls, v):
        try:
            ipaddress.IPv4Network(v, strict=False)
            return v
        except ipaddress.AddressValueError:
            raise ValueError('Invalid CIDR notation')
    
    @validator('gateway')
    def validate_gateway(cls, v):
        if v:
            try:
                ipaddress.IPv4Address(v)
                return v
            except ipaddress.AddressValueError:
                raise ValueError('Invalid gateway IP address')
        return v
    
    @validator('dns_servers')
    def validate_dns_servers(cls, v):
        if v:
            for dns in v:
                try:
                    ipaddress.IPv4Address(dns)
                except ipaddress.AddressValueError:
                    raise ValueError(f'Invalid DNS server IP: {dns}')
        return v
    
    @validator('reserved_ranges')
    def validate_reserved_ranges(cls, v):
        if v:
            for range_def in v:
                if 'start' not in range_def or 'end' not in range_def:
                    raise ValueError('Reserved range must have start and end fields')
                try:
                    start_ip = ipaddress.IPv4Address(range_def['start'])
                    end_ip = ipaddress.IPv4Address(range_def['end'])
                    if start_ip > end_ip:
                        raise ValueError('Start IP must be less than or equal to end IP')
                except ipaddress.AddressValueError:
                    raise ValueError('Invalid IP address in reserved range')
        return v

class IPPoolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    gateway: Optional[str] = None
    dns_servers: Optional[List[str]] = None
    reserved_ranges: Optional[List[Dict[str, str]]] = None
    is_active: Optional[bool] = None
    
    @validator('gateway')
    def validate_gateway(cls, v):
        if v:
            try:
                ipaddress.IPv4Address(v)
                return v
            except ipaddress.AddressValueError:
                raise ValueError('Invalid gateway IP address')
        return v

class IPPoolResponse(BaseModel):
    id: int
    name: str
    cidr: str
    description: Optional[str]
    gateway: Optional[str]
    dns_servers: Optional[str]  # JSON string
    reserved_ranges: Optional[str]  # JSON string
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class IPPoolUtilization(BaseModel):
    pool_name: str
    cidr: str
    total_ips: int
    usable_ips: int
    reserved_ips: int
    allocated_ips: int
    available_ips: int
    utilization_percent: float

# IP Allocation Schemas
class IPAllocationCreate(BaseModel):
    pool_id: int = Field(..., description="Pool ID to allocate from")
    client_id: Optional[str] = Field(None, max_length=255, description="Client identifier (MAC, hostname, etc.)")
    client_name: Optional[str] = Field(None, max_length=255, description="Client display name")
    allocation_strategy: str = Field(default="first_fit", description="Allocation strategy")
    lease_duration: int = Field(default=86400, gt=0, description="Lease duration in seconds")
    network_interface: Optional[str] = Field(None, description="Network interface for binding")
    
    @validator('allocation_strategy')
    def validate_strategy(cls, v):
        valid_strategies = ['first_fit', 'random', 'sequential', 'load_balanced']
        if v not in valid_strategies:
            raise ValueError(f'Invalid strategy. Must be one of: {valid_strategies}')
        return v

class IPReservationCreate(BaseModel):
    pool_id: int = Field(..., description="Pool ID to reserve from")
    ip_address: str = Field(..., description="Specific IP address to reserve")
    client_id: Optional[str] = Field(None, max_length=255)
    client_name: Optional[str] = Field(None, max_length=255)
    lease_duration: int = Field(default=86400, gt=0)
    network_interface: Optional[str] = None
    
    @validator('ip_address')
    def validate_ip_address(cls, v):
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise ValueError('Invalid IP address')

class IPAllocationResponse(BaseModel):
    id: int
    pool_id: int
    ip_address: str
    client_id: Optional[str]
    client_name: Optional[str]
    allocation_type: str
    allocation_strategy: str
    assigned_at: datetime
    last_seen: datetime
    is_active: bool
    network_interface: Optional[str]
    binding_status: str
    
    class Config:
        from_attributes = True

class IPAllocationResult(BaseModel):
    success: bool
    message: str
    ip_address: Optional[str] = None
    allocation_id: Optional[int] = None

# IP Lease Schemas
class IPLeaseResponse(BaseModel):
    id: int
    pool_id: int
    allocation_id: int
    lease_start: datetime
    lease_duration: int
    lease_end: datetime
    renewal_count: int
    max_renewals: int
    is_expired: bool
    auto_renew: bool
    time_remaining_seconds: Optional[int] = None
    
    class Config:
        from_attributes = True

class LeaseRenewalRequest(BaseModel):
    lease_id: int
    extension_seconds: int = Field(default=86400, gt=0, description="Extension time in seconds")

# Network Interface Schemas
class NetworkInterfaceResponse(BaseModel):
    name: str
    display_name: str
    description: str
    mac_address: str
    current_ips: List[str]
    is_active: bool
    is_virtual: bool
    supports_binding: bool

class IPBindingRequest(BaseModel):
    interface_name: str = Field(..., description="Network interface name")
    ip_address: str = Field(..., description="IP address to bind")
    subnet_mask: str = Field(default="255.255.255.0", description="Subnet mask")
    persistent: bool = Field(default=False, description="Whether to make binding persistent")
    
    @validator('ip_address')
    def validate_ip_address(cls, v):
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise ValueError('Invalid IP address')
    
    @validator('subnet_mask')
    def validate_subnet_mask(cls, v):
        try:
            # Basic validation - could be more sophisticated
            parts = v.split('.')
            if len(parts) != 4:
                raise ValueError('Invalid subnet mask format')
            for part in parts:
                num = int(part)
                if not 0 <= num <= 255:
                    raise ValueError('Invalid subnet mask values')
            return v
        except (ValueError, TypeError):
            raise ValueError('Invalid subnet mask')

class IPBindingResult(BaseModel):
    success: bool
    message: str

# Connectivity Test Schemas
class ConnectivityTestRequest(BaseModel):
    target_ip: str = Field(..., description="Target IP to test connectivity")
    source_interface: Optional[str] = Field(None, description="Source interface for test")
    
    @validator('target_ip')
    def validate_target_ip(cls, v):
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise ValueError('Invalid target IP address')

class ConnectivityTestResult(BaseModel):
    target_ip: str
    ping_success: bool
    ping_time_ms: Optional[float]
    traceroute_hops: List[str]
    source_interface: Optional[str]
    timestamp: str
    error: Optional[str] = None

# General Response Schemas
class OperationResult(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Statistics and Monitoring Schemas
class SystemStats(BaseModel):
    total_pools: int
    active_pools: int
    total_allocations: int
    active_allocations: int
    total_leases: int
    active_leases: int
    expired_leases: int
    system_interfaces: int
    active_interfaces: int

class AllocationStats(BaseModel):
    pool_id: int
    pool_name: str
    total_allocations: int
    active_allocations: int
    allocation_rate_24h: int
    most_common_strategy: str
    average_lease_duration: float

# Pagination Schemas
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=50, ge=1, le=1000, description="Items per page")
    
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool 