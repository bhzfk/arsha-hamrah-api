from shop_api.models import User, UserMeta
from django.contrib.auth.hashers import make_password, check_password

from shop_api.repositories.sms_repo import SMSRepository
import random
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import get_user_model
User = get_user_model()
class UserRepository:
    def register_user_account(self,obj):
        
        if  obj['username'] is None or obj['first_name'] is None or obj['last_name'] is None or obj['password'] is None or obj['nationalid'] is None:
            return {"success":False,"message":"اطلاعات ناقص است"}
        
        if self.is_username_has(obj['username']):
            return {"success":False,"message":"نام کاربری تکراری است"}
        
        
        nuser = User(username=obj['username'],first_name=obj['first_name'],last_name=obj['last_name'],password=make_password(obj['password']),is_active=1)
        nuser.save()
        puser = self.get_by_username(nuser)
        rand = random.randint(11111, 99999)
        id = puser['id']
        # self.add_meta(id,"active_code",f"{rand}")
        self.add_meta(id,"nationalid",f"{obj['nationalid']}")
        # SMSRepository().send_sms(obj['username'],f"کد فعالسازی شما : {rand}")
        # suser =  authenticate(username=obj['username'], password=obj['password'])
        # print(suser)
        user = User.objects.get(id=id)

        token, created = Token.objects.get_or_create(user=user)

        return {"success":True,"token":token.key}
        # return {"success":True}
    def update_user(self,user_id,obj):
        user = User.objects.get(id=user_id) 
        # for item in obj.keys():
        #     print(item)
        #     print((not user[item] is None))
        #     if not user[item] is None:
        #         user[item]  = obj[item]
        # user.save()
        some_dict = {
            'first_name': obj['first_name'],
            'last_name': obj['last_name'],
        }

        User.objects.filter(pk=user_id).update(**some_dict)
    
    def is_username_has(self,username):
        users = User.objects.filter(username=username).values()
        return users.count()>0
    
    def get_by_username(self,username):
        users = User.objects.filter(username=username).values()
        if users.count()>0:
            return users[0]
        return None
    
    def add_meta(self,user_id,meta_key,meta_value):
     
        umetas = UserMeta.objects.filter(user_id=user_id).filter(meta_key=meta_key)
        if umetas.count()==0 :
            umeta = UserMeta(user_id=user_id,meta_key=meta_key,meta_value=meta_value)
            umeta.save()
        else:
            umeta = umetas[0]
            umeta.meta_value = meta_value
            umeta.save()
    def get_meta(self,user_id,meta_key):
       
        umetas = UserMeta.objects.filter(user_id=user_id).filter(meta_key=meta_key)
        if umetas.count()==0 :
            return None
        else:
            umeta = umetas[0]
            return  umeta.meta_value
    
    
    
    def resend_acode_for_user_account(self,obj):
    
        if  obj['username'] is None:
            return {"success":False,"message":"اطلاعات ناقص است"}
        
        
        if self.is_username_has(obj['username'])==False:
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
        
        puser = self.get_by_username(obj['username'])
        rand = random.randint(11111, 99999)
        id = puser['id']
        self.add_meta(id,"active_code",f"{rand}")
        SMSRepository().send_sms(obj['username'],f"کد فعالسازی شما : {rand}")
        


        return {"success":True}
    
    
    
    def login_with_password_user_account(self,obj):
        
        if  obj['username'] is None  or obj['password'] is None :
            return {"success":False,"message":"اطلاعات ناقص است"}
        
        if self.is_username_has(obj['username'])==False:
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
        
        
      
        puser = self.get_by_username(obj['username'])
        is_valid = check_password(obj['password'], puser['password'])
        if is_valid :
            id = puser['id']
            user = User.objects.get(id=id)
            token, created = Token.objects.get_or_create(user=user)
            return {"success":True,"token":token.key}
        else:
            
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
       

        
    def login_with_acode_user_account(self,obj):
        
        if  obj['username'] is None  :
            return {"success":False,"message":"اطلاعات ناقص است"}
        
        if self.is_username_has(obj['username'])==False:
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
        
        
        puser = self.get_by_username(obj['username'])
        rand = random.randint(11111, 99999)
        id = puser['id']
        self.add_meta(id,"active_code",f"{rand}")
        SMSRepository().send_sms(obj['username'],f"کد فعالسازی شما : {rand}")
       
       

        return {"success":True}
    
    
    
    def check_acode_user_account(self,obj):
    
        if  obj['username'] is None  or obj['acode'] is None :
            return {"success":False,"message":"اطلاعات ناقص است"}
        
        if self.is_username_has(obj['username'])==False:
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
        
        
        
        puser = self.get_by_username(obj['username'])
        id = puser['id']
        acode_value = self.get_meta(id,"active_code")
        
        is_valid= (acode_value==obj['acode'])
        
        if is_valid :
            
            user = User.objects.get(id=id)
            token, created = Token.objects.get_or_create(user=user)
            return {"success":True,"token":token.key}
        else:
            
            return {"success":False,"message":"نام کاربری یا کلمه عبور اشتباه است"}
    
    
    def is_token_valid(token_key):
        try:
            # Try to get the token object from the database
            token = Token.objects.get(key=token_key)
            return True  # Token exists and is valid
        except ObjectDoesNotExist:
            return False  # Token does not exist or is invalid
        
    def get_user_by_request_token(self,request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Token "):
            token_key = auth_header.split(" ")[1]
            try:
            # Fetch the token object
                token = Token.objects.get(key=token_key)
            # Return the associated user
                user= self.get_by_username(token.user)
                user=self.attach_meta_to_user(user)
                print("********************************")
                print(user)
                del user['password']
                del user['is_active']
                del user['is_staff']
                del user['is_superuser']

                print(user)
                return user
            except Token.DoesNotExist:
                return None
        return None
    
    def attach_meta_to_user(self,user):
        
        umetas = UserMeta.objects.filter(user_id=user['id']).values()
        print("********************************")
        print(user['id'])
        print(umetas)
        if umetas.count()==0 :
            return user
        
        for item in umetas:
            user[item['meta_key']]=item['meta_value'] 
            
        
        return user
            
        