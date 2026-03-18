from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import*
import re
from django.utils.html import escape
from django.db.models import Q
from django.core.paginator import Paginator
import qrcode
from django.utils.translation import get_language
import os
from django.conf import settings
from .models import Exhibit, Category, Image 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from .models import Event, EventApplication
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import Event, EventApplication
# Your existing view functions here



def index(request):
    return render(request, 'index.html')

# Home page view
def admin_home(request):
    return render(request, 'admin_home.html')

# About page view
# def about(request):
#     return render(request, 'about.html')

# About Us page view
# def about_us(request):
#     return render(request, 'about_us.html')

# Objectives page view
# def objectives(request):
#     return render(request, 'objectives.html')

# Vision page view
# def vision(request):
#     return render(request, 'vision.html')

# Mission page view
# def mission(request):
#     return render(request, 'mission.html')

# Institution page view
# def institution(request):
#     return render(request, 'institution.html')

# Institution specific location pages
# def thiruvananthapuram(request):
#     return render(request, 'thiruvananthapuram.html')

def thrissur(request):
    return render(request, 'index.html')

# def kozhikode(request):
#     return render(request, 'kozhikode.html')

# def kannur(request):
#     return render(request, 'kannur.html')

# def wayanad(request):
#     return render(request, 'wayanad.html')

# Notice page view
# def notice(request):
#     return render(request, 'notice.html')

# Notice sub-pages
# def govt_orders(request):
#     return render(request, 'govt_orders.html')

# def rti(request):
#     return render(request, 'rti.html')

# def tenders(request):
#     return render(request, 'tenders.html')

# Rentals page view
# def rentals(request):
#     return render(request, 'rentals.html')

# Rentals sub-pages
# def rentals_thiruvananthapuram(request):
#     return render(request, 'rentals_thiruvananthapuram.html')

# def rentals_kozhikode(request):
#     return render(request, 'rentals_kozhikode.html')

# Visit Us page view
# def visit_us(request):
#     return render(request, 'visit_us.html')


# Gallery page view
# def gallery(request):
#     return render(request, 'gallery.html')

# Gallery sub-pages
# def photo_gallery(request):
#     return render(request, 'photo_gallery.html')

# def video_gallery(request):
#     return render(request, 'video_gallery.html')

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Contact sub-pages
def directorate_office(request):
    return render(request, 'directorate_office.html')

def feedback(request):
    return render(request, 'feedback.html')

def qr_code_scanner(request):
    return render(request, 'scanner.html')

def success(request):
    return render(request, 'success.html')

# Login page view

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')  
#         # Redirect to home after login
#         else:
#             messages.error(request, "Invalid username or password.")
#             return redirect('login')  
#         # Redirect back to the login page

#     return render(request, 'login.html')
  # Render the login page

