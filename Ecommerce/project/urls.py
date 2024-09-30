from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    # path('login/',views.login,name='login'),
    path('cart/',views.cart,name='cart'),
    # path('signup/',views.signup,name='signup'),
    path('checkout/',views.checkout,name='checkout'),
    
]
