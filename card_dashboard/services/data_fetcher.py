from database.connect_to_db import get_wb_cards_by_account, get_wb_accounts

def get_cards_statistics():
    accounts = get_wb_accounts()
    total_accounts = len(accounts)
    active_accounts = len([a for a in accounts if a.is_active])
    
    all_cards = []
    for account in accounts:
        cards = get_wb_cards_by_account(account.id)
        all_cards.extend(cards)
    
    total_cards = len(all_cards)
    total_quantity = sum(card.total_quantity or 0 for card in all_cards)
    
    prices = [card.current_price for card in all_cards if card.current_price]
    avg_price = sum(prices) / len(prices) if prices else 0
    
    brands = {}
    for card in all_cards:
        if card.brand_name:
            brands[card.brand_name] = brands.get(card.brand_name, 0) + 1
    
    categories = {}
    for card in all_cards:
        if card.subject_name:
            categories[card.subject_name] = categories.get(card.subject_name, 0) + 1
    
    return {
        'total_cards': total_cards,
        'total_accounts': total_accounts,
        'active_accounts': active_accounts,
        'total_quantity': total_quantity,
        'avg_price': round(avg_price, 2),
        'top_brands': sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10],
        'top_categories': sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
    }
