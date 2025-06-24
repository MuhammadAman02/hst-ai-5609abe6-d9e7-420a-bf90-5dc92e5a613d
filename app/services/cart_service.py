"""Cart service for managing shopping cart functionality"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import CartItem, Product

class CartService:
    """Service for managing shopping cart"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_to_cart(self, session_id: str, product_id: int, quantity: int = 1, user_id: Optional[int] = None) -> bool:
        """Add product to cart"""
        try:
            # Check if item already exists in cart
            existing_item = self.db.query(CartItem).filter(
                CartItem.session_id == session_id,
                CartItem.product_id == product_id
            ).first()
            
            if existing_item:
                existing_item.quantity += quantity
            else:
                cart_item = CartItem(
                    session_id=session_id,
                    product_id=product_id,
                    quantity=quantity,
                    user_id=user_id
                )
                self.db.add(cart_item)
            
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    def remove_from_cart(self, session_id: str, product_id: int):
        """Remove product from cart"""
        cart_item = self.db.query(CartItem).filter(
            CartItem.session_id == session_id,
            CartItem.product_id == product_id
        ).first()
        
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()
    
    def get_cart_items(self, session_id: str) -> List[dict]:
        """Get all cart items with product details"""
        cart_items = self.db.query(CartItem).filter(
            CartItem.session_id == session_id
        ).all()
        
        result = []
        for item in cart_items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                result.append({
                    "cart_item": item,
                    "product": product,
                    "subtotal": product.price * item.quantity
                })
        
        return result
    
    def get_cart_total(self, session_id: str) -> float:
        """Get total cart value"""
        cart_items = self.get_cart_items(session_id)
        return sum(item["subtotal"] for item in cart_items)
    
    def get_cart_count(self, session_id: str) -> int:
        """Get total number of items in cart"""
        return self.db.query(CartItem).filter(
            CartItem.session_id == session_id
        ).count()
    
    def clear_cart(self, session_id: str):
        """Clear all items from cart"""
        self.db.query(CartItem).filter(
            CartItem.session_id == session_id
        ).delete()
        self.db.commit()