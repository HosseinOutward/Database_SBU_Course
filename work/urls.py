from django.urls import path
from .views import *

urlpatterns = [
    # path('patient/', PatientListView.as_view(), name='user-patients-list'),
    # path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    # path('patient/<int:pk>/<int:image_id>/', PatientDetailView.as_view(), name='patient-detail-ID'),
    #
    # path('patient/new/', PatientCreateView.as_view(), name='patient-create'),
    # path('patient/<int:pk>/update/', PatientUpdateView.as_view(), name='patient-update'),
    #
    # path('patient/<int:patient_id>/imageAdd/', Panel.as_view(), name='image-add'),
    path('work_list/', WorkList.as_view(), name='work-list'),

    path('work_detail/<int:pk>', WorkDetail.as_view(), name='work-detail'),
    path('work_delete/<int:pk>/', WorkDelete.as_view(), name='work-delete'),
    path('panel/', PanelClient.as_view(), name='base-panel'),
]