# Admin login view
def admin_login(request):
    # Define multiple default admin credentials
    ADMIN_CREDENTIALS = {
        'Admin@12': '123admin',
        '#Museum25': '456museum',  # Add more username-password pairs here
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists and password matches
        if username in ADMIN_CREDENTIALS and password == ADMIN_CREDENTIALS[username]:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()

            login(request, user)
            return redirect('admin_home')  # Redirect to admin home page

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('admin_login')

    return render(request, 'login.html')


def admin_home(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('admin_login')
    
    events = Event.objects.all()  # Fetching all events
    return render(request, 'admin/admin_home.html', {'events': events})  # Passing events to template

# Log out view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('index')  # Redirect to the home page after logging out

# View for adding a category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')

        # Validate the input
        if category_name:
            # Check if the category already exists
            if Category.objects.filter(name=category_name).exists():
                return JsonResponse({'success': False, 'error': 'Category already exists.'})

            # Create a new category instance
            category = Category(name=category_name)
            category.save()  # Save the new category to the database

            # Return a JSON response with success message
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with error message
            return JsonResponse({'success': False, 'error': 'Please provide a valid category name.'})
    
    return render(request, 'admin/add_category.html')  # Render the form if it's a GET request

@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()  # Delete the category
    messages.success(request, 'Category deleted successfully!')
    return redirect('list_category')

# View to list all categories
def list_category(request):
    # Retrieve all categories from the database
    categories = Category.objects.all()
    
    # Render the category list template with the retrieved categories
    return render(request, 'admin/list_category.html', {'data': categories})

# View to edit a category
def edit_category(request, category_id):
    # Retrieve the category to be edited
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Get the updated category name and status from the form
        category_name = request.POST.get('name')
        category_description = request.POST.get('description')
        category_status = request.POST.get('status')
        category_image = request.FILES.get('image')  # Handle image upload

        # Validate the input
        if category_name:
            # Update the category details
            category.name = category_name
            category.description = category_description
            category.status = category_status
            
            if category_image:
                category.image = category_image  # Assuming you have an image field in your Category model

            category.save()  # Save the changes to the database

            # Add a success message
            messages.success(request, 'Category updated successfully!')
            return redirect('list_category')  # Redirect to the list of categories
        else:
            messages.error(request, 'Please provide a valid category name.')

    # Render the edit category form with the current category data
    return render(request, 'admin/edit_category.html', {'category': category})


def admin_add_exhibit(request):
    categories = Category.objects.all()

    def validate_image(image):
        """Validate image file size and type."""
        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if isinstance(image, InMemoryUploadedFile):
            if image.size > 5 * 1024 * 1024:  # Limit image size to 5MB
                raise ValidationError("Image file size should be under 5MB.")
            if image.content_type not in valid_image_types:
                raise ValidationError("Only JPEG, PNG, JPG, and GIF image types are allowed.")
        return image

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        name_ml = request.POST.get('name_ml')  # Malayalam Name
        description_ml = request.POST.get('description_ml')  # Malayalam Description
        date = request.POST.get('date')
        category_id = request.POST.get('category')
        status = request.POST.get('status')

        try:
            # Validate and parse the date
            date = datetime.strptime(date, '%Y-%m-%d').date()
            category = Category.objects.get(id=category_id)

            # Duplication prevention check for name + category
            if Exhibit.objects.filter(name=name, category=category).exists():
                return JsonResponse({'success': False, 'error': 'An exhibit with this name and category already exists.'})

            # Duplication prevention check for description
            if Exhibit.objects.filter(description=description).exists():
                return JsonResponse({'success': False, 'error': 'An exhibit with this description already exists.'})

            # Create the exhibit instance
            exhibit = Exhibit.objects.create(
                name=name,
                description=description,
                name_ml=name_ml,
                description_ml=description_ml,
                date=date,
                category=category,
                status=status
            )

            # Generate the exhibit URL for QR code
            base_url = "https://603zj39v-8001.inc1.devtunnels.ms"  # Replace with your actual base URL
            exhibit_url = f"{base_url}/user_view_exhibit/{exhibit.id}/"

            # Generate QR code for the newly created exhibit
            qr_code_url = generate_qr_code(exhibit_url, exhibit.id)

            # Save the QR code URL to the exhibit
            exhibit.qr_code_image = qr_code_url
            exhibit.save()

            # Handle multiple image uploads with captions and validation
            images = request.FILES.getlist('images')
            image_ids = []
            for i, img in enumerate(images):
                try:
                    validate_image(img)
                except ValidationError as e:
                    return JsonResponse({'success': False, 'error': f"Image validation failed: {e.message}"})

                caption_en = request.POST.get(f'caption_{i}_en', '')
                caption_ml = request.POST.get(f'caption_{i}_ml', '')
                new_image = Image.objects.create(
                    exhibit=exhibit,
                    image=img,
                    caption=caption_en,
                    caption_ml=caption_ml,
                    position=i
                )
                image_ids.append(new_image.id)

            exhibit.set_image_ids(image_ids)

            return JsonResponse({'success': True})

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format. It must be in YYYY-MM-DD format.'})
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid category selected.'})

    return render(request, 'admin/add_exhibits.html', {'categories': categories})




# List all exhibits with pagination

def list_exhibits(request):
    exhibits = Exhibit.objects.all()
    paginator = Paginator(exhibits, 10)  # Show 10 exhibits per page

    page_number = request.GET.get('page')
    exhibits_page = paginator.get_page(page_number)

    # Check the current language of the user
    current_language = get_language()

    # Pass the language to the template for conditional rendering
    return render(request, 'admin/list_exhibits.html', {'exhibits': exhibits_page, 'current_language': current_language})


def view_exhibit(request, id):
    # Get the exhibit object or return a 404 if not found
    exhibit = get_object_or_404(Exhibit, id=id)

    # Check if the user is trying to set a language preference
    if request.method == "POST":
        # Toggle language preference
        if request.session.get('language') == 'en':
            request.session['language'] = 'ml'  # Switch to Malayalam
        else:
            request.session['language'] = 'en'  # Switch to English
        request.session.modified = True  # Mark the session as modified

    # Fetch images in the correct order
    exhibit_images = exhibit.images.all()  # This will use the default ordering defined in the model

    # Render the exhibit detail template with the exhibit object
    return render(request, 'admin/view_exhibit.html', {
        'exhibit': exhibit,
        'exhibit_images': exhibit_images
    })



def edit_exhibit(request, exhibit_id):
    exhibit = get_object_or_404(Exhibit, pk=exhibit_id)
    categories = Category.objects.all()
    exhibit_images = Image.objects.filter(exhibit=exhibit).order_by('position')

    def validate_image(image):
        """Validate image file size and type."""
        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if isinstance(image, InMemoryUploadedFile):
            if image.size > 5 * 1024 * 1024:  # Limit image size to 5MB
                raise ValidationError("Image file size should be under 5MB.")
            if image.content_type not in valid_image_types:
                raise ValidationError("Only JPEG, PNG, JPG and GIF image types are allowed.")
        return image

    def check_duplicate_image(image):
        """Check if the image already exists in the database."""
        existing_images = Image.objects.filter(exhibit=exhibit, image=image)
        if existing_images.exists():
            raise ValidationError("This image has already been uploaded.")

    if request.method == 'POST':
        # Update exhibit details
        exhibit.name = request.POST.get('name')
        exhibit.name_ml = request.POST.get('name_ml')
        exhibit.description = request.POST.get('description')
        exhibit.description_ml = request.POST.get('description_ml')
        exhibit.date = request.POST.get('date')
        exhibit.category_id = request.POST.get('category')
        exhibit.status = request.POST.get('status')

        # Collect new image IDs
        new_image_ids = []

        # Handle new image uploads with validation
        if request.FILES.getlist('images'):
            # Validate each image
            for img in request.FILES.getlist('images'):
                try:
                    validate_image(img)  # Validate image size and type
                    check_duplicate_image(img)  # Check for duplicates
                except ValidationError as e:
                    messages.error(request, f"Image validation failed: {e.message}")
                    return render(request, 'admin/edit_exhibits.html', {
                        'exhibit': exhibit,
                        'categories': categories,
                        'exhibit_images': exhibit_images
                    })

            # Create new images after validation
            for index, img in enumerate(request.FILES.getlist('images')):
                new_image = Image.objects.create(exhibit=exhibit, image=img, position=len(exhibit_images) + index)

                # Get captions for the new images
                new_caption = request.POST.get(f'new_caption_eng_{index}', "").strip()
                new_caption_ml = request.POST.get(f'new_caption_ml_{index}', "").strip()

                # Save captions if provided
                if new_caption:
                    new_image.caption = new_caption
                if new_caption_ml:
                    new_image.caption_ml = new_caption_ml
                new_image.save()

                new_image_ids.append(new_image.id)

        # Update captions for existing images
        for image in exhibit_images:
            caption_field_name = f'caption_{image.id}'
            caption_ml_field_name = f'caption_ml_{image.id}'
            new_caption = request.POST.get(caption_field_name, "").strip()
            new_caption_ml = request.POST.get(caption_ml_field_name, "").strip()

            if new_caption:
                image.caption = new_caption
            if new_caption_ml:
                image.caption_ml = new_caption_ml
            image.save()

        exhibit.save()
        messages.success(request, 'Exhibit updated successfully.')

        # Redirect to a different page after successful update
        return redirect('list_exhibits')

    return render(request, 'admin/edit_exhibits.html', {
        'exhibit': exhibit,
        'categories': categories,
        'exhibit_images': exhibit_images
    })


def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, id=image_id)
        exhibit_id = image.exhibit.id  # Get the exhibit ID to redirect after deletion
        image.delete()
        return JsonResponse({'success': True, 'exhibit_id': exhibit_id})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# Delete an exhibit
def delete_exhibit(request, exhibit_id):
    exhibit = get_object_or_404(Exhibit, pk=exhibit_id)

    if request.method == 'POST':
        exhibit.delete()
        messages.success(request, 'Exhibit and its QR code deleted successfully.')
        return redirect('list_exhibits')

    return redirect('list_exhibits')


 # Import the correct Image model
def generate_qr_code(data, exhibit_id):
    # Create a QR code instance with the provided data (URL or exhibit ID)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Set the file path for saving the QR code image
    file_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f'exhibit_{exhibit_id}.png')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the image
    img.save(file_path)

    # Return the relative URL for the saved file
    return os.path.join('qr_codes', f'exhibit_{exhibit_id}.png')



