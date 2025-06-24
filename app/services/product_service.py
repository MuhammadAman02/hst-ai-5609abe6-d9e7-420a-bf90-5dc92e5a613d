"""Product service for managing luxury watch products"""

import json
import random
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import Product

class ProductService:
    """Service for managing products"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.db.query(Product).filter(Product.is_available == True).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id, Product.is_available == True).first()
    
    def get_featured_products(self, limit: int = 6) -> List[Product]:
        """Get featured products"""
        return self.db.query(Product).filter(
            Product.is_featured == True, 
            Product.is_available == True
        ).limit(limit).all()
    
    def get_products_by_collection(self, collection: str) -> List[Product]:
        """Get products by collection"""
        return self.db.query(Product).filter(
            Product.collection == collection,
            Product.is_available == True
        ).all()
    
    def get_collections(self) -> List[str]:
        """Get all unique collections"""
        collections = self.db.query(Product.collection).distinct().all()
        return [collection[0] for collection in collections]
    
    def get_related_products(self, collection: str, exclude_id: int, limit: int = 4) -> List[Product]:
        """Get related products from same collection"""
        return self.db.query(Product).filter(
            Product.collection == collection,
            Product.id != exclude_id,
            Product.is_available == True
        ).limit(limit).all()
    
    async def create_sample_products(self):
        """Create sample Rolex-inspired products"""
        sample_products = [
            {
                "name": "Submariner Date",
                "collection": "Submariner",
                "model": "126610LN",
                "price": 8950.00,
                "description": "The Submariner Date is a legendary diving watch, waterproof to 300 metres. Crafted from Oystersteel with a unidirectional rotatable bezel.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "41mm",
                    "Water Resistance": "300m/1,000ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,submariner&sig=1001",
                "is_featured": True
            },
            {
                "name": "GMT-Master II",
                "collection": "GMT-Master",
                "model": "126710BLNR",
                "price": 9700.00,
                "description": "The GMT-Master II is the ultimate traveller's watch. Features a bidirectional rotatable 24-hour graduated bezel.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "40mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,gmt&sig=1002",
                "is_featured": True
            },
            {
                "name": "Datejust 36",
                "collection": "Datejust",
                "model": "126234",
                "price": 6850.00,
                "description": "The Datejust is the archetype of the classic watch. A symbol of universal and timeless elegance.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel and White Gold",
                    "Case Diameter": "36mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Jubilee, five-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,datejust&sig=1003",
                "is_featured": True
            },
            {
                "name": "Daytona",
                "collection": "Daytona",
                "model": "116500LN",
                "price": 13150.00,
                "description": "The Cosmograph Daytona is designed to be the ultimate racing chronograph.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "40mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, chronograph",
                    "Power Reserve": "Approximately 72 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,daytona&sig=1004",
                "is_featured": True
            },
            {
                "name": "Explorer",
                "collection": "Explorer",
                "model": "124270",
                "price": 6550.00,
                "description": "The Explorer is a tool watch in its purest form. Designed for extreme conditions and adventures.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "36mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,explorer&sig=1005",
                "is_featured": False
            },
            {
                "name": "Sea-Dweller",
                "collection": "Sea-Dweller",
                "model": "126600",
                "price": 11350.00,
                "description": "The Sea-Dweller is the ultimate deep-sea diving watch, waterproof to 1,220 metres.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "43mm",
                    "Water Resistance": "1,220m/4,000ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,diving&sig=1006",
                "is_featured": True
            },
            {
                "name": "Yacht-Master",
                "collection": "Yacht-Master",
                "model": "126622",
                "price": 12050.00,
                "description": "The Yacht-Master embodies the privileged relationship between Rolex and the world of sailing.",
                "specifications": json.dumps({
                    "Case Material": "Rolesium (Oystersteel and Platinum)",
                    "Case Diameter": "40mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oysterflex"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,yacht&sig=1007",
                "is_featured": False
            },
            {
                "name": "Air-King",
                "collection": "Air-King",
                "model": "126900",
                "price": 6200.00,
                "description": "The Air-King pays tribute to the pioneers of flight and the role of Rolex in the epic story of aviation.",
                "specifications": json.dumps({
                    "Case Material": "Oystersteel",
                    "Case Diameter": "40mm",
                    "Water Resistance": "100m/330ft",
                    "Movement": "Perpetual, mechanical, self-winding",
                    "Power Reserve": "Approximately 70 hours",
                    "Bracelet": "Oyster, flat three-piece links"
                }),
                "image_url": "https://source.unsplash.com/800x800/?luxury-watch,aviation&sig=1008",
                "is_featured": False
            }
        ]
        
        for product_data in sample_products:
            product = Product(**product_data)
            self.db.add(product)
        
        self.db.commit()