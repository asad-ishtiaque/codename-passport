from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from passport.passport.views import PasspportViewSet
from passport.driving_license.views import DrivingLicenseViewSet
from passport.residence_permit.views import ResidencePermitViewSet
from passport.vehicle_inspection_certificate.views import VehicleInspectionCertificateViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'passports', PasspportViewSet, basename='passport')
router.register(r'driving-licenses', DrivingLicenseViewSet, basename='driving-license')
router.register(
    r'vehicle-inspection-certificates',
    VehicleInspectionCertificateViewSet,
    basename='vehicle-inspection-certificate'
)
router.register(
    r'residence-permits',
    ResidencePermitViewSet,
    basename='residence-permit'
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  #returns access + refresh token (pair)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
