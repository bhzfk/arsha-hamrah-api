import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from shop_api.models import ProductCatalog,ProductCatalogCategory
from shop_api.repositories.address_repository import AddressRepositpry
from shop_api.repositories.brand_repository import BrandRepo
from shop_api.repositories.product_catalog_categories_repo import ProductCatalogCategoryRepo
from shop_api.repositories.product_cataloge_repositpry_repo import productCatalogeRepositpry
from shop_api.repositories.setting_repository import SettingRepo
from django.core import serializers

from shop_api.repositories.slider_repository_repo import SliderRepository
from shop_api.repositories.sms_repo import SMSRepository
from shop_api.repositories.user_repository import UserRepository

# Create your views here.




@permission_classes([AllowAny])
class GetHomeData(APIView):
	def get(self, request, format=None):
     	# using select_related()
		# queryset = ProductCatalogCategory.objects.filter('Parent','null').select_related('Parent').values()
		# queryset = ProductCatalogCategoryRepo().get_parent_categories()

		products = []
		return Response({'products': products}, status=status.HTTP_200_OK)
@permission_classes([AllowAny])
class GetMenuCategoriesData(APIView):
	def get(self, request, format=None):
		categories = ProductCatalogCategoryRepo().get_parent_categories_for_front_menu()

		return Response(categories, status=status.HTTP_200_OK)



class GetProducts(APIView):
	def get(self, request, format=None):
     	
		products = ProductCatalog.objects.values()
		return Response({'products': products}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class GetFrontSlides(APIView):
	def get(self, request, format=None):
     	
		slides = SliderRepository.get_front_list()
		return Response(slides, status=status.HTTP_200_OK)


@permission_classes([AllowAny])

class GetSetting(APIView):
	def get(self, request,name, format=None):
     	
		result = SettingRepo.get_setting_by_name(name)
		# result = SettingRepo.get_all_settings_dic()
		header = {
				'Content-Type': 'application/json; charset=utf-8'
			}
		return Response(result, headers=header, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class GetFrontSettings(APIView):
	def get(self, request, format=None):
     	
		result = SettingRepo.get_all_settings_dic()
		header = {
				'Content-Type': 'application/json; charset=utf-8'
			}
		return Response(result, headers=header, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class GetFrontSingleCategory(APIView):
	def get(self, request,slug, format=None):
     	
		result = ProductCatalogCategoryRepo().get_single_category_front_by_slug(slug=slug)
		header = {
				'Content-Type': 'application/json; charset=utf-8'
			}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class GetFrontAllCategories(APIView):
	def get(self, request, format=None):
		categories = ProductCatalogCategoryRepo().get_all_front_categories()

		return Response(categories, status=status.HTTP_200_OK)



@permission_classes([AllowAny])
class GetFrontAllBrands(APIView):
	def get(self, request, format=None):
		brands = BrandRepo().get_all()

		return Response(brands, status=status.HTTP_200_OK)







@permission_classes([AllowAny])
class GetFrontSingleProduct(APIView):
	def get(self, request,slug, format=None):
     	
		result = productCatalogeRepositpry().get_single_product_front_by_slug(slug=slug)
		header = {
				'Content-Type': 'application/json; charset=utf-8'
			}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)




@permission_classes([AllowAny])
class GetFrontProductsOfCategory(APIView):
	def post(self, request, format=None):
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = productCatalogeRepositpry().get_products_by_category_array(json_data)
		
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)





@permission_classes([AllowAny])
class CheckBasketPriceQTY(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = productCatalogeRepositpry().check_price_qty_of_products(json_data)
		
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)





@permission_classes([AllowAny])
class RegisterUser(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = UserRepository().register_user_account(json_data)
		# result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)



@permission_classes([AllowAny])
class ReSendAcodeUser(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = UserRepository().resend_acode_for_user_account(json_data)
		# result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)
@permission_classes([AllowAny])
class LoginWithPassword(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = UserRepository().login_with_password_user_account(json_data)
		# result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)
@permission_classes([AllowAny])
class LoginWithAcode(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = UserRepository().login_with_acode_user_account(json_data)
		# result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)


class CkeckToken(APIView):
	def get(self, request, format=None):
		result=[]

		return Response(result, status=status.HTTP_200_OK)





@permission_classes([AllowAny])
class CheckAcode(APIView):
	def post(self, request, format=None):
		
		print(request.body)
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		result = UserRepository().check_acode_user_account(json_data)
		# result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		if not result ==None :
			return Response(result, headers=header, status=status.HTTP_200_OK)
		else:
			return Response(result, headers=header, status=status.HTTP_404_NOT_FOUND)



class GetUserByToken(APIView):
	def get(self, request, format=None):
		result = UserRepository().get_user_by_request_token(request)
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		print(result)
		if not result ==None :
			return Response(result, headers=header,  status=status.HTTP_200_OK)
		else:
			return Response({},  status=status.HTTP_404_NOT_FOUND)



class AddUserMeta(APIView):
	def post(self, request, format=None):
		user = UserRepository().get_user_by_request_token(request)
		if user is None :
			return Response({},  status=status.HTTP_404_NOT_FOUND)

		json_data = json.loads(str(request.body, encoding='utf-8'))
		for item in json_data.keys():
			if item!="first_name" and item!="first_name":
				UserRepository().add_meta(user['id'],item,json_data[item])

		UserRepository().update_user(user['id'],json_data)


		result=UserRepository().get_user_by_request_token(request)
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		print(result)
		if not result ==None :
			return Response(result, headers=header,  status=status.HTTP_200_OK)
		else:
			return Response({},  status=status.HTTP_404_NOT_FOUND)





class GetUserAddresses(APIView):
	def get(self, request, format=None):
		

		result= AddressRepositpry().get_all_for_user_front(request)
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		print(result)
		if not result ==None :
			return Response(result, headers=header,  status=status.HTTP_200_OK)
		else:
			return Response({},  status=status.HTTP_404_NOT_FOUND)




class AddUserAddress(APIView):
	def post(self, request, format=None):
		

		json_data = json.loads(str(request.body, encoding='utf-8'))
  
		address= AddressRepositpry().add_front(request,json_data)
		if address is None:
			return Response({},  status=500)
		result= AddressRepositpry().get_all_for_user_front(request)
		if result is None:
			result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		print(result)
		if not result ==None :
			return Response(result, headers=header,  status=status.HTTP_200_OK)
		else:
			return Response({},  status=status.HTTP_404_NOT_FOUND)


class DeleteUserAddress(APIView):
	def post(self, request, format=None):
		
  
		user= UserRepository().get_user_by_request_token(request)
		if user is None :
			return None

		json_data = json.loads(str(request.body, encoding='utf-8'))
		address= AddressRepositpry().get_by_id(json_data['id'])
		if address is None or address['user_id'] != user['id']:
			return Response({},  status=500)
		dd= AddressRepositpry().delete_by_id(json_data['id'])
		if dd==False:
			return Response({},  status=500)
		result= AddressRepositpry().get_all_for_user_front(request)
		if result is None:
			result=[]
		header = {
			'Content-Type': 'application/json; charset=utf-8'
		}
		print(result)
		if not result ==None :
			return Response(result, headers=header,  status=status.HTTP_200_OK)
		else:
			return Response({},  status=status.HTTP_404_NOT_FOUND)





@permission_classes([AllowAny])
class SMSDD(APIView):
	def get(self, request, format=None):
		brands = SMSRepository().send_sms("","")

		return Response(brands, status=status.HTTP_200_OK)