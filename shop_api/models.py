from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Setting(models.Model):
    name  = models.CharField(max_length=255, verbose_name="عنوان")
    val  = models.TextField(null=True, verbose_name="مقدار")
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "sob_settings"



class ProductCatalogCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description  = models.TextField(null=True)
    Parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,null=True,verbose_name="دسته",related_name="categories")
    type = models.IntegerField(default=1)
    sob_type = models.IntegerField(default=1)
    image  = models.TextField(null=True)
    image_icon  = models.TextField(null=True)
    image_menu  = models.TextField(null=True)
    image_app  = models.TextField(null=True)
    image  = models.TextField(null=True)
    show_type   = models.CharField(max_length=255,null=True)
    show_on_mobile = models.IntegerField(default=0)
    page_id  = models.IntegerField(null=True)
    position  = models.IntegerField(null=True)

    
    
    
    
    active = models.IntegerField(default=1)
    params  = models.TextField(null=True)
    deleted_at  = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "product_catalog_categories"

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in ProductCatalogCategory.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r


class ProductCatalog(models.Model):
    user_id = models.IntegerField(default=0)
    code  = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=200, verbose_name="عنوان")
    en_title  = models.CharField(max_length=255,null=True)
    # _2en_title  = models.CharField(max_length=255,null=True)
    description  = models.TextField(null=True)
    brand_id = models.BigIntegerField(default=0)
    product_attribute  = models.TextField(null=True)
    type = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    is_special = models.IntegerField(default=0)
    out_of_sell = models.IntegerField(default=0)
    is_coming_soon = models.IntegerField(default=1)
    image  = models.TextField(null=True)
    params  = models.TextField(null=True)
    deleted_at  = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "product_catalogs"




class Product(models.Model):
    product_catalog_id = models.BigIntegerField(null=True)
    product_code = models.CharField(max_length=255,null=True)
    price = models.BigIntegerField(default=0)
    pre_price = models.BigIntegerField(default=0)
    discount = models.IntegerField(default=0)
    discount_expire_at   = models.DateTimeField( null=True)
    qty = models.BigIntegerField(default=0)
    color = models.CharField(max_length=255,null=True)
    color_name = models.CharField(max_length=255,null=True)
    color_name_en = models.CharField(max_length=255,null=True)
    warranty = models.CharField(max_length=255,null=True)
    wight = models.IntegerField(default=0)
    params  = models.TextField(null=False)
    good_id = models.BigIntegerField(null=True)
    goodsCode = models.CharField(max_length=255,null=True)
    typeCode = models.IntegerField(null=True)
    tafsiliID = models.IntegerField(null=True)
    good_info = models.TextField(null=True)
   
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "products"




class ProductCatalogCategoryRels(models.Model):
    category = models.ForeignKey(ProductCatalogCategory, on_delete=models.DO_NOTHING,related_name="category")

    product_catalog  = models.ForeignKey(ProductCatalog, on_delete=models.DO_NOTHING,related_name="product_catalog")
    created_at  = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "product_catalog_category_rels"
        
        
class Image(models.Model):
    imageable_type = models.CharField(max_length=255,null=False)
    imageable_id = models.BigIntegerField(null=False)
    src  = models.TextField(null=False)
    alt = models.CharField(max_length=255,null=True)
  
    created_at  = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "images"









class Brand(models.Model):
    title = models.CharField(max_length=255)
    description  = models.TextField(null=False)
    type = models.IntegerField(default=1)
    image   = models.TextField(null=True)
    params  = models.TextField(null=True)
   
    deleted_at   = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "brands"
    



class Slider(models.Model):
    title = models.CharField(max_length=255)
    src   = models.TextField(null=True)
    type = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    params  = models.TextField(null=False)
    cats  = models.TextField(null=True)
    image_mobile   = models.TextField(null=True)
    url   = models.TextField(null=True)
    active = models.IntegerField(default=1)
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "sliders"
    
    
    

class ProductCatalogCategoryAttribute(models.Model):
    attribute_group_id = models.IntegerField()
    product_catalog_category_id = models.IntegerField()
    title = models.CharField(max_length=255)
    type = models.IntegerField(default=1)
    image   = models.TextField(null=True)
    params  = models.TextField(null=False)
    position = models.IntegerField(default=0)
   
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "attributes"
    

class ProductCatalogCategoryAttributeGroup(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.TextField(null=True)
    params = models.TextField(null=True)
    position = models.IntegerField(default=0)
   
   
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)


   

    class Meta:
        db_table = "attribute_groups"




class ProductCatalogCategoryAttributeValue(models.Model):
    attribute_group_id  = models.IntegerField()
    attribute_id  = models.BigIntegerField()
    value = models.TextField()
   
   
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)

   

    class Meta:
        db_table = "attribute_values"
    
    
class ProductCatalogCategoryAttributeProductValue(models.Model):
    product_catalogs_id  = models.BigIntegerField()
    attribute_id  = models.BigIntegerField()
    value_id  = models.BigIntegerField()
   
   
   
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)


   

    class Meta:
        db_table = "attribute_value_products"







class Address(models.Model):
    user_id  = models.BigIntegerField()

    name  = models.CharField(max_length=255, verbose_name="عنوان")
    address  = models.TextField(null=True, verbose_name="مقدار")
    latitude  = models.DecimalField(null=True,decimal_places=2,max_digits=10)
    longitude  = models.DecimalField(null=True,decimal_places=2,max_digits=10)
    state  = models.BigIntegerField()
    city  = models.BigIntegerField()
    zip  = models.CharField(null=True,max_length=255)
    pelak  = models.CharField(null=True,max_length=255)
    vahed  = models.CharField(null=True,max_length=255)
    reciever_name  = models.CharField(null=True,max_length=255)
    reciever_mobile  = models.CharField(null=True,max_length=255)
    nat_id  = models.CharField(null=True,max_length=255)
   
    me_reciever   = models.IntegerField(default=0)
    is_delete   = models.IntegerField(default=0)
   
    
    deleted_at   = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)
   

    class Meta:
        db_table = "addresses"




class State(models.Model):
    post_id  = models.BigIntegerField(null=True)

    name  = models.CharField(max_length=255, verbose_name="عنوان")
  
    
    deleted_at   = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)
   

    class Meta:
        db_table = "states"





class City(models.Model):
    state_id  = models.BigIntegerField()
    post_id  = models.BigIntegerField(null=True)

    name  = models.CharField(max_length=255, verbose_name="عنوان")
  
    
    deleted_at   = models.DateTimeField(null=True)
    created_at   = models.DateTimeField(null=True)
    updated_at  = models.DateTimeField(null=True)
   

    class Meta:
        db_table = "cities"










class UserMeta(models.Model):
    user_id  = models.BigIntegerField()

    meta_key  = models.CharField(max_length=255, verbose_name="عنوان")
    meta_value  = models.TextField(null=True, verbose_name="مقدار")
    create_at   = models.DateTimeField(null=True)
    update_at  = models.DateTimeField(null=True)
   

    class Meta:
        db_table = "sob_user_meta"


class User(AbstractUser):
    pass
	# mobile = models.CharField(max_length=200,null=True, verbose_name="موبایل")