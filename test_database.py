# test_database.py
from database import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test database creation and sample data"""
    
    print("=" * 50)
    print("Testing Database Setup")
    print("=" * 50)
    
    # Step 1: Create tables
    print("\n1. Creating database tables...")
    db_manager.create_tables()
    print("   ✓ Tables created successfully")
    
    # Step 2: Initialize with sample data
    print("\n2. Adding sample data...")
    db_manager.init_db()
    print("   ✓ Sample data added")
    
    # Step 3: Query and verify data
    print("\n3. Verifying data...")
    session = db_manager.get_session()
    
    from database import Customer, Vendor, Site, Location, Item, Asset
    
    # Check customers
    customer_count = session.query(Customer).count()
    print(f"   ✓ Customers: {customer_count} records")
    
    # Check vendors
    vendor_count = session.query(Vendor).count()
    print(f"   ✓ Vendors: {vendor_count} records")
    
    # Check sites
    site_count = session.query(Site).count()
    print(f"   ✓ Sites: {site_count} records")
    
    # Check locations
    location_count = session.query(Location).count()
    print(f"   ✓ Locations: {location_count} records")
    
    # Check items
    item_count = session.query(Item).count()
    print(f"   ✓ Items: {item_count} records")
    
    # Check assets
    asset_count = session.query(Asset).count()
    print(f"   ✓ Assets: {asset_count} records")
    
    session.close()
    
    # Step 4: Test some queries
    print("\n4. Testing sample queries...")
    
    # Query 1: Assets by site
    session = db_manager.get_session()
    result = session.execute("""
        SELECT s.name as site_name, COUNT(*) as asset_count
        FROM assets a
        JOIN sites s ON s.id = a.site_id
        GROUP BY s.name
    """)
    
    print("\n   Assets by site:")
    for row in result:
        print(f"      - {row.site_name}: {row.asset_count} assets")
    
    # Query 2: Total asset value
    result = session.execute("""
        SELECT SUM(cost) as total_value
        FROM assets
    """)
    total = result.first()
    print(f"\n   Total asset value: ${total.total_value:,.2f}")
    
    session.close()
    
    print("\n" + "=" * 50)
    print("Database test completed successfully!")
    print("=" * 50)
    
    # Show database file info
    import os
    if os.path.exists("inventory.db"):
        size = os.path.getsize("inventory.db")
        print(f"\nDatabase file: inventory.db ({size:,} bytes)")

if __name__ == "__main__":
    test_database()