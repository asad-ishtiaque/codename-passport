from django.shortcuts import render
from passport.core.views import BaseDocumentViewSet
from passport.driving_license.models import DrivingLicense
from passport.driving_license.serializer import DrivingLicenseSerializer

class DrivingLicenseView(BaseDocumentViewSet):
    model = DrivingLicense
    serializer_class = DrivingLicenseSerializer