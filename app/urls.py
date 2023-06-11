from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PassChangeFrom, PassResetForm, PassResetConfirmForm

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetails.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='remove_cart'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=PassChangeFrom, success_url='/passchangedone/'), name='passwordchange'),
    path('passchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passchangedone.html'), name='passchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=PassResetForm), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=PassResetConfirmForm), name='password_reset_confirm'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),
    path('search/', views.search_results, name='search_results')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
