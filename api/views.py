# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from  .seriliazers import UserSerializer 
# from  .models import User


# @api_view(['GET'])

# def getRoutes(request):
#         routes = [
#             {
#                 'Endpoint': '/SchoolApp',
#                 'method' : 'GET',
#                 'body' : None,
#                 'description' : 'Returns an array of SchoolApp'
#             }, 
#             {
#                 'Endpoint': '/SchoolApp/id',
#                 'method' : 'GET',
#                 'body' : None,
#                 'description' : 'Returns a single SchoolApp object'
#             },
#             {
#                 'Endpoint': '/SchoolAppcreate/',
#                 'method' : 'POST',
#                 'body' : {'body': ""},
#                 'description' : 'creates a  SchoolApp with data sent in POST request'
#             }, 
#             {
#                 'Endpoint': '/SchoolApp/id/update/',
#                 'method' : 'PUT',
#                 'body' : {'body': ""},
#                 'description' : 'updates an existing  SchoolApp with data sent in POST request'
#             },  
#             {
#                 'Endpoint': '/SchoolApp/id/delete/',
#                 'method' : 'DELETE',
#                 'body' : None,
#                 'description' : 'Deletes and exite SchoolApp'
#             },  
            
#         ]
        
#         return Response(routes)
# @api_view(['GET'])
# def getUser(request):
#         users =  User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

# @api_view(['GET']) 
# def getUserDetails(request, pk):
#         users =  User.objects.get(id=pk)
#         serializer = UserSerializer(users, many=False)
#         return Response(serializer.data)
  
# @api_view(['POST'])
# def createUser(request):
#         data = request.data
#         users = User.objects.create(
#                 user_name =  data['user_name'],
#                 user_surname = data['user_surname'],
#                 email = data['email'],
#                 telephone = data['telephone'],
#                 password = data['password'] 
#         )
#         serializer = UserSerializer(users, many= False)
#         return Response(serializer.data)

# @api_view(['PUT'])
# def updateUser(request, pk):
#         data = request.data

#         users = User.objects.get(id=pk)
#         serializer = UserSerializer(users, data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#         return Response(serializer.data)

# @api_view(['DELETE'])
# def deleteUser(request, pk):
#        users = User.objects.get(id=pk)
#        users.delete()

#        return Response('User  was deleted!')
# # Create your views here.

