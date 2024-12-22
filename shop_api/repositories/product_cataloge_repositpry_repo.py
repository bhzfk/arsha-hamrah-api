from shop_api.models import Image, Product, ProductCatalog, ProductCatalogCategory, ProductCatalogCategoryAttribute, ProductCatalogCategoryAttributeGroup, ProductCatalogCategoryAttributeProductValue, ProductCatalogCategoryAttributeValue, ProductCatalogCategoryRels
from django.db.models import Sum,Min


class productCatalogeRepositpry:
    
    def get_single_product(product_id):
        pass
    
    def get_single_product_front_by_slug(self,slug):
        temp = ProductCatalog.objects.filter(title=slug.replace("-"," ")).values()
        
        
     
        if temp.count()>0:
            product = temp[0]
            images = Image.objects.filter(imageable_type='Modules\Shop\Entities\ProductCatalog').filter(imageable_id=product['id'])
            product["images"] = images.values()
            childs = Product.objects.filter(product_catalog_id=product['id']).filter(qty__gt=0)
            product["childs"] = childs.values()
            product["cats"] = self.get_categories_of_Product(product['id'])
            product["attr"] = self.get_attributes_of_Product(product['id'])
            return product
        else:
            return None
        
    def get_categories_of_Product(self,product_id):
        list=[]
        temp = ProductCatalogCategoryRels.objects.filter(product_catalog=product_id).values()
        for item in temp :
            categories = ProductCatalogCategory.objects.filter(id=item["category_id"]).values()
            if categories.count()>0:
                list.append(categories[0])
        
        return list
    
    
    
    def get_attributes_of_Product(self,product_id):
        list=[]
        group_list = []
        net_attr_list= ProductCatalogCategoryAttributeProductValue.objects.filter(product_catalogs_id=product_id).values()
        for item in net_attr_list :
          attr={"id":item['id'],"attribute_id":item['attribute_id']}
          self.get_attribute_withValue_of_atribute_Product(item,attr,group_list)
            
                     

        return group_list
    
    def get_attribute_withValue_of_atribute_Product(self,myItem,attr,group_list):
        values = ProductCatalogCategoryAttributeValue.objects.filter(id=myItem['value_id']).values()
        if not values == None and values.count()>0 : 
            value_item = values[0]
            attr["value"]=value_item["value"]
        attrs = ProductCatalogCategoryAttribute.objects.filter(id=myItem['attribute_id']).values()
        if not attrs == None and attrs.count()>0 : 
            attr_item = attrs[0]
            attr["title"]=attr_item["title"]
            self.get_group_attribute_of_atribute_Product(attr_item['attribute_group_id'],attr,group_list)
            # attr_item['attribute_group_id']
            
    def get_group_attribute_of_atribute_Product(self,group_id,attr,group_list):
        group_items = ProductCatalogCategoryAttributeGroup.objects.filter(id=group_id).values()
        if not group_items == None and group_items.count()>0 :
            group_item=group_items[0]
            group_exists =  list(x for x in group_list if x['id']==group_item['id'])
            if not group_exists == None and len(group_exists)>0 :
                group_exist = group_exists[0]
                if  group_exist['attr'] == None :
                    group_exist['attr']=[attr]
                else:
                    lst =[]
                    lst = group_exist['attr'] 
                    lst.append(attr)
                    group_exist['attr']=lst
            else:
                group_item['attr']=[attr]
                group_list.append(group_item)
        
        return group_list
    
    
    def get_products_by_category_array(self,arr):
        list=[]
        for cat in arr:
            
            temp = ProductCatalogCategoryRels.objects.filter(category=cat).values()
            for item in temp :
                products= ProductCatalog.objects.filter(id=item['product_catalog_id']).filter(is_active=1).values()
                if products.count()>0:
                    product=products[0]
                    childs = Product.objects.filter(product_catalog_id=product['id'])
                    product['qty']=childs.aggregate(qty=Sum('qty'))['qty']
                    product['price']=childs.filter(price__gt=0).aggregate(price=Min('price'))['price']
                    product["childs"] = childs.values()
                    # product["attrs"]=self.get_product_attributes(product['id'])
                    if  ((not product['qty'] is None and int(f'{product['qty']}',0)>0) ):
                        list.append(product)
        return list
    
    
    def check_price_qty_of_product(self,product_id):
        childs = Product.objects.filter(id=product_id).values()
        if childs.count()>0:
            return childs[0]
        else:
            return None
        
        
    def check_price_qty_of_products(self,product_ids):
        lst=[]
        for product_id in product_ids :
            product = self.check_price_qty_of_product(product_id)
            if not product==None:
                lst.append(product)
        
        return lst

                
            
    
    