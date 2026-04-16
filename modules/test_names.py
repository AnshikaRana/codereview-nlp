from name_quality import name_quality_score

code = """
def calculate_total_price(item_price, tax):
    total_price = item_price + tax
    return total_price
"""

print(name_quality_score(code))