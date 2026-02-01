from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import random

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Item(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str] = mapped_column(String(250), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    on_discount: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    discount_price: Mapped[float] = mapped_column(nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

def add_random_items():
    """Add 36 random cosmetic items to the database"""
    with app.app_context():
        db.create_all()
        
        # Check if database is already populated
        if Item.query.count() == 0:
            # Cosmetic product names and categories
            cosmetics = [
                ("Hydrating Face Moisturizer", "Skincare", "A lightweight, hydrating moisturizer for all skin types"),
                ("Vitamin C Serum", "Skincare", "Brightening serum with 20% vitamin C for radiant skin"),
                ("Matte Red Lipstick", "Makeup", "Long-lasting matte red lipstick for bold looks"),
                ("Eyeshadow Palette - Nude", "Makeup", "12-shade neutral eyeshadow palette"),
                ("Waterproof Mascara", "Makeup", "Volumizing waterproof mascara for dramatic lashes"),
                ("Anti-Aging Night Cream", "Skincare", "Rich night cream with retinol and peptides"),
                ("Cleansing Oil", "Skincare", "Gentle cleansing oil removes makeup and impurities"),
                ("Rose Gold Highlighter", "Makeup", "Shimmering highlighter for a radiant glow"),
                ("Liquid Foundation", "Makeup", "Full coverage liquid foundation with SPF 30"),
                ("Exfoliating Face Scrub", "Skincare", "Gentle exfoliating scrub with natural ingredients"),
                ("Nude Lip Gloss", "Makeup", "Shiny nude lip gloss with vanilla scent"),
                ("Eye Makeup Remover", "Skincare", "Gentle oil-free eye makeup remover"),
                ("Blush Palette", "Makeup", "4-shade blush palette in warm tones"),
                ("Hyaluronic Acid Serum", "Skincare", "Intense hydration serum with pure hyaluronic acid"),
                ("Setting Spray", "Makeup", "Long-lasting makeup setting spray"),
                ("Micellar Water", "Skincare", "All-in-one cleanser and makeup remover"),
                ("Eyebrow Pencil", "Makeup", "Precision eyebrow pencil with spoolie brush"),
                ("Sunscreen SPF 50", "Skincare", "Broad spectrum sunscreen for daily protection"),
                ("Contour Kit", "Makeup", "3-shade contour and highlight kit"),
                ("Clay Face Mask", "Skincare", "Purifying clay mask for deep cleansing"),
                ("Eyeliner - Black", "Makeup", "Waterproof liquid eyeliner pen"),
                ("Facial Toner", "Skincare", "Balancing toner with witch hazel"),
                ("Bronzer", "Makeup", "Matte bronzer for sun-kissed skin"),
                ("Under Eye Cream", "Skincare", "Brightening eye cream reduces dark circles"),
                ("Lip Liner Set", "Makeup", "6-piece nude lip liner set"),
                ("Makeup Brush Set", "Tools", "12-piece professional makeup brush set"),
                ("Face Primer", "Makeup", "Smoothing primer for flawless makeup application"),
                ("Sheet Mask - Collagen", "Skincare", "Hydrating collagen sheet mask"),
                ("Nail Polish Set", "Nails", "5-piece nude nail polish collection"),
                ("Makeup Sponge Set", "Tools", "3-piece beauty sponge set"),
                ("Perfume - Floral", "Fragrance", "Light floral perfume with notes of jasmine"),
                ("Body Lotion", "Body Care", "Moisturizing body lotion with shea butter"),
                ("Hand Cream", "Body Care", "Nourishing hand cream with vitamin E"),
                ("Hair Serum", "Hair Care", "Smoothing hair serum for frizz control"),
                ("Dry Shampoo", "Hair Care", "Volumizing dry shampoo for fresh hair"),
                ("Makeup Remover Wipes", "Skincare", "Gentle makeup remover wipes - 30 pack")
            ]
            
            # Add items to database
            for i, (name, category, description) in enumerate(cosmetics, 1):
                # Generate random price between $5 and $89
                price = round(random.uniform(5.0, 89.99), 2)
                
                # Random discount (30% chance)
                on_discount = random.choice([True, False, False, False])
                discount_price = round(price * 0.7, 2) if on_discount else None
                
                # Random stock between 0 and 150
                stock = random.randint(0, 150)
                
                # Generate SKU
                sku = f"COS-{i:04d}"
                
                # Use picsum.photos for random images
                image_url = f"https://picsum.photos/id/{random.randint(1, 200)}/400/400"
                
                item = Item(
                    name=name,
                    description=description,
                    image_url=image_url,
                    price=price,
                    on_discount=on_discount,
                    discount_price=discount_price,
                    stock=stock,
                    sku=sku,
                    category=category,
                    is_active=True
                )
                db.session.add(item)
            
            db.session.commit()
            print(f"✅ Successfully added 36 cosmetic items to the database!")
        else:
            print(f"Database already contains {Item.query.count()} items.")

if __name__ == "__main__":
    add_random_items()
