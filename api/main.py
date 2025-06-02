from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta
import logging

from database import get_db, IPPool, IPAllocation, IPLease, AllocationLog
from core.ip_allocator import IPAllocator
from network.interface_manager import NetworkInterfaceManager
from .schemas import (
    IPPoolCreate, IPPoolUpdate, IPPoolResponse, IPPoolUtilization,
    IPAllocationCreate, IPReservationCreate, IPAllocationResponse, IPAllocationResult,
    IPLeaseResponse, LeaseRenewalRequest,
    NetworkInterfaceResponse, IPBindingRequest, IPBindingResult,
    ConnectivityTestRequest, ConnectivityTestResult,
    OperationResult, SystemStats, ErrorResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BlackzAllocator API",
    description="Professional IP Pool Management and Allocation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global network interface manager
network_manager = NetworkInterfaceManager()

# Background task for lease cleanup
def cleanup_expired_leases_task():
    """Background task to clean up expired leases"""
    try:
        from database import get_db_session
        db = get_db_session()
        allocator = IPAllocator(db)
        cleaned_count = allocator.cleanup_expired_leases()
        logger.info(f"Cleaned up {cleaned_count} expired leases")
        db.close()
    except Exception as e:
        logger.error(f"Error cleaning up expired leases: {e}")

# IP Pool Management Endpoints
@app.post("/pools/", response_model=IPPoolResponse, status_code=status.HTTP_201_CREATED)
async def create_ip_pool(pool_data: IPPoolCreate, db: Session = Depends(get_db)):
    """Create a new IP pool"""
    try:
        # Check if pool name already exists
        existing_pool = db.query(IPPool).filter(IPPool.name == pool_data.name).first()
        if existing_pool:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pool with name '{pool_data.name}' already exists"
            )
        
        # Create new pool
        pool = IPPool(
            name=pool_data.name,
            cidr=pool_data.cidr,
            description=pool_data.description,
            gateway=pool_data.gateway,
            dns_servers=json.dumps(pool_data.dns_servers) if pool_data.dns_servers else None,
            reserved_ranges=json.dumps(pool_data.reserved_ranges) if pool_data.reserved_ranges else None
        )
        
        db.add(pool)
        db.commit()
        db.refresh(pool)
        
        logger.info(f"Created IP pool: {pool.name} ({pool.cidr})")
        return pool
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating IP pool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/pools/", response_model=List[IPPoolResponse])
async def list_ip_pools(
    active_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all IP pools"""
    query = db.query(IPPool)
    if active_only:
        query = query.filter(IPPool.is_active == True)
    
    pools = query.offset(skip).limit(limit).all()
    return pools

@app.get("/pools/{pool_id}", response_model=IPPoolResponse)
async def get_ip_pool(pool_id: int, db: Session = Depends(get_db)):
    """Get a specific IP pool"""
    pool = db.query(IPPool).filter(IPPool.id == pool_id).first()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pool {pool_id} not found"
        )
    return pool

@app.put("/pools/{pool_id}", response_model=IPPoolResponse)
async def update_ip_pool(
    pool_id: int,
    pool_update: IPPoolUpdate,
    db: Session = Depends(get_db)
):
    """Update an IP pool"""
    pool = db.query(IPPool).filter(IPPool.id == pool_id).first()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pool {pool_id} not found"
        )
    
    try:
        update_data = pool_update.dict(exclude_unset=True)
        
        # Handle JSON fields
        if 'dns_servers' in update_data and update_data['dns_servers'] is not None:
            update_data['dns_servers'] = json.dumps(update_data['dns_servers'])
        if 'reserved_ranges' in update_data and update_data['reserved_ranges'] is not None:
            update_data['reserved_ranges'] = json.dumps(update_data['reserved_ranges'])
        
        for field, value in update_data.items():
            setattr(pool, field, value)
        
        pool.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(pool)
        
        logger.info(f"Updated IP pool: {pool.name}")
        return pool
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating IP pool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.delete("/pools/{pool_id}", response_model=OperationResult)
async def delete_ip_pool(pool_id: int, db: Session = Depends(get_db)):
    """Delete an IP pool"""
    pool = db.query(IPPool).filter(IPPool.id == pool_id).first()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pool {pool_id} not found"
        )
    
    try:
        # Check if pool has active allocations
        active_allocations = db.query(IPAllocation).filter(
            IPAllocation.pool_id == pool_id,
            IPAllocation.is_active == True
        ).count()
        
        if active_allocations > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete pool with {active_allocations} active allocations"
            )
        
        db.delete(pool)
        db.commit()
        
        logger.info(f"Deleted IP pool: {pool.name}")
        return OperationResult(success=True, message=f"Pool '{pool.name}' deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting IP pool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/pools/{pool_id}/utilization", response_model=IPPoolUtilization)
async def get_pool_utilization(pool_id: int, db: Session = Depends(get_db)):
    """Get IP pool utilization statistics"""
    try:
        allocator = IPAllocator(db)
        utilization = allocator.get_pool_utilization(pool_id)
        return IPPoolUtilization(**utilization)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting pool utilization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# IP Allocation Endpoints
@app.post("/allocations/", response_model=IPAllocationResult, status_code=status.HTTP_201_CREATED)
async def allocate_ip(allocation_data: IPAllocationCreate, db: Session = Depends(get_db)):
    """Allocate the next available IP address"""
    try:
        allocator = IPAllocator(db)
        success, message, ip_address = allocator.allocate_next_ip(
            pool_id=allocation_data.pool_id,
            client_id=allocation_data.client_id,
            client_name=allocation_data.client_name,
            strategy=allocation_data.allocation_strategy,
            lease_duration=allocation_data.lease_duration
        )
        
        allocation_id = None
        if success and ip_address:
            # Get the allocation ID
            allocation = db.query(IPAllocation).filter(
                IPAllocation.ip_address == ip_address,
                IPAllocation.pool_id == allocation_data.pool_id,
                IPAllocation.is_active == True
            ).first()
            if allocation:
                allocation_id = allocation.id
                
                # Bind to network interface if specified
                if allocation_data.network_interface:
                    bind_success, bind_message = network_manager.bind_ip_to_interface(
                        allocation_data.network_interface,
                        ip_address
                    )
                    if bind_success:
                        allocation.network_interface = allocation_data.network_interface
                        allocation.binding_status = "bound"
                        db.commit()
                        message += f" and bound to {allocation_data.network_interface}"
                    else:
                        allocation.binding_status = "failed"
                        db.commit()
                        message += f" but binding failed: {bind_message}"
        
        return IPAllocationResult(
            success=success,
            message=message,
            ip_address=ip_address,
            allocation_id=allocation_id
        )
        
    except Exception as e:
        logger.error(f"Error allocating IP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/reservations/", response_model=OperationResult, status_code=status.HTTP_201_CREATED)
async def reserve_specific_ip(reservation_data: IPReservationCreate, db: Session = Depends(get_db)):
    """Reserve a specific IP address"""
    try:
        allocator = IPAllocator(db)
        success, message = allocator.reserve_specific_ip(
            pool_id=reservation_data.pool_id,
            ip_address=reservation_data.ip_address,
            client_id=reservation_data.client_id,
            client_name=reservation_data.client_name,
            lease_duration=reservation_data.lease_duration
        )
        
        if success and reservation_data.network_interface:
            # Bind to network interface if specified
            bind_success, bind_message = network_manager.bind_ip_to_interface(
                reservation_data.network_interface,
                reservation_data.ip_address
            )
            if bind_success:
                # Update allocation record
                allocation = db.query(IPAllocation).filter(
                    IPAllocation.ip_address == reservation_data.ip_address,
                    IPAllocation.pool_id == reservation_data.pool_id,
                    IPAllocation.is_active == True
                ).first()
                if allocation:
                    allocation.network_interface = reservation_data.network_interface
                    allocation.binding_status = "bound"
                    db.commit()
                    message += f" and bound to {reservation_data.network_interface}"
            else:
                message += f" but binding failed: {bind_message}"
        
        return OperationResult(success=success, message=message)
        
    except Exception as e:
        logger.error(f"Error reserving IP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/allocations/", response_model=List[IPAllocationResponse])
async def list_allocations(
    pool_id: Optional[int] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List IP allocations"""
    query = db.query(IPAllocation)
    
    if pool_id:
        query = query.filter(IPAllocation.pool_id == pool_id)
    if active_only:
        query = query.filter(IPAllocation.is_active == True)
    
    allocations = query.offset(skip).limit(limit).all()
    return allocations

@app.delete("/allocations/{allocation_id}", response_model=OperationResult)
async def deallocate_ip(allocation_id: int, db: Session = Depends(get_db)):
    """Deallocate an IP address"""
    try:
        allocator = IPAllocator(db)
        
        # Get allocation details for network unbinding
        allocation = db.query(IPAllocation).filter(IPAllocation.id == allocation_id).first()
        if allocation and allocation.network_interface and allocation.binding_status == "bound":
            # Unbind from network interface
            unbind_success, unbind_message = network_manager.unbind_ip_from_interface(
                allocation.network_interface,
                allocation.ip_address
            )
            if unbind_success:
                allocation.binding_status = "unbound"
                db.commit()
        
        success, message = allocator.deallocate_ip(allocation_id)
        return OperationResult(success=success, message=message)
        
    except Exception as e:
        logger.error(f"Error deallocating IP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Lease Management Endpoints
@app.get("/leases/", response_model=List[IPLeaseResponse])
async def list_leases(
    pool_id: Optional[int] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List IP leases"""
    query = db.query(IPLease)
    
    if pool_id:
        query = query.filter(IPLease.pool_id == pool_id)
    if active_only:
        query = query.filter(IPLease.is_expired == False)
    
    leases = query.offset(skip).limit(limit).all()
    
    # Add time remaining to each lease
    result = []
    for lease in leases:
        lease_dict = IPLeaseResponse.from_orm(lease).dict()
        if not lease.is_expired:
            time_remaining = lease.lease_end - datetime.utcnow()
            lease_dict['time_remaining_seconds'] = max(0, int(time_remaining.total_seconds()))
        result.append(IPLeaseResponse(**lease_dict))
    
    return result

@app.post("/leases/renew", response_model=OperationResult)
async def renew_lease(renewal_data: LeaseRenewalRequest, db: Session = Depends(get_db)):
    """Renew an IP lease"""
    try:
        allocator = IPAllocator(db)
        success, message = allocator.renew_lease(
            renewal_data.lease_id,
            renewal_data.extension_seconds
        )
        return OperationResult(success=success, message=message)
        
    except Exception as e:
        logger.error(f"Error renewing lease: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/leases/cleanup", response_model=OperationResult)
async def cleanup_expired_leases(background_tasks: BackgroundTasks):
    """Clean up expired leases (can be run manually or as background task)"""
    background_tasks.add_task(cleanup_expired_leases_task)
    return OperationResult(
        success=True,
        message="Expired lease cleanup task scheduled"
    )

# Network Interface Management Endpoints
@app.get("/interfaces/", response_model=List[NetworkInterfaceResponse])
async def list_network_interfaces():
    """List available network interfaces"""
    try:
        interfaces = network_manager.get_network_interfaces()
        return [
            NetworkInterfaceResponse(
                name=iface.name,
                display_name=iface.display_name,
                description=iface.description,
                mac_address=iface.mac_address,
                current_ips=iface.current_ips,
                is_active=iface.is_active,
                is_virtual=iface.is_virtual,
                supports_binding=iface.supports_binding
            )
            for iface in interfaces
        ]
    except Exception as e:
        logger.error(f"Error listing network interfaces: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/interfaces/bind", response_model=IPBindingResult)
async def bind_ip_to_interface(binding_data: IPBindingRequest):
    """Bind an IP address to a network interface"""
    try:
        success, message = network_manager.bind_ip_to_interface(
            binding_data.interface_name,
            binding_data.ip_address,
            binding_data.subnet_mask,
            binding_data.persistent
        )
        return IPBindingResult(success=success, message=message)
        
    except Exception as e:
        logger.error(f"Error binding IP to interface: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/interfaces/unbind", response_model=IPBindingResult)
async def unbind_ip_from_interface(
    interface_name: str,
    ip_address: str
):
    """Unbind an IP address from a network interface"""
    try:
        success, message = network_manager.unbind_ip_from_interface(
            interface_name,
            ip_address
        )
        return IPBindingResult(success=success, message=message)
        
    except Exception as e:
        logger.error(f"Error unbinding IP from interface: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Connectivity Testing Endpoints
@app.post("/connectivity/test", response_model=ConnectivityTestResult)
async def test_connectivity(test_data: ConnectivityTestRequest):
    """Test network connectivity to a target IP"""
    try:
        result = network_manager.test_connectivity(
            test_data.target_ip,
            test_data.source_interface
        )
        return ConnectivityTestResult(**result)
        
    except Exception as e:
        logger.error(f"Error testing connectivity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/connectivity/ping/{ip_address}")
async def ping_ip(ip_address: str):
    """Simple ping test"""
    try:
        success = network_manager.ping_ip(ip_address)
        return {
            "ip_address": ip_address,
            "ping_success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error pinging IP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# System Statistics and Monitoring
@app.get("/stats/system", response_model=SystemStats)
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        # Get database statistics
        total_pools = db.query(IPPool).count()
        active_pools = db.query(IPPool).filter(IPPool.is_active == True).count()
        total_allocations = db.query(IPAllocation).count()
        active_allocations = db.query(IPAllocation).filter(IPAllocation.is_active == True).count()
        total_leases = db.query(IPLease).count()
        active_leases = db.query(IPLease).filter(IPLease.is_expired == False).count()
        expired_leases = db.query(IPLease).filter(IPLease.is_expired == True).count()
        
        # Get interface statistics
        interfaces = network_manager.get_network_interfaces()
        system_interfaces = len(interfaces)
        active_interfaces = len([iface for iface in interfaces if iface.is_active])
        
        return SystemStats(
            total_pools=total_pools,
            active_pools=active_pools,
            total_allocations=total_allocations,
            active_allocations=active_allocations,
            total_leases=total_leases,
            active_leases=active_leases,
            expired_leases=expired_leases,
            system_interfaces=system_interfaces,
            active_interfaces=active_interfaces
        )
        
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "BlackzAllocator API"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "BlackzAllocator API",
        "version": "1.0.0",
        "description": "Professional IP Pool Management and Allocation System",
        "docs_url": "/docs",
        "health_url": "/health"
    } 