def defineproduct(stop):
    i in finder:
    name = i['name']
    category = i['category']
    try:
        sub_category = i['sub_category']
    except KeyError:
        sub_category = "null"
    try:
        sub_sub_category = i['sub_sub_category']
    except KeyError:
        sub_sub_category = 'null'
    brand = i['brand']
    price = i['price']['selling_price']
    doelgroep = i['properties']['doelgroep']
    productdetail = [name, brand, price]

