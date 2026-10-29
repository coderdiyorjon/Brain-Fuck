def calc_total(price: int, tax_rate: int) -> int:
    """Calculaes total cost depending on given price and tax rate
    If price or tax is negative, returns 0
    """
    
    if price < 0 or tax_rate < 0:
        return 0
    
    tax: int = (price * tax_rate) // 100
    return price + tax
