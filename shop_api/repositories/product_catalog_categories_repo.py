from shop_api.models import Product, ProductCatalog, ProductCatalogCategory, ProductCatalogCategoryAttribute, ProductCatalogCategoryAttributeProductValue, ProductCatalogCategoryAttributeValue, ProductCatalogCategoryRels
from django.db.models import Sum,Min

class ProductCatalogCategoryRepo:
    def __init__(self):
        pass
    def get_parent_categories(self,loadChilds=True,loadProducts=False):
        temp = ProductCatalogCategory.objects.filter(Parent=None).order_by('position').values()
        if not loadChilds :
            return temp
        list=[]
        for item in temp :
            # print(item)
            item["cats"]= self.get_child_categories(item['id'],loadProducts=loadProducts)
            # item["products"]= self.get_products(item['id'])
        
        return temp
   

    
    def get_child_categories(self,parent_id,loadProducts=False):
        temp = ProductCatalogCategory.objects.filter(Parent=parent_id).values()
        for item in temp :
           
            item["cats"]= self.get_child_categories(item['id'],loadProducts=loadProducts)
            # item["products"]= self.get_products(item['id'])
        return temp
    
    
    def get_products(self,parent_id,showQtyZero=False):
        list=[]
        temp = ProductCatalogCategoryRels.objects.filter(category=parent_id).values()
        for item in temp :
            products= ProductCatalog.objects.filter(id=item['product_catalog_id']).filter(is_active=1).values()
            if products.count()>0:
                product=products[0]
                childs = Product.objects.filter(product_catalog_id=product['id'])
                product['qty']=childs.aggregate(qty=Sum('qty'))['qty']
                product['price']=childs.filter(price__gt=0).aggregate(price=Min('price'))['price']
                product["childs"] = childs.values()
                product["attrs"]=self.get_product_attributes(product['id'])
                if  (showQtyZero or (not product['qty'] is None and int(f'{product['qty']}',0)>0) ):
                    list.append(product)
        return list
    
    
    def get_product_attributes(self,product_id):
        attrs = ProductCatalogCategoryAttributeProductValue.objects.filter(product_catalogs_id=product_id)
        # for item in attrs:
        #     values= ProductCatalogCategoryAttributeValue.objects.filter(id=item.value_id)
        #     if values.count()>0 :
        #         item["value"]=values[0].value
        #     else:
        #         item["value"]="nulll"
        return attrs.values()
    
    def get_parent_categories_for_front_menu(self):
        temp = ProductCatalogCategory.objects.filter(Parent=None).order_by('position').values()
      
        list=[]
        for item in temp :
        # print(item)
            item["cats"]= self.get_child_categories_for_front_menu(item['id'])

        return temp
    
    def get_child_categories_for_front_menu(self,parent_id):
            temp = ProductCatalogCategory.objects.filter(Parent=parent_id).order_by('position').values()
            for item in temp :
            
                item["cats"]= self.get_child_categories_for_front_menu(item['id'])
                # item["products"]= self.get_products(item['id'])
            return temp
    def get_single_category_front_by_slug(self,slug):
        temp = ProductCatalogCategory.objects.filter(title=slug.replace("-"," ")).values()
        for item in temp:
            # item["products"]=self.get_products(item['id'],showQtyZero=True).sort(key=lambda x: 0 if x['qty'] is None  else   int(f'{x['qty']}',0))
            item["products"]=self.get_products(item['id'],showQtyZero=True)
            item["attrs"]=self.get_all_attributes_for_category(item['id'])
        if temp.count()>0:
            return temp[0]
        else:
            return None
       
    
    def sortProducts(e,z):
        return e['qty']
    def get_all_attributes_for_category(self,category_id):
        temp = ProductCatalogCategoryAttribute.objects.filter(product_catalog_category_id=category_id).filter(params__contains='{"for_filter":"1"}').order_by('position').values()
        for item in temp:
            item["values"]=self.get_all_values_attributes_for_category(item["id"])
        return temp
    def get_all_values_attributes_for_category(self,parent_id):
        temp = ProductCatalogCategoryAttributeValue.objects.filter(attribute_id=parent_id).values()
        return temp
       
    def get_all_front_categories(self):
        temp = ProductCatalogCategory.objects.order_by('position').values()
        
        
        return temp
    
    
 
    
  
        

        
            
