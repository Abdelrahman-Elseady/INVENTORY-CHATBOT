# database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, DECIMAL, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create base class for all database models
Base = declarative_base()

# ========== TABLE DEFINITIONS ==========

class Customer(Base):
    """Customers table - stores customer information"""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200))
    phone = Column(String(50))
    address = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f"<Customer {self.code}: {self.name}>"

class Vendor(Base):
    """Vendors table - stores supplier information"""
    __tablename__ = 'vendors'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200))
    phone = Column(String(50))
    address = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    assets = relationship("Asset", back_populates="vendor")
    bills = relationship("Bill", back_populates="vendor")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
    
    def __repr__(self):
        return f"<Vendor {self.code}: {self.name}>"

class Site(Base):
    """Sites table - stores location sites (warehouses, stores, etc.)"""
    __tablename__ = 'sites'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    timezone = Column(String(100))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    locations = relationship("Location", back_populates="site", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="site")
    purchase_orders = relationship("PurchaseOrder", back_populates="site")
    sales_orders = relationship("SalesOrder", back_populates="site")
    
    def __repr__(self):
        return f"<Site {self.code}: {self.name}>"

class Location(Base):
    """Locations table - specific locations within a site (aisles, bins, etc.)"""
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey('locations.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    site = relationship("Site", back_populates="locations")
    parent = relationship("Location", remote_side=[id], backref="children")
    assets = relationship("Asset", back_populates="location")
    
    __table_args__ = (
        # Ensure location codes are unique within a site
        UniqueConstraint('site_id', 'code', name='uix_site_location'),
    )
    
    def __repr__(self):
        return f"<Location {self.code}: {self.name}>"

class Item(Base):
    """Items table - products/inventory items"""
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    unit = Column(String(50))  # Unit of measure (pcs, kg, etc.)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    purchase_order_lines = relationship("PurchaseOrderLine", back_populates="item")
    sales_order_lines = relationship("SalesOrderLine", back_populates="item")
    
    def __repr__(self):
        return f"<Item {self.code}: {self.name}>"

class Asset(Base):
    """Assets table - company assets (equipment, vehicles, etc.)"""
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    tag = Column(String(100), unique=True, nullable=False)  # Asset tag number
    name = Column(String(200), nullable=False)
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'))
    serial = Column(String(200))
    category = Column(String(100))
    status = Column(String(30), nullable=False, default='Active')
    cost = Column(DECIMAL(18, 2))
    purchase_date = Column(Date)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    site = relationship("Site", back_populates="assets")
    location = relationship("Location", back_populates="assets")
    vendor = relationship("Vendor", back_populates="assets")
    transactions = relationship("AssetTransaction", back_populates="asset")
    
    def __repr__(self):
        return f"<Asset {self.tag}: {self.name}>"

class Bill(Base):
    """Bills table - vendor bills/invoices"""
    __tablename__ = 'bills'
    
    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    bill_number = Column(String(100), nullable=False)
    bill_date = Column(Date, nullable=False)
    due_date = Column(Date)
    total_amount = Column(DECIMAL(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default='USD')
    status = Column(String(30), nullable=False, default='Open')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="bills")
    
    __table_args__ = (
        # Ensure bill numbers are unique per vendor
        UniqueConstraint('vendor_id', 'bill_number', name='uix_vendor_bill'),
    )
    
    def __repr__(self):
        return f"<Bill {self.bill_number}: {self.total_amount}>"

class PurchaseOrder(Base):
    """Purchase Orders table"""
    __tablename__ = 'purchase_orders'
    
    id = Column(Integer, primary_key=True)
    po_number = Column(String(100), unique=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    po_date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default='Open')
    site_id = Column(Integer, ForeignKey('sites.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="purchase_orders")
    site = relationship("Site", back_populates="purchase_orders")
    lines = relationship("PurchaseOrderLine", back_populates="purchase_order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PO {self.po_number}: {self.status}>"

class PurchaseOrderLine(Base):
    """Purchase Order Lines table"""
    __tablename__ = 'purchase_order_lines'
    
    id = Column(Integer, primary_key=True)
    po_id = Column(Integer, ForeignKey('purchase_orders.id'), nullable=False)
    line_number = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'))
    item_code = Column(String(100), nullable=False)
    description = Column(String(200))
    quantity = Column(DECIMAL(18, 4), nullable=False)
    unit_price = Column(DECIMAL(18, 4), nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="lines")
    item = relationship("Item", back_populates="purchase_order_lines")
    
    __table_args__ = (
        UniqueConstraint('po_id', 'line_number', name='uix_po_line'),
    )
    
    def __repr__(self):
        return f"<POLine {self.line_number}: {self.quantity} x {self.unit_price}>"

class SalesOrder(Base):
    """Sales Orders table"""
    __tablename__ = 'sales_orders'
    
    id = Column(Integer, primary_key=True)
    so_number = Column(String(100), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    so_date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default='Open')
    site_id = Column(Integer, ForeignKey('sites.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer")
    site = relationship("Site", back_populates="sales_orders")
    lines = relationship("SalesOrderLine", back_populates="sales_order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SO {self.so_number}: {self.status}>"

class SalesOrderLine(Base):
    """Sales Order Lines table"""
    __tablename__ = 'sales_order_lines'
    
    id = Column(Integer, primary_key=True)
    so_id = Column(Integer, ForeignKey('sales_orders.id'), nullable=False)
    line_number = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'))
    item_code = Column(String(100), nullable=False)
    description = Column(String(200))
    quantity = Column(DECIMAL(18, 4), nullable=False)
    unit_price = Column(DECIMAL(18, 4), nullable=False)
    
    # Relationships
    sales_order = relationship("SalesOrder", back_populates="lines")
    item = relationship("Item", back_populates="sales_order_lines")
    
    __table_args__ = (
        UniqueConstraint('so_id', 'line_number', name='uix_so_line'),
    )
    
    def __repr__(self):
        return f"<SOLine {self.line_number}: {self.quantity} x {self.unit_price}>"

class AssetTransaction(Base):
    """Asset Transactions table - tracks movement of assets"""
    __tablename__ = 'asset_transactions'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    from_location_id = Column(Integer, ForeignKey('locations.id'))
    to_location_id = Column(Integer, ForeignKey('locations.id'))
    transaction_type = Column(String(30), nullable=False)  # Move, Transfer, Dispose, etc.
    quantity = Column(Integer, nullable=False, default=1)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    note = Column(String(500))
    
    # Relationships
    asset = relationship("Asset", back_populates="transactions")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
    
    def __repr__(self):
        return f"<AssetTxn {self.transaction_type}: Asset {self.asset_id}>"

# Add missing imports at the top
from sqlalchemy import UniqueConstraint

# ========== DATABASE CONNECTION AND SETUP ==========

class DatabaseManager:
    """
    Manages database connection and provides session handling
    """
    
    def __init__(self, db_url=None):
        """
        Initialize database manager
        If db_url is None, uses SQLite file in current directory
        """
        if db_url is None:
            # Use SQLite database file
            self.db_url = "sqlite:///inventory.db"
        else:
            self.db_url = db_url
        
        # Create engine
        self.engine = create_engine(
            self.db_url,
            echo=False,  # Set to True to see SQL queries
            connect_args={"check_same_thread": False}  # Needed for SQLite
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info(f"Database manager initialized with {self.db_url}")
    
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)
        logger.warning("All database tables dropped")
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def init_db(self):
        """Initialize database with sample data for testing"""
        session = self.get_session()
        
        try:
            # Check if we already have data
            if session.query(Customer).first():
                logger.info("Database already has data, skipping initialization")
                return
            
            # Add sample customers
            customers = [
                Customer(code="C001", name="Acme Corporation", email="info@acme.com", city="New York", country="USA"),
                Customer(code="C002", name="TechStart Inc", email="contact@techstart.com", city="San Francisco", country="USA"),
                Customer(code="C003", name="Global Traders", email="sales@globaltraders.com", city="London", country="UK"),
            ]
            session.add_all(customers)
            
            # Add sample vendors
            vendors = [
                Vendor(code="V001", name="SupplyCo", email="orders@supplyco.com", city="Chicago", country="USA"),
                Vendor(code="V002", name="TechParts Ltd", email="sales@techparts.com", city="Boston", country="USA"),
                Vendor(code="V003", name="Global Shipping", email="info@globalshipping.com", city="Miami", country="USA"),
            ]
            session.add_all(vendors)
            
            # Add sample sites
            sites = [
                Site(code="S001", name="Main Warehouse", city="New York", country="USA"),
                Site(code="S002", name="West Coast Facility", city="Los Angeles", country="USA"),
                Site(code="S003", name="European Hub", city="Amsterdam", country="Netherlands"),
            ]
            session.add_all(sites)
            session.flush()  # To get IDs
            
            # Add locations for each site
            locations = [
                Location(site_id=sites[0].id, code="A1", name="Aisle 1, Bay 1"),
                Location(site_id=sites[0].id, code="A2", name="Aisle 1, Bay 2"),
                Location(site_id=sites[1].id, code="B1", name="Storage Room B1"),
                Location(site_id=sites[1].id, code="B2", name="Storage Room B2"),
                Location(site_id=sites[2].id, code="EU-01", name="European Storage 1"),
            ]
            session.add_all(locations)
            
            # Add sample items
            items = [
                Item(code="ITM001", name="Laptop Computer", category="Electronics", unit="pcs"),
                Item(code="ITM002", name="Office Chair", category="Furniture", unit="pcs"),
                Item(code="ITM003", name="Printer Paper", category="Supplies", unit="box"),
                Item(code="ITM004", name="USB Cable", category="Electronics", unit="pcs"),
            ]
            session.add_all(items)
            
            # Add sample assets
            assets = [
                Asset(tag="AST001", name="Forklift A", site_id=sites[0].id, location_id=locations[0].id, 
                      serial="FL12345", category="Equipment", status="Active", cost=25000, purchase_date=datetime(2023,1,15).date()),
                Asset(tag="AST002", name="Server Rack", site_id=sites[1].id, location_id=locations[2].id,
                      serial="SR78901", category="IT Equipment", status="Active", cost=15000, purchase_date=datetime(2023,3,20).date()),
                Asset(tag="AST003", name="Delivery Van", site_id=sites[0].id, location_id=None,
                      serial="VAN45678", category="Vehicle", status="Active", cost=35000, purchase_date=datetime(2022,11,5).date()),
            ]
            session.add_all(assets)
            
            # Commit all changes
            session.commit()
            logger.info("Sample data added successfully")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str):
        """
        Execute a raw SQL query and return results
        Useful for testing the SQL generated by Gemini
        """
        session = self.get_session()
        try:
            result = session.execute(query)
            if result.returns_rows:
                return [dict(row) for row in result]
            return None
        finally:
            session.close()

# Create global database manager instance
db_manager = DatabaseManager()