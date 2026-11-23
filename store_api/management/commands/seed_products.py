from decimal import Decimal
from django.core.management.base import BaseCommand
from store_api.models import Product


class Command(BaseCommand):
    help = "Populates the database with 24 smartphone and gadget products."

    def handle(self, *args, **kwargs):
        products_data = [
            ("iPhone 13 Pro Max 256GB", "Apple", "6.7-inch Super Retina XDR display with ProMotion, A15 Bionic chip, Sierra Blue.", Decimal("48990.00"), 12),
            ("iPhone 15 Pro 128GB", "Apple", "Titanium design, A17 Pro chip, 48MP main camera system, USB-C.", Decimal("62990.00"), 10),
            ("iPhone 14 128GB", "Apple", "6.1-inch OLED display, A15 Bionic, Dual-camera system with Photonic Engine.", Decimal("41990.00"), 18),
            ("Galaxy S24 Ultra 512GB", "Samsung", "6.8-inch QHD+ Dynamic AMOLED 2X, Snapdragon 8 Gen 3, built-in S Pen.", Decimal("74990.00"), 9),
            ("Galaxy A55 5G 256GB", "Samsung", "6.6-inch Super AMOLED 120Hz, Exynos 1480, 50MP OIS triple camera.", Decimal("24990.00"), 25),
            ("Galaxy Z Flip 5 256GB", "Samsung", "Compact foldable smartphone with 3.4-inch Flex Window cover screen.", Decimal("52990.00"), 7),
            ("Xiaomi 14 512GB", "Xiaomi", "Leica Summilux optical lens, Snapdragon 8 Gen 3, 90W HyperCharge.", Decimal("45990.00"), 14),
            ("Redmi Note 13 Pro+ 5G", "Xiaomi", "200MP OIS camera, 1.5K curved AMOLED display, 120W HyperCharge.", Decimal("20990.00"), 30),
            ("POCO X6 Pro 5G 512GB", "POCO", "Dimensity 8300-Ultra flagship processor, 120Hz Flow AMOLED display.", Decimal("16990.00"), 28),
            ("POCO F6 5G 256GB", "POCO", "Snapdragon 8s Gen 3, 50MP Sony IMX882 OIS camera, 90W turbo charging.", Decimal("19490.00"), 22),
            ("Tecno Camon 30 Pro 5G", "Tecno", "50MP Sony IMX890 OIS main camera, 144Hz AMOLED, 70W Ultra Charge.", Decimal("14999.00"), 35),
            ("Tecno Pova 6 Pro 5G", "Tecno", "6000mAh mega battery, 70W Ultra Charge, Dynamic-Tech LED design.", Decimal("11999.00"), 40),
            ("Vivo V30 5G 256GB", "Vivo", "Aura Light Portrait 3.0, 50MP AF group selfie, ultra-slim 3D curved screen.", Decimal("24999.00"), 19),
            ("Vivo X100 Pro 512GB", "Vivo", "ZEISS APO Floating Telephoto Camera, Dimensity 9300, V3 imaging chip.", Decimal("59999.00"), 8),
            ("OPPO Reno 11 Pro 5G", "OPPO", "32MP Telephoto Portrait Camera, 80W SUPERVOOC flash charge.", Decimal("27999.00"), 16),
            ("OPPO Find N3 Flip", "OPPO", "Hasselblad camera for mobile, 44W SUPERVOOC, pocketable flagship.", Decimal("49999.00"), 6),
            ("Realme 12 Pro+ 5G", "Realme", "Periscope portrait camera, luxury watch design, 120Hz curved vision display.", Decimal("23999.00"), 21),
            ("Realme GT 6T 256GB", "Realme", "Snapdragon 7+ Gen 3, 6000-nit hyper display, 120W SUPERVOOC.", Decimal("22499.00"), 17),
            ("Infinix GT 20 Pro 5G", "Infinix", "Dedicated gaming display chip, Dimensity 8200 Ultimate, Mecha Loop LED.", Decimal("15999.00"), 32),
            ("Infinix Note 40 Pro+ 5G", "Infinix", "100W All-Round FastCharge 2.0, 20W Wireless MagCharge, 108MP OIS.", Decimal("13999.00"), 29),
            ("Pixel 8 Pro 256GB", "Google", "Google Tensor G3, pro-level triple camera with Magic Editor AI.", Decimal("54990.00"), 11),
            ("OnePlus 12 512GB", "OnePlus", "4th-Gen Hasselblad Camera, Snapdragon 8 Gen 3, 100W SUPERVOOC.", Decimal("51990.00"), 13),
            ("ROG Phone 8 Pro 512GB", "ASUS", "Flagship gaming smartphone with AniMe Vision mini-LED matrix and AirTriggers.", Decimal("64990.00"), 9),
            ("Nothing Phone (2a) 256GB", "Nothing", "Glyph Interface LEDs, custom Dimensity 7200 Pro, clean Nothing OS.", Decimal("18990.00"), 24),
        ]

        created_count = 0
        for name, brand, description, price, stock in products_data:
            _, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "brand": brand,
                    "category": "Smartphones & Gadgets",
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "is_available": True,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Done! Added {created_count} new products (Total in DB: {Product.objects.count()}).")
        )