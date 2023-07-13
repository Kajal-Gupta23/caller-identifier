from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class MarkSpamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        spam_likelihood = float(request.data.get('spam_likelihood', 0))

        contact = get_object_or_404(Contact, phone_number=phone_number)
        contact.spam_likelihood = spam_likelihood
        contact.save()

        return Response(status=status.HTTP_200_OK)

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query')

        # Searching by name
        name_results = Contact.objects.filter(
            Q(name__startswith=query) | Q(name__contains=query)
        ).exclude(user=request.user)

        # Searching by phone number
        phone_results = Contact.objects.filter(
            phone_number=query
        ).exclude(user=request.user)

        name_serializer = ContactSerializer(name_results, many=True)
        phone_serializer = ContactSerializer(phone_results, many=True)

        return Response({
            'name_results': name_serializer.data,
            'phone_results': phone_serializer.data
        }, status=status.HTTP_200_OK)