def admin_add_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        event_duration = request.POST.get('event_duration')
        event_organizer = request.POST.get('event_organizer')
        event_location = request.POST.get('event_location')
        event_description = request.POST.get('event_description')
        event_image = request.FILES.get('event_image')

        try:
            event_time = datetime.strptime(event_time, '%H:%M').time() if event_time else None
            event_duration = timedelta(hours=float(event_duration)) if event_duration else None
        except ValueError as e:
            return JsonResponse({'success': False, 'error': 'Invalid time or duration format.'})

        duplicate_event = Event.objects.filter(
            name=event_name, event_date=event_date, event_time=event_time, location=event_location
        ).exists()

        if duplicate_event:
            return JsonResponse({'success': False, 'error': 'An event with similar details already exists.'})

        try:
            Event.objects.create(
                name=event_name,
                event_type=event_type,
                event_date=event_date,
                event_time=event_time,
                duration=event_duration,
                organizer=event_organizer,
                location=event_location,
                description=event_description,
                image=event_image,
                created_by=request.user
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'admin/admin_events.html')




def event_list(request):
    events = Event.objects.all()  # Fetch all events from the database
    no_events = not events.exists()  # Check if there are no events
    return render(request, 'event_user.html', {'events': events, 'no_events': no_events})

def index(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'index.html', {'events': events })# Pass events to the template


