import random


from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import generics,status
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

# Create your views here.

class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')

        try:
            user = User.objects.get(email=email, mobile_number=mobile_number)

            if user.is_verified:
                return Response({'error': 'User with this email and mobile number is already verified.'},
                                status=status.HTTP_400_BAD_REQUEST)

            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            send_mail(
                'OTP Verification',
                f'Your new OTP is {otp}',
                'praveencodeedex@gmail.com',
                [user.email]
            )


            return Response({'message': 'A new OTP has been sent to your email. Please verify your OTP.'},
                            status=status.HTTP_200_OK)

        except User.DoesNotExist:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                otp = random.randint(100000, 999999)
                user.otp = otp
                user.save()

                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp}',
                    'praveencodeedex@gmail.com',
                    [user.email]
                )


                return Response({'message': 'OTP Sent successfully! Please verify your OTP.'},
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OTPVerifyView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.is_active = True
                    user.is_verified = True
                    user.otp = None
                    user.save()
                    return Response({'message': 'Email verified successfully! You can now log in.'},
                                    status=status.HTTP_200_OK)
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({'message': 'Logged in successfully!', 'user_id': user.id,'status':True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'logout successful',
            'status':'True'
        }
        return response


User = get_user_model()

class PasswordResetView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PasswordResetSerializer

    def post(self, request):
        email = request.data.get('email', None)
        user = User.objects.filter(email=email).first()

        if user:
            otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])

            user.otp_secret_key = otp
            user.save()

            email_subject = 'Password Reset OTP'
            email_body = f'Your OTP for password reset is: {otp}'
            to_email = [user.email]
            send_mail(email_subject, email_body, from_email=None, recipient_list=to_email)


            return Response({'detail': 'OTP sent successfully.','status':True}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not found.','status':False}, status=status.HTTP_404_NOT_FOUND)

class PassOTPVerificationView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PassOTPVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)
        otp = serializer.validated_data.get('otp', None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': f'User with email {email} not found.', 'status': False}, status=status.HTTP_404_NOT_FOUND)

        if not self.verify_otp(user.otp_secret_key, otp):
            return Response({'detail': 'Invalid OTP.', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

        user.otp_secret_key = None
        user.save()

        return Response({'detail': 'OTP verification successful. Proceed to reset password.', 'status': True}, status=status.HTTP_200_OK)

    def verify_otp(self, secret_key, otp):

        return secret_key == otp


class ChangePasswordView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        new_password = serializer.validated_data.get('new_password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': f'User with email {email} not found.', 'status': False}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.', 'status': True}, status=status.HTTP_200_OK)


class Usercreateview(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Userdetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDeatils(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSerializer(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductDeatils(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class OrderViewCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeatils(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

User = get_user_model()


class AddToCartView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, user_id, product_id):
        # Get the user object
        user = get_object_or_404(User, pk=user_id)

        # Get the product object
        product = get_object_or_404(Products, pk=product_id)

        # Get or create the user's active cart
        cart, created = Cart.objects.get_or_create(user=user, is_active=True)

        # Check if the product already exists in the user's cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # If the cart item exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        # Serialize the cart with the cart items
        serializer = CartSerializer(cart, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserCartView(APIView):
    def get(self, request, user_id):
        # Retrieve the cart items of the user
        cart_items = CartItem.objects.filter(cart__user_id=user_id)

        # Calculate the total price for each cart item and the total cart price
        total_cart_price = 0
        for cart_item in cart_items:
            total_cart_price += cart_item.total_price()  # Call the method to get the total price

        # Serialize the cart items with the total price
        serializer = CartItemSerializer(cart_items, context={'request': request}, many=True)

        # Add the total cart price to the response data
        response_data = {
            'message': 'Products Retrieved Successfully',
            'cart_items': serializer.data,
            'total_cart_price': total_cart_price
        }

        return Response(response_data, status=status.HTTP_200_OK)

class UpdateCartView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request, user_id, cart_item_id):
        # Retrieve the cart item by cart_item_id and user_id
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user_id=user_id)

        # Serialize the cart item with the incoming request data
        serializer = CartItemSerializer(cart_item, data=request.data)

        if serializer.is_valid():
            # Save the updated cart item
            serializer.save()

            response_data = {
                'message': 'Updated Cart Item Successfully',
                'status': True
            }

            return Response(response_data, status=status.HTTP_200_OK)

        # Return errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItemView(APIView):
    authentication_classes = []
    permission_classes = []
    def delete(self, request, user_id, cart_item_id):
        cart_item = get_object_or_404(Cart, pk=cart_item_id, user_id=user_id)
        cart_item.delete()
        cart_items = Cart.objects.filter(user_id=user_id)

        # Serialize the cart items with their associated product images

        response_data = {
            'message': 'Removed From Cart Successfully',
            'status': True
        }

        return Response(response_data, status=status.HTTP_200_OK)

