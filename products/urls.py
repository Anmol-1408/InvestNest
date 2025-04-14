from django.urls import path
from . import views

urlpatterns = [
	path('', views.landing, name='landing'),
	
	path('explore/', views.explore, name='explore'),
    path('fetch-more-featured-products/', views.fetch_more_featured_products, name='fetch_more_featured_products'),
    
	path('product/<int:pk>/', views.product, name='product'),
	path('product/new/', views.product_create, name='product_create'),
	path('product/<int:pk>/edit/', views.product_update, name='product_update'),
	path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
	
	path('coming-soon/', views.comingsoon, name='comingsoon'),
	path('invest/new/', views.invest_create, name='invest_create'),
    

	
    path('community/discuss/', views.community_discuss, name='community_discuss'),
    path('community/thread/<int:discussion_id>/', views.community_thread_detail, name='community_thread_detail'),
    
	# path('events/create/', views.create_event, name='create_event'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    
	path('zoom/login/', views.zoom_login, name='zoom_login'),
    path('zoom/callback/', views.zoom_callback, name='zoom_callback'),
    path('events/create/', views.create_event, name='create_event'),

    
]