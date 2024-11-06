from tkinter.font import names
from .import views
from django.urls import path
from .views import *


urlpatterns = [

    # login register logout

    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:pk>/',Userdetails.as_view(),name='user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password-otp/', views.PassOTPVerificationView.as_view(), name='otp-verification'),



    path('category/',CategoryViewCreate.as_view(),name='category'),
    path('category/<int:pk>/', CategoryDeatils.as_view(), name='category-details'),
    path('products/', ProductViewSerializer.as_view(), name='products'),
    path('products/<int:pk>/', ProductDeatils.as_view(), name='productdetails'),
    path('order/',OrderViewCreate.as_view(),name='order'),
    path('order/<int:pk>/',OrderDeatils.as_view(),name='order-deatils'),

    path('add-to-cart/<int:user_id>/<int:product_id>/', views.AddToCartView.as_view(),name='cart-add-product'),
    path('view-cart/<int:user_id>/', views.UserCartView.as_view(), name='user_cart'),
    path('update-cart/<int:user_id>/<int:cart_item_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('delete-cart-item/<int:user_id>/<int:cart_item_id>/', views.DeleteCartItemView.as_view(),name='delete_cart_item'),
]