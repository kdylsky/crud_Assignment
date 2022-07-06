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
    # def get(self, request):
    #     for owner in owners:
    #         dogs = Dog.objects.filter(owner_id=owner.id)
    #         pet_list = []
    #         for dog in dogs:
    #             pet_list.append(
    #                 {
    #                     "pet_name": dog.name,
    #                     "pet_age": dog.age,
    #                     "pet_owner": dog.owner.name,
    #                     "pet_owner_id": dog.owner_id
    #                 }
    #             )
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



    # 방법2
    # pet_list 위치 주의
    # 밖에 위치하면 계속해서 축적되서 데이터가 들어가기 때문에 새로운 for문을 들어가기 전에 초기화 해주어야 한다.
    def get(self, request):
        dogs = Dog.objects.all()
        owners = Owner.objects.all()
        result = []

        for owner in owners:
            pet_list = []
            for dog in dogs:
                if owner.id == dog.owner_id:
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