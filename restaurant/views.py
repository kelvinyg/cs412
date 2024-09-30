from django.shortcuts import render, redirect
import random 
from datetime import datetime, timedelta

# Create your views here.
daily_special_prices = {
    "Bluefin Tuna": 25,
    "Pan Seared Scallops": 30,
    "Szechuan Spicy Fish": 20,
    "Grilled Swordfish with Lemon Butter": 28,
    "Herb-Crusted Salmon with Dill Sauce": 22,
    "Garlic Butter Shrimp Skewers": 24,
    "Thai Coconut Curry Shrimp": 26,
    "Crab-Stuffed Flounder": 32,
    "Blackened Red Snapper with Mango Salsa": 27,
    "Steamed Clams with White Wine and Garlic": 18,
    "Crispy Soft-Shell Crab Sandwich": 15,
    "Sesame-Crusted Ahi Tuna": 35,
    "Lobster Ravioli in Creamy Tomato Sauce": 40,
    "Chilean Sea Bass with Citrus Glaze": 38,
    "Oysters Rockefeller": 30,
    "Cedar Plank Salmon": 36,
    "Smoked Trout with Horseradish Cream": 29,
}
menu_prices = {
            'Cajun Seafood Boil (Base)': 10,
            'Lobster Rolls': 35,
            'Chinese Steamed Fish': 20,
            'Oysters by the Sea (1/2 dozen)': 18,
}
customization_prices = {
    'Crawfish': 15,
    'Alaskan King Crab': 25,
    'Shrimp': 10,
    'Lobster Tail': 30,
}

def main(request):
    return render(request, 'restaurant/main.html')


def order(request):
    # Choose a random daily special from the list
    daily_item = random.choice(list(daily_special_prices.keys()))
    
    # Look up the price of the chosen daily special
    daily_special_price = daily_special_prices[daily_item]
    
    # Pass the special and its price to the context
    context = {
        'special': daily_item,  
        'special_price': daily_special_price, 
        'menu': menu_prices  
    }

    return render(request, 'restaurant/order.html', context)
def confirmation(request):
    if request.method == 'POST':
        # Read the form data
        customer_name = request.POST['name']
        customer_email = request.POST['email']
        customer_phone = request.POST['phone']

        items = request.POST.getlist('items') 
        
        # Additional customizations selected for Seafood Boil
        customizations = request.POST.getlist('customize_seafood_boil')
        
        include_special = request.POST.get('include_special')

        total_price = sum(menu_prices.get(item, 0) for item in items)
        
        # Add the price for the daily special if selected
        if include_special and include_special in daily_special_prices:
            total_price += daily_special_prices[include_special]
            items.append(include_special)  # Add daily special to the list of items

        # Add the prices of any selected customizations
        for customization in customizations:
            total_price += customization_prices.get(customization, 0)

        context = {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'items': items,
            'customizations': customizations,
            'total_price': total_price,
            'special_instructions': request.POST.get('special_instructions'),
        }

        return render(request, 'restaurant/confirmation.html', context)

    return redirect('order')