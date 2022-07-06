import json

from django.http import JsonResponse
from django.views import View
# from django.shortcuts import render

from owners_app.models import Owner, Dog

# Create your views here.


class OwnerView(View):

    def post(self, request):
        data = json.loads(request.body)
        Owner.objects.create(name=data["name"], email=data["email"], age=data["age"] )

        return JsonResponse({"message":"owner enrolled"}, status=201)

    # 방법1
    def get(self, request):
        owners = Owner.objects.all()
        result = []
        for owner in owners:
            dogs = Dog.objects.filter(owner_id=owner.id)
            pet_list = []
            for dog in dogs:
                pet_list.append(
                    {
                        "pet_name": dog.name,
                        "pet_age": dog.age,
                        "pet_owner": dog.owner.name,
                        "pet_owner_id": dog.owner_id
                    }
                )

            result.append(
                {
                    "id": owner.id,
                    "name": owner.name,
                    "age": owner.age,
                    "email": owner.email,
                    "pet": pet_list,
                }
            )
        return JsonResponse({"result": result}, status=200)



    # 방법2
    # pet_list 위치 주의
    # 밖에 위치하면 계속해서 축적되서 데이터가 들어가기 때문에 새로운 for문을 들어가기 전에 초기화 해주어야 한다.
    # def get(self, request):
    #     # 역참조를 사용하지 않으면, 모든 데이터를 가지고와서 다시 한번 확인을 하는 코드가 필요하다.
    #     # 그렇기 때문에 맨 처음부터 관계가 있느 데이터만 가지고 오게 하느 것이 좋다.
    #     # 모든 정보를 가지고 오기 때문에 대량의 데이터가 있으면 부담이 된다.
    #     dogs = Dog.objects.all()
    #     owners = Owner.objects.all()
    #     result = []
    #     for owner in owners:
    #         pet_list = []
    #         # dogs = Dog.objects.filter(owner=owner)
    #
    #         for dog in dogs:
    #             if owner.id == dog.owner_id:
    #                 pet_list.append(
    #                     {
    #                         "pet_name": dog.name,
    #                         "pet_age": dog.age,
    #                         "pet_owner": dog.owner.name,
    #                         "pet_owner_id": dog.owner_id
    #                     }
    #                 )
    #
    #         result.append(
    #             {
    #                 "id": owner.id,
    #                 "name": owner.name,
    #                 "age": owner.age,
    #                 "email": owner.email,
    #                 "pet": pet_list,
    #             }
    #         )
    #
    #     return JsonResponse({"result": result}, status=200)


    #방법3
    # 역참조를 이용한 데이터 가지고 오기
    # 본래는 dog에서 주인에 대한 참조는 가능하나, 주인에서 dog에 대한 참조가 불가능하다.
    # 하지만 역참조를 활용해서 참조가 가능하다.

    # def get(self, response):
    #     owners = Owner.objects.all()
    #     result=[]
    #     for owner in owners:
    #         dog_list = []
    #         dogs = owner.dog_set.all()
    #
    #         for dog in dogs:
    #             dog_info={
    #                 "dog_name":dog.name,
    #                 "dog_age":dog.age,
    #                 "dog_owner":dog.owner.name
    #             }
    #         dog_list.append(dog_info)
    #
    #         owner_list={
    #             "owner_name":owner.name,
    #             "owner_age":owner.age,
    #             "owner_email":owner.email,
    #             "dot_list" : dog_list
    #         }
    #
    #         result.append(owner_list)
    #     return JsonResponse({"result" : result}, status=200)



class DogView(View):

    # 방법1 주인 이름으로 등록하기

    def post(self, request):
        data = json.loads(request.body)

        owner_name_list = []
        for temp_owner in list(Owner.objects.all()):
            owner_name_list.append(temp_owner.name)

        if data["owner"] in owner_name_list:
            owner = Owner.objects.get(name=data["owner"])

            Dog.objects.create(name=data["name"], age=data["age"], owner=owner)
            return JsonResponse({"message":"dog enrolled"}, status=201)

        elif data["owner"] not in owner_name_list:
            return JsonResponse({"message":"not enrolled owner"}, status=400)


    # 방법2 주인 번호롤 입력하기
    # def post(self, request):
    #     data = json.loads(request.body)
    #
    #     owner = Owner.objects.all()
    #     data_inner = int(data["owner"])
    #
    #     if data_inner > len(owner) - 1:
    #         return JsonResponse({"message": "주인이 없습니다"}, status=400)
    #     else:
    #         Dog.objects.create(name=data["name"], age=data["age"], owner=owner[int(data_inner)-1])
    #         return JsonResponse({"message": "enroll dogs"}, status=201)


    def get(self,request):
        dogs = Dog.objects.all()
        result = []

        for dog in dogs:
            result.append({
                "pet_name":dog.name,
                "pet_age": dog.age,
                "pet_id": dog.id,

            })

        return JsonResponse({"result":result}, status=200)