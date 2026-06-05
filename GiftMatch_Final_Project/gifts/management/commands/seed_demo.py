from datetime import timedelta
from urllib.parse import quote_plus
import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from gifts.choices import RECIPIENT_OCCASION_MAP
from gifts.models import Category, Gift, Interest
from occasions.models import Notification, Occasion
from wishlist.models import WishlistItem

STORE_BASES = {
    'Shopee': 'https://shopee.ph/search?keyword=',
    'Lazada': 'https://www.lazada.com.ph/catalog/?q=',
    'TikTok Shop': 'https://www.tiktok.com/shop/search?q=',
    'Temu': 'https://www.temu.com/search_result.html?search_key=',
}

OCCASION_LABELS = {
    'birthday': 'Birthday',
    'anniversary': 'Anniversary',
    'monthsary': 'Monthsary',
    'graduation': 'Graduation',
    'christmas': 'Christmas',
    'new_year': 'New Year',
    'valentines': "Valentine's Day",
    'mothers_day': "Mother's Day",
    'fathers_day': "Father's Day",
    'family_reunion': 'Family Reunion',
    'wedding': 'Wedding',
    'baby_shower': 'Baby Shower',
    'promotion': 'Promotion',
    'retirement': 'Retirement',
    'other': 'Special Event',
}

RECIPIENT_LABELS = {
    'partner': 'Partner',
    'family': 'Family',
    'friend': 'Friend',
    'coworker': 'Coworker',
}