def admin_event_applications(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')

    applications = EventApplication.objects.all()
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)

    return render(request, 'admin/event_applications.html', {'applications': applications_page})



# Regex patterns for validation
PHONE_REGEX = re.compile(r'^\d{10}$')  # 10-digit phone number
EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')  # Standard email pattern

SCHOOL_KEYWORDS = ["school", "academy", "high school"]

def apply_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        user_type = request.POST.get('user_type', 'individual').strip()
        name = request.POST.get('name', '').strip()
        phone_no = request.POST.get('phone_no', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        members_count = request.POST.get('members', '').strip()

        # Validate required fields
        if not all([name, phone_no, email, address, members_count]):
            return JsonResponse({'success': False, 'error': 'Please fill in all fields.'})

        if not PHONE_REGEX.match(phone_no):
            return JsonResponse({'success': False, 'error': 'Invalid phone number. It must be 10 digits long.'})

        
        if not EMAIL_REGEX.match(email):
            return JsonResponse({'success': False, 'error': 'Invalid email format.'})

        # Convert members_count to integer
        try:
            members_count = int(members_count)
            if members_count < 1:
                raise ValueError("Number of members must be at least 1.")
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)})

         # Ensure user type is correct
        if user_type not in ["individual", "school", "academy", "high school"]:
            return JsonResponse({'success': False, 'error': 'Invalid user type selected.'})

        # Determine user type
        if user_type in ["school", "academy", "high school"]:  # Ensure it's an institution
            if members_count < 2:  # Institutions must have at least 2 members
                return JsonResponse({'success': False, 'error': 'Schools must have at least 2 members.'})
    
            school_name = name
            name = f"{school_name} - Students"
        else:
            if members_count > 1:  # Individual users can't register more than 1 person
                return JsonResponse({'success': False, 'error': 'Individual users cannot add multiple members.'})


        # Prevent duplicate applications
        if EventApplication.objects.filter(Q(event=event), Q(email=email) | Q(phone_no=phone_no)).exists():
            return JsonResponse({'success': False, 'error': 'You have already applied for this event.'})

        student_names, student_phones, student_classes = [], [], []

        # Validate and collect school member details
        if user_type in ["school", "academy", "high school"]:

            for i in range(1, members_count + 1):
                member_name = escape(request.POST.get(f'member_name_{i}', '').strip())
                member_phone = request.POST.get(f'member_phone_{i}', '').strip()
                member_class = escape(request.POST.get(f'member_class_{i}', '').strip())

                if member_phone and not PHONE_REGEX.match(member_phone):
                    return JsonResponse({'success': False, 'error': f'Invalid phone number for member {i}.'})

                if member_name and member_phone:
                    student_names.append(member_name)
                    student_phones.append(member_phone)
                    student_classes.append(member_class)

            # Ensure the correct number of members are added
            if len(student_names) != members_count:
                return JsonResponse({'success': False, 'error': f'Expected {members_count} members, but received {len(student_names)}.'})

        # Create application
        application = EventApplication.objects.create(
            event=event,
            name=name,
            phone_no=phone_no,
            email=email,
            address=address,
            members=members_count,
            applied_on=timezone.now(),
            user_type=user_type,
            student_names=",".join(student_names) if student_names else None,
            student_phones=",".join(student_phones) if student_phones else None,
            student_classes=",".join(student_classes) if student_classes else None
        )

        return JsonResponse({'success': True})

    return render(request, 'user_apply_event.html', {'event': event})

