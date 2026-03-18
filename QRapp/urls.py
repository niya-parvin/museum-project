from django.urls import path
from . import views  # Corrected import statement
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('admin_home/', views.admin_home, name='admin_home'),  # Admin dashboard
    # path('about/about-us/', views.about_us, name='about_us'),
    # path('about/objectives/', views.objectives, name='objectives'),
    # path('about/vision/', views.vision, name='vision'),
    # path('about/mission/', views.mission, name='mission'),
    # path('institution/', views.institution, name='institution'),
    # path('institution/thiruvananthapuram/', views.thiruvananthapuram, name='thiruvananthapuram'),
    # path('institution/thrissur/', views.thrissur, name='thrissur'),
    # path('institution/kozhikode/', views.kozhikode, name='kozhikode'),
    # path('institution/kannur/', views.kannur, name='kannur'),
    # path('institution/wayanad/', views.wayanad, name='wayanad'),
    # path('notice/', views.notice, name='notice'),
    # path('notice/govt-orders/', views.govt_orders, name='govt_orders'),
    # path('notice/rti/', views.rti, name='rti'),
    # path('notice/tenders/', views.tenders, name='tenders'),
    # path('rentals/', views.rentals, name='rentals'),
    # path('rentals/thiruvananthapuram/', views.rentals_thiruvananthapuram, name='rentals_thiruvananthapuram'),
    # path('rentals/kozhikode/', views.rentals_kozhikode, name='rentals_kozhikode'),
    # path('visit-us/', views.visit_us, name='visit_us'),
    # path('gallery/', views.gallery, name='gallery'),
    # path('gallery/photo-gallery/', views.photo_gallery, name='photo_gallery'),
    # path('gallery/video-gallery/', views.video_gallery, name='video_gallery'),
    path('contact/', views.contact, name='contact'),
    path('contact/directorate-office/', views.directorate_office, name='directorate_office'),
    path('contact/feedback/', views.feedback, name='feedback'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),  # Corrected to reference logout_view
    path('add_category/', views.add_category, name='add_category'),
    path('list_category/', views.list_category, name='list_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_exhibit/', views.admin_add_exhibit, name='add_exhibit'),
    path('edit_exhibit/<int:exhibit_id>/', views.edit_exhibit, name='edit_exhibits'),
    path('delete_exhibit/<int:exhibit_id>/', views.delete_exhibit, name='delete_exhibit'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('list_exhibits/', views.list_exhibits, name='list_exhibits'),
    path('exhibit/<int:id>/', views.view_exhibit, name='view_exhibit'),  # URL for viewing an exhibit
    path('qr_code_scanner/', views.qr_code_scanner, name='qr_code_scanner'),# This links the scanner page view
    path('admin_add_event/', views.admin_add_event, name='admin_add_event'),# add event
    path('events_list/', views.event_list, name='event_list'),#  user List events
    path('admin_edit-event/<int:event_id>/', views.admin_edit_event, name='admin_edit_event'),
    path('admin_view_event/<int:event_id>/', views.admin_view_event, name='admin_view_event'),
    path('admin_events/', views.admin_event_list, name='admin_event_list'),  # Redirect after cancel/update
    path('admin_delete_event/<int:event_id>/', views.admin_delete_event, name='admin_delete_event'),  # Added this line
    path('admin_event_applications/', views.admin_event_applications, name='admin_event_applications'),
    path('success/', views.success, name='success'),
    path('apply_for_event/<int:event_id>/', views.apply_for_event, name='apply_for_event'),
    path('user_view_exhibit/<int:id>/', views.user_view_exhibit, name='user_view_exhibit'), 

    

]