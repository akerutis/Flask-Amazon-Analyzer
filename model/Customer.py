class Customer:
    def __init__(self, order_id, merchant_id, purchase_date, last_updated_date,	order_status, shop,
                 channel,	order_channel,	url, ship_service_level, product_name,	sku, asin,
                 item_status,	quantity,	currency,	item_price,	item_tax,	shipping_price,	shipping_tax,	gift_wrap_price,
                 gift_wrap_tax,	item_promotion_discount,	ship_promotion_discount,	ship_city,	ship_state,	postal_code,
                 ship_country,	promotion_ids,	is_business_order,	purchase_order_number,	price_designation):
            self.order_id = order_id
            self.shop = shop
            self.merchant_id = merchant_id
            self.purchase_date = purchase_date
            self.last_updated_date = last_updated_date
            self.order_status = order_status
            self.channel = channel
            self.order_channel = order_channel
            self.url = url
            self.ship_service_level = ship_service_level
            self.product_name = product_name
            self.sku = sku
            self.asin = asin
            self.item_status = item_status
            self.quantity = quantity
            self.currency = currency
            self.item_price = item_price
            self.item_tax = item_tax
            self.shipping_price = shipping_price
            self.shipping_tax = shipping_tax
            self.gift_wrap_price = gift_wrap_price
            self.gift_wrap_tax = gift_wrap_tax
            self.item_promotion_discount = item_promotion_discount
            self.ship_promotion_discount = ship_promotion_discount
            self.ship_city = ship_city
            self.ship_state = ship_state
            self.postal_code = postal_code
            self.ship_country = ship_country
            self.promotion_ids = promotion_ids
            self.is_business_order = is_business_order
            self.purchase_order_number = purchase_order_number
            self.price_designation = price_designation


