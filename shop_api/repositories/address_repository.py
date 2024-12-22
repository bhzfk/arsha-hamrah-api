from shop_api.models import Address
from shop_api.repositories.location_repositories import LocationRepositpry
from shop_api.repositories.user_repository import UserRepository


class AddressRepositpry:
    
    def add_front(self,request,obj):
        user= UserRepository().get_user_by_request_token(request)
        if user is None :
            return None



        if (obj['state'] is None or obj['city'] is None or obj['name'] is None 
            or obj['address'] is None or obj['zip'] is None 
            or obj['latitude'] is None  or obj['longitude'] is None or obj['reciever_name'] is None
            or obj['pelak'] is None or obj['reciever_mobile'] is None
            or obj['nat_id'] is None or obj['me_reciever'] is None
            ):
            return None
        
        
        vahed=''
        if not obj['vahed'] is None:
                vahed=obj['vahed']
             
        #check state
        state = LocationRepositpry().state_exist_by_name(obj['state'])
        if state is None :
            state = LocationRepositpry().add_state(obj['state'])
            
            
         #check city
        city = LocationRepositpry().city_exist_by_name_and_state(obj['city'],state['id'])
        if city is None :
            city = LocationRepositpry().add_state(obj['city'],state['id'])
        address = Address(user_id=user['id'],state=state['id'],city=city['id'],name=obj['name']
                          ,address=obj['address'],zip=obj['zip']
                          ,latitude=obj['latitude'],longitude=obj['longitude']
                          ,reciever_name=obj['reciever_name'],pelak=obj['pelak']
                          ,reciever_mobile=obj['reciever_mobile'],nat_id=obj['nat_id']
                          ,me_reciever=obj['me_reciever'],vahed=obj['vahed']
                          )
        address.save()
        return address
    
    
    def get_all_for_user_front(self,request):
        user= UserRepository().get_user_by_request_token(request)
        if user is None :
            return None
        addresses= Address.objects.filter(user_id=user['id']).filter(is_delete=0).values()
        
        for item in addresses:
            state = LocationRepositpry().get_state(item['state'])
            item['state_name']=state['name']
            city = LocationRepositpry().get_city(item['city'])
            item['city_name']=city['name']
        
        return addresses
    def get_by_id(self,id):
        addresses= Address.objects.filter(id=id).filter(is_delete=0).values()
        if addresses.count()==0:
            return None
        address = addresses[0]
        state = LocationRepositpry().get_state(address['state'])
        address['state_name']=state['name']
        city = LocationRepositpry().get_city(address['city'])
        address['city_name']=city['name']
            
        
        return address
    def delete_by_id(self,id):
    
       dic= {
           "is_delete":"1"
       } 
       address = Address.objects.filter(id=id).filter(is_delete=0).update(**dic)
       
            
        
       return True
        

