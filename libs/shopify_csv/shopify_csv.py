import os
import csv
from .shopify_row import ShopifyRow

class ShopifyCsv:
    
    def __init__(self):
        self.create_output_file()
        
    def create_output_file(self):
        
        # Check if the file already exists
        if not os.path.exists('spf_products.csv'):

            # If the file doesn't exist, create a new CSV file
            with open('spf_products.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(ShopifyRow.FIELDS)  # write header

    def get_shopify_row(self, product, index, is_row_image = False):
        return_rows = []
        # not need insert header field in here
        # return_rows.append(ShopifyRow.FIELDS)
        if not is_row_image:
            if(index == 1):
                row = ShopifyRow()
                row.handle = product['handle']
                row.title = product['title']
                row.vendor = "Vendor"
                
                if product['type']:
                    row.type = product['type']
                    
                if product['tags']:
                    row.tags = product['tags']
                    
                row.published = True
                row.option1_name = product['option1_name'] if 'option1_name' in product else 'Title'
                row.option1_value = product['option1_value'] if 'option1_value' in product else 'Default Title'

                if 'option2_name' in product:
                    row.option2_name = product['option2_name']
                    row.option2_value = product['option2_value']
                else:
                    row.option2_name = ''
                    row.option2_value = ''
                    
                if 'option3_name' in product:
                    row.option3_name = product['option3_name']
                    row.option3_value = product['option3_value']
                else:
                    row.option3_name = ''
                    row.option3_value = ''

                row.variant_grams = 0
                row.variant_weight_unit = 'kg'
                row.variant_inventory_policy = "deny"
                row.variant_inventory_qty = 999
                row.variant_fulfillment_service = "manual"
                row.variant_price = product['variant_price']
                # row.variant_compare_at_price = 34.99
                row.variant_requires_shipping = True
                row.variant_taxable = True
                if 'image_src' in product:
                    row.image_src = product['image_src']
                    row.image_position = product['image_position']
                    row.image_alt_text = product['image_alt_text']
                row.gift_card = False
                row.seo_title = ""
                row.seo_description = ""
                row.google_shopping_google_product_category = ""
                row.google_shopping_gender = ""
                row.google_shopping_age_group = ""
                row.google_shopping_mpn = ""
                row.google_shopping_adwords_grouping = ""
                row.google_shopping_adwords_labels = ""
                row.google_shopping_condition = ""
                row.google_shopping_custom_product = ""
                row.variant_weight_unit = ""
                if 'variant_image' in product:
                    row.variant_image = product['variant_image']
                row.status = "active"
                # row.validate_required_fields()
                return_rows.append(row.writable)

            if (index > 1):
                row = ShopifyRow()
                row.handle = product['handle']
                row.option1_name = product['option1_name'] or 'Title'
                row.option1_value = product['option1_value'] or 'Default Title'
                
                if 'option2_name' in product:
                    row.option2_name = product['option2_name']
                    row.option2_value = product['option2_value']
                else:
                    row.option2_name = ''
                    row.option2_value = ''
                    
                if 'option3_name' in product:
                    row.option3_name = product['option3_name']
                    row.option3_value = product['option3_value']
                else:
                    row.option3_name = ''
                    row.option3_value = ''

                row.variant_inventory_policy = "deny"
                row.variant_inventory_qty = 999
                row.variant_fulfillment_service = "manual"
                row.variant_price = product['variant_price']
                # row.variant_compare_at_price = 34.99
                if 'image_src' in product:
                    row.image_src = product['image_src']
                    row.image_position = product['image_position']
                    row.image_alt_text = product['image_alt_text']
                row.status = "active"
                if 'variant_image' in product:
                    row.variant_image = product['variant_image']
                # row.validate_required_fields(is_variant=True)
                return_rows.append(row.writable)
        
        else:
            row = ShopifyRow()
            row.handle = product['handle']
            if 'image_src' in product:
                row.image_src = product['image_src']
                row.image_position = product['image_position']
                row.image_alt_text = product['image_alt_text']
            
            # row.validate_required_fields()
            return_rows.append(row.writable)
        return return_rows