INTEREST_DATA = {
    'Technology': ('⌘', 'Tech', 'A useful tech gift that makes daily tasks easier and more enjoyable.', 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80', ['Smart Gadget Kit', 'Portable Power Bank', 'Bluetooth Tracker', 'Tablet Stand']),
    'Gaming': ('◈', 'Tech', 'A fun gaming accessory for relaxing, playing, and upgrading a setup.', 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=900&q=80', ['RGB Gaming Mouse', 'Controller Dock', 'Gaming Headset', 'Desk Light Bar']),
    'Music': ('♪', 'Tech', 'A practical audio gift for listening to music, calls, and entertainment.', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80', ['Wireless Earbuds', 'Studio Headphones', 'Mini Speaker', 'Vinyl Display Stand']),
    'Sports': ('●', 'Sports', 'A sporty gift for active routines, outdoor play, and training days.', 'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80', ['Sports Towel Set', 'Insulated Water Bottle', 'Training Bands', 'Performance Cap']),
    'Fitness': ('◆', 'Sports', 'A wellness gift for workout motivation, recovery, and healthy habits.', 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80', ['Fitness Resistance Kit', 'Yoga Mat Set', 'Recovery Massage Ball', 'Smart Jump Rope']),
    'Travel': ('✈', 'Experiences', 'A travel-friendly item for trips, organization, and memorable adventures.', 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=80', ['Travel Organizer', 'Passport Holder Set', 'Packing Cube Bundle', 'Memory Journal']),
    'Coffee': ('☕', 'Gourmet', 'A cozy coffee-themed gift for slow mornings and relaxing breaks.', 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=900&q=80', ['Coffee Sampler Box', 'French Press Set', 'Ceramic Mug Pair', 'Cold Brew Bottle']),
    'Books': ('▤', 'Home', 'A thoughtful gift for reading, studying, planning, and quiet hobbies.', 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=900&q=80', ['Reading Lamp', 'Personal Journal', 'Book Stand', 'Bookmark Gift Set']),
    'Fashion': ('◇', 'Fashion', 'A stylish accessory that works for everyday wear and special occasions.', 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80', ['Minimalist Watch', 'Leather Wallet', 'Silk Scarf', 'Everyday Tote Bag']),
    'Beauty': ('✧', 'Self Care', 'A self-care gift for skincare, confidence, and pampering routines.', 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=900&q=80', ['Skincare Starter Kit', 'Perfume Discovery Set', 'Vanity Organizer', 'Lip Care Bundle']),
    'Photography': ('◎', 'Creative', 'A creative gift for capturing memories and improving photo setups.', 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80', ['Tripod Phone Stand', 'Camera Strap', 'Mini Photo Printer', 'Lens Cleaning Kit']),
    'Movies': ('▣', 'Entertainment', 'A fun home-entertainment gift for movie nights and cozy weekends.', 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=900&q=80', ['Movie Night Snack Box', 'Projector Stand', 'Cinema Blanket', 'Streaming Gift Card']),
    'Cooking': ('⌂', 'Gourmet', 'A kitchen gift for people who enjoy preparing meals and trying recipes.', 'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80', ['Chef Knife Set', 'Spice Rack Starter', 'Copper Pan', 'Recipe Journal']),
    'Art': ('✎', 'Creative', 'A creative gift for drawing, painting, crafting, and personal expression.', 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80', ['Watercolor Set', 'Sketchbook Bundle', 'Acrylic Paint Kit', 'Desk Easel']),
    'Pets': ('♡', 'Home', 'A sweet gift for pet lovers and their favorite companions.', 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?auto=format&fit=crop&w=900&q=80', ['Pet Portrait Voucher', 'Treat Box', 'Pet Toy Bundle', 'Custom Name Tag']),
    'Cars': ('▰', 'Automotive', 'A practical car accessory for cleaner, safer, and more comfortable driving.', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80', ['Car Organizer', 'Dashboard Phone Mount', 'Mini Vacuum Cleaner', 'Emergency Tool Kit']),
}


PRODUCT_IMAGE_URLS = {
    # Technology
    'Smart Gadget Kit': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80',
    'Portable Power Bank': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=900&q=80',
    'Bluetooth Tracker': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80',
    'Tablet Stand': 'https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?auto=format&fit=crop&w=900&q=80',
    # Gaming
    'RGB Gaming Mouse': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=900&q=80',
    'Controller Dock': 'https://images.unsplash.com/photo-1605901309584-818e25960a8f?auto=format&fit=crop&w=900&q=80',
    'Gaming Headset': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=900&q=80',
    'Desk Light Bar': 'https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=900&q=80',
    # Music
    'Wireless Earbuds': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=80',
    'Studio Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
    'Mini Speaker': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80',
    'Vinyl Display Stand': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80',
    # Sports/Fitness
    'Sports Towel Set': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80',
    'Insulated Water Bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80',
    'Training Bands': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?auto=format&fit=crop&w=900&q=80',
    'Performance Cap': 'https://images.unsplash.com/photo-1521369909029-2afed882baee?auto=format&fit=crop&w=900&q=80',
    'Fitness Resistance Kit': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    'Yoga Mat Set': 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?auto=format&fit=crop&w=900&q=80',
    'Recovery Massage Ball': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=900&q=80',
    'Smart Jump Rope': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=900&q=80',
    # Travel
    'Travel Organizer': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=80',
    'Passport Holder Set': 'https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=900&q=80',
    'Packing Cube Bundle': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80',
    'Memory Journal': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=900&q=80',
    # Coffee/Books
    'Coffee Sampler Box': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=900&q=80',
    'French Press Set': 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=900&q=80',
    'Ceramic Mug Pair': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80',
    'Cold Brew Bottle': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80',
    'Reading Lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80',
    'Personal Journal': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=900&q=80',
    'Book Stand': 'https://images.unsplash.com/photo-1519682337058-a94d519337bc?auto=format&fit=crop&w=900&q=80',
    'Bookmark Gift Set': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80',
    # Fashion/Beauty
    'Minimalist Watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80',
    'Leather Wallet': 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80',
    'Silk Scarf': 'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80',
    'Everyday Tote Bag': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80',
    'Skincare Starter Kit': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=900&q=80',
    'Perfume Discovery Set': 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=900&q=80',
    'Vanity Organizer': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=900&q=80',
    'Lip Care Bundle': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=900&q=80',
    # Photography/Movies
    'Tripod Phone Stand': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80',
    'Camera Strap': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=900&q=80',
    'Mini Photo Printer': 'https://images.unsplash.com/photo-1510127034890-ba27508e9f1c?auto=format&fit=crop&w=900&q=80',
    'Lens Cleaning Kit': 'https://images.unsplash.com/photo-1452780212940-6f5c0d14d848?auto=format&fit=crop&w=900&q=80',
    'Movie Night Snack Box': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=900&q=80',
    'Projector Stand': 'https://images.unsplash.com/photo-1601944179066-29786cb9d32a?auto=format&fit=crop&w=900&q=80',
    'Cinema Blanket': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80',
    'Streaming Gift Card': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?auto=format&fit=crop&w=900&q=80',
    # Cooking/Art/Pets/Cars
    'Chef Knife Set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?auto=format&fit=crop&w=900&q=80',
    'Spice Rack Starter': 'https://images.unsplash.com/photo-1532336414038-cf19250c5757?auto=format&fit=crop&w=900&q=80',
    'Copper Pan': 'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80',
    'Recipe Journal': 'https://images.unsplash.com/photo-1514986888952-8cd320577b68?auto=format&fit=crop&w=900&q=80',
    'Watercolor Set': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80',
    'Sketchbook Bundle': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=900&q=80',
    'Acrylic Paint Kit': 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=900&q=80',
    'Desk Easel': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80',
    'Pet Portrait Voucher': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?auto=format&fit=crop&w=900&q=80',
    'Treat Box': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?auto=format&fit=crop&w=900&q=80',
    'Pet Toy Bundle': 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=900&q=80',
    'Custom Name Tag': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=900&q=80',
    'Car Organizer': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80',
    'Dashboard Phone Mount': 'https://images.unsplash.com/photo-1593941707882-a5bba13938c2?auto=format&fit=crop&w=900&q=80',
    'Mini Vacuum Cleaner': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80',
    'Emergency Tool Kit': 'https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=900&q=80',
}

DEFAULT_PRODUCT_IMAGE = 'https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&w=900&q=80'

PRICE_CYCLE = [399, 699, 999, 1299, 1799, 2499, 3499, 4999]
STORES = ['Shopee', 'Lazada', 'TikTok Shop', 'Temu']


class Command(BaseCommand):
    help = 'Seed GiftMatch with expanded demo data and accounts.'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@giftmatch.local', 'is_staff': True, 'is_superuser': True})
        admin.is_staff = True
        admin.is_superuser = True
        if created:
            admin.set_password('admin12345')
        admin.save()

        demo, created = User.objects.get_or_create(username='sarah', defaults={'email': 'sarah@giftmatch.local', 'first_name': 'Sarah'})
        if created:
            demo.set_password('demo12345')
            demo.save()
        demo.profile.full_name = 'Sarah Reyes'
        demo.profile.bio = 'GiftMatch demo user for final project presentation.'
        demo.profile.save()

        # Optional social-login setup. Replace these env values with real OAuth credentials
        # from Google Cloud/Facebook Developers for production use.
        try:
            from django.contrib.sites.models import Site
            from allauth.socialaccount.models import SocialApp
            site, _ = Site.objects.get_or_create(id=1, defaults={'domain': '127.0.0.1:8000', 'name': 'GiftMatch Local'})
            site.domain = os.getenv('SITE_DOMAIN', '127.0.0.1:8000')
            site.name = 'GiftMatch Local'
            site.save()
            social_apps = [
                ('google', 'Google', os.getenv('GOOGLE_CLIENT_ID', 'CHANGE_ME_GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET', 'CHANGE_ME_GOOGLE_CLIENT_SECRET')),
                ('facebook', 'Facebook', os.getenv('FACEBOOK_CLIENT_ID', 'CHANGE_ME_FACEBOOK_CLIENT_ID'), os.getenv('FACEBOOK_CLIENT_SECRET', 'CHANGE_ME_FACEBOOK_CLIENT_SECRET')),
            ]
            for provider, name, client_id, secret in social_apps:
                app, _ = SocialApp.objects.get_or_create(provider=provider, name=f'{name} Login', defaults={'client_id': client_id, 'secret': secret})
                app.client_id = client_id
                app.secret = secret
                app.save()
                app.sites.set([site])
        except Exception:
            pass

        # Reset demo catalog so old placeholder records do not affect recommendation accuracy.
        WishlistItem.objects.all().delete()
        Notification.objects.all().delete()
        Gift.objects.all().delete()
        Interest.objects.all().delete()
        Category.objects.all().delete()

        categories = {
            'Tech': 'Useful gadgets and digital accessories.',
            'Self Care': 'Wellness, skincare, and relaxation gifts.',
            'Home': 'Home, decor, and everyday comfort items.',
            'Fashion': 'Style accessories and wearable gifts.',
            'Gourmet': 'Food, drinks, and kitchen experiences.',
            'Experiences': 'Memorable activities and celebration ideas.',
            'Sports': 'Active lifestyle and training gifts.',
            'Creative': 'Artistic and maker-focused gifts.',
            'Entertainment': 'Movie, music, and home fun gifts.',
            'Automotive': 'Car-related practical accessories.',
        }
        category_objs = {name: Category.objects.create(name=name, description=desc) for name, desc in categories.items()}
        interest_icon_slugs = {
            'Technology': 'technology', 'Gaming': 'gaming', 'Music': 'music', 'Sports': 'sports',
            'Fitness': 'fitness', 'Travel': 'travel', 'Coffee': 'coffee', 'Books': 'books',
            'Fashion': 'fashion', 'Beauty': 'beauty', 'Photography': 'photography', 'Movies': 'movies',
            'Cooking': 'cooking', 'Art': 'art', 'Pets': 'pets', 'Cars': 'cars',
        }
        interest_objs = {
            name: Interest.objects.create(name=name, icon=interest_icon_slugs.get(name, 'spark'))
            for name in INTEREST_DATA.keys()
        }

        created_gifts = 0
        # Create a larger catalog: each recipient/occasion/interest receives multiple product options
        # across all marketplaces and price points, so results remain varied without showing random items.
        for recipient, occasions in RECIPIENT_OCCASION_MAP.items():
            for occasion in occasions:
                for index, (interest_name, data) in enumerate(INTEREST_DATA.items()):
                    icon, category_name, desc, image, titles = data
                    for title_index, title in enumerate(titles):
                        for store_index, store in enumerate(STORES):
                            price = PRICE_CYCLE[(index + title_index + store_index + len(occasion)) % len(PRICE_CYCLE)]
                            name = f"{title} for {OCCASION_LABELS.get(occasion, 'Special Event')}"
                            unique_name = f"{name} ({RECIPIENT_LABELS[recipient]})"
                            gift = Gift.objects.create(
                                name=unique_name,
                                description=desc,
                                category=category_objs[category_name],
                                recipient_type=recipient,
                                occasion_type=occasion,
                                minimum_budget=max(0, price - 300),
                                maximum_budget=price + 1500,
                                price=price,
                                product_image=PRODUCT_IMAGE_URLS.get(title, image or DEFAULT_PRODUCT_IMAGE),
                                store_link=STORE_BASES[store] + quote_plus(title),
                                store_name=store,
                                is_featured=created_gifts < 12,
                                rating=round(4.25 + (((index + title_index + store_index) % 7) * 0.09), 2),
                            )
                            gift.interests.set([interest_objs[interest_name]])
                            created_gifts += 1

        # A few carefully named homepage cards.
        featured_names = [
            'The Minimalist Workspace', 'The Wellness Retreat', 'Master Chef Series',
        ]
        for i, gift in enumerate(Gift.objects.all()[:3]):
            gift.name = featured_names[i]
            gift.is_featured = True
            gift.save()

        occ, _ = Occasion.objects.get_or_create(
            user=demo,
            event_title="Mom's 60th Birthday",
            defaults={
                'recipient_name': 'Mom',
                'occasion_type': 'birthday',
                'event_date': timezone.localdate() + timedelta(days=4),
                'reminder_days_before': 3,
                'notes': 'Find a meaningful milestone gift and prepare a card.',
            }
        )
        Occasion.objects.get_or_create(
            user=demo,
            event_title='Wedding: Alex & Sam',
            defaults={
                'recipient_name': 'Alex and Sam',
                'occasion_type': 'wedding',
                'event_date': timezone.localdate() + timedelta(days=18),
                'reminder_days_before': 7,
                'notes': 'Check their registry before buying.',
            }
        )

        first_gift = Gift.objects.filter(is_featured=True).first()
        if first_gift:
            WishlistItem.objects.get_or_create(user=demo, gift=first_gift)
            Notification.objects.create(
                user=demo,
                notification_type='wishlist',
                title='Wishlist price drop',
                message=f'A saved item from your list, {first_gift.name}, is ready to review.',
                gift=first_gift,
            )
        Notification.objects.create(
            user=demo,
            notification_type='occasion',
            title="3 days before Mom's Birthday",
            message="Order Mom's gift soon for on-time delivery.",
            occasion=occ,
        )
        Notification.objects.create(
            user=demo,
            notification_type='recommendation',
            title='New gift suggestion added',
            message='GiftMatch added fresh recommendations based on your interests and budget.',
        )

        self.stdout.write(self.style.SUCCESS(f'GiftMatch demo data seeded successfully with {created_gifts} gifts.'))