# View to list all events
def admin_event_list(request):
    if not request.user.is_authenticated:  # Ensure only logged-in admins access
        return redirect('login')  # Replace with your login URL name

    events = Event.objects.all().order_by('-event_date')  # Order by date, newest first
    return render(request, 'admin/event_list.html', {'events': events})

def admin_view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'admin/admin_view_event.html', {'event': event})



def admin_edit_event(request, event_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    # Retrieve the event object
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Update event fields with values from the form
        event.name = request.POST.get('event_name', event.name)
        event.event_type = request.POST.get('event_type', event.event_type)
        event.event_date = request.POST.get('event_date', event.event_date)
        event.description = request.POST.get('event_description', event.description)
        event.location = request.POST.get('event_location', event.location)

        # Handle the duration input field
        duration_input = request.POST.get('event_duration', '')
        if duration_input:
            try:
                duration_hours = float(duration_input)
                event.duration = timedelta(hours=duration_hours)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid duration format.'})

        # Update other fields
        event.event_time = request.POST.get('event_time', event.event_time)
        event.organizer = request.POST.get('event_organizer', event.organizer)

        # Check if a new image is uploaded, and if so, update the event image
        if 'event_image' in request.FILES and request.FILES['event_image']:
            event.image = request.FILES['event_image']  # Update the image if provided
        
        try:
            # Save the event to the database
            event.save()  # Ensure the changes are persisted in the database

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Event updated successfully!'})
        
        except ValidationError as ve:
            # Catch validation errors and send an error message
            return JsonResponse({'success': False, 'error': str(ve)})
        
        except Exception as e:
            # Catch any other exceptions (e.g., database issues)
            return JsonResponse({'success': False, 'error': str(e)})

    # If not a POST request, just render the edit page with current event data
    return render(request, 'admin/edit_event.html', {'event': event})




def admin_delete_event(request, event_id):
    if not request.user.is_authenticated:  # Ensure only logged-in admins can delete
        return redirect('login')

    event = get_object_or_404(Event, id=event_id)

    # Delete the image from storage before deleting the event
    if event.image:
        image_path = event.image.path  # Get the image file path
        if default_storage.exists(image_path):  # Check if the image exists in storage
            default_storage.delete(image_path)  # Delete the image

    event.delete()  # Now delete the event

    messages.success(request, "Event deleted successfully!")
    return redirect('admin_event_list')




def user_view_exhibit(request, id):
    # Get the exhibit object or return a 404 if not found
    exhibit = get_object_or_404(Exhibit, id=id)

    # Check if the user is trying to set a language preference
    if request.method == "POST":
        # Toggle language preference
        if request.session.get('language') == 'en':
            request.session['language'] = 'ml'  # Switch to Malayalam
        else:
            request.session['language'] = 'en'  # Switch to English
        request.session.modified = True  # Mark the session as modified

    # Render the exhibit detail template with the exhibit object
    return render(request, 'user_view_exhibit.html', {'exhibit': exhibit})
