from django.shortcuts import render

# Create your views here.
# file = [
#   # "Customer",
#   # "Addresses",
#   # "Category",
#   # "Orders",
#   # "Order_Items",
#   # "Payments",
#   # "Product_Reviews",
#   # "Cart",
#   # "Cart_Items",
#   # "InventoryTransactions",
#   # "Promotions",
#   # "Product_Promotions",
#   # "Wishlists",
#   # "Wishlist_Items",
#   # "Shipping_Methods",
#   # "Order_Shipping",
#   # "Taxes",
#   # "Order_Taxes",
#   # "Product_Images",
#   # "Vendors",
#   # "Product_Vendors",
#   # "Customer_Support_Tickets",
#   # "Customer_Support_Responses",
#   # "Admins",
#   # "Product_Bundles",
#   # "Bundle_Items",
#   # "Customer_Segments",
#   # "Customer_Segment_Members",
#   # "Analytics_Events",
#   # "Gift_Cards",
#   # "Gift_Card_Transactions",
#   # "Returns",
#   # "Return_Items",
#   # "Subscriptions"
#   "Notifications",
#   "Notification_Preferences",
#   "Notification_Templates",
#   "Product_Rankings",
#   "Product_Ranking_Metrics",
#   "Recommendations",
#   "Search_History",
#   "Loyalty_Programs",
#   "Customer_Loyalty",
#   "Loyalty_Transactions",
#   "Abandoned_Carts",
#   "Price_History",
#   "Product_Tags",
#   "Product_Tag_Associations",
#   "Dynamic_Pricing_Rules"
# ]
# for f in file:
#   fileName = f.replace('_','')
#   with open(f'customer/models/{fileName}Model.py', 'x') as filewrite:
#     filewrite.write(f"""from django.db import models
# import uuid
# from django.utils.text import slugify
# from django.contrib.auth import get_user_model
# from django.conf import settings
# from customer.models.DateModel import DateModel
                    
# class {fileName.replace("Model", "")}(models.Model, DateModel):
#   {f.lower()}_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
#   customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_id")




#   def str(self):
#     return "This is {fileName.replace("Model","")} data"
# """)