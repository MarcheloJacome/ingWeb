from django.urls import path
from .views import  (
    TestListView,
    test_view,
    test_data_view,
    save_test_view
)

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name = 'main-view'),
    path('<pk>/<pk2>/', test_view, name='test-view'),
    path('<pk>/<pk2>/save/', save_test_view, name='save-view'),
    path('<pk>/<pk2>/data/', test_data_view, name='test-data-view')
]
