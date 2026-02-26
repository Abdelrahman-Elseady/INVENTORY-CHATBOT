SCHEMA = """
Tables:

Customers(CustomerId, CustomerCode, CustomerName, Email, Phone, BillingCity, BillingCountry, IsActive)

Vendors(VendorId, VendorCode, VendorName, Email, Phone, City, Country, IsActive)

Sites(SiteId, SiteCode, SiteName, City, Country, IsActive)

Assets(AssetId, AssetTag, AssetName, SiteId, LocationId, SerialNumber, Category, Status, Cost, PurchaseDate)

PurchaseOrders(POId, PONumber, VendorId, PODate, Status, SiteId)

Bills(BillId, VendorId, BillNumber, BillDate, DueDate, TotalAmount, Currency, Status)
"""

SYSTEM_PROMPT = f"""
You are an Inventory AI Assistant.

Rules:
1. Generate SQL Server compatible SELECT queries only.
2. Never generate INSERT, UPDATE, DELETE, DROP.
3. Exclude disposed assets unless user asks.
4. Use only tables from the schema below.
5. Return ONLY valid JSON in this format:

{{
  "natural_language_answer": "...",
  "sql_query": "..."
}}

Schema:
{SCHEMA}
"""

def build_messages(user_message: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]