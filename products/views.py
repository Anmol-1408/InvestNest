from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, CommunityDiscussion, CommunityReply, Event
from .forms import ProductForm, InvestmentForm, CommunityDiscussionForm, CommunityReplyForm, EventForm
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .utils import get_zoom_access_token, create_zoom_meeting


from django.utils import timezone
import datetime

from django.http import JsonResponse

# Create your views here.

def landing(request):
	return render(request, 'products/landing.html')

from django.shortcuts import render
from .models import Product

def explore(request):
    category = request.GET.get('category')
    
    # Fetch all published products sorted by publication date
    if category:
        products = Product.objects.filter(is_published=True, category=category).order_by('-pub_date')
    else:
        products = Product.objects.filter(is_published=True).order_by('-pub_date')
    
    # Fetch featured products
    featured_products = Product.objects.filter(is_featured=True, is_published=True).order_by('-pub_date')

    # Create a combined list with featured products interspersed
    combined_products = []
    regular_count = 0
    featured_index = 0
    total_regular = products.count()
    
    # Get a list of regular products
    regular_products = list(products)

    for product in regular_products:
        combined_products.append(product)
        regular_count += 1

        # Add a featured product after every 2 regular products if available
        if regular_count % 2 == 0 and featured_index < featured_products.count():
            combined_products.append(featured_products[featured_index])
            featured_index += 1

    return render(request, 'products/explore.html', {'products': combined_products})

@login_required
def fetch_more_featured_products(request):
    # Get the next set of featured products
    featured_products = Product.objects.filter(is_featured=True, is_published=True)[:5]  # Adjust the slicing as needed
    products_data = []
    
    for product in featured_products:
        products_data.append({
            'id': product.id,
            'title': product.title,
            'summary': product.summary(),
            'icon_url': product.icon.url,
        })
        print(f"Product ID: {product.id}, Title: {product.title}, Summary: {product.summary()}")
    
    return JsonResponse({'featured_products': products_data})





def product(request, pk):
	product = Product.objects.get(pk=pk)
	return render(request, 'products/product.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)  # Don't save to the database yet
                product.developer = request.user.profile  # Assign the developer as the logged-in user's profile
                
                # If pub_date is required and not in the form, set it manually
                if not product.pub_date:
                    from django.utils import timezone
                    product.pub_date = timezone.now()

                product.save()  # Now save the product to the database
                return redirect('explore')  # Redirect after saving
            except Exception as e:
                print("Error saving product:", e)  # Debugging any potential save issues
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        form = ProductForm()
    
    return render(request, 'products/product_create.html', {'form': form})




@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_update.html', {'form': form})



@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)  
    if request.method == 'POST':
        product.delete()
        return redirect('explore')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


def comingsoon(request):
	products = Product.objects.all()
	return render(request, 'products/product_comingsoon.html', {'products': products})


@login_required
def invest_create(request):
    if request.user.profile.is_investor:  # Restrict investment to investors only
        if request.method == 'POST':
            form = InvestmentForm(request.POST)
            if form.is_valid():
                investment = form.save(commit=False)
                investment.investor = request.user.profile  # Assign logged-in user as investor
                investment.save()
                return redirect('explore')
        else:
            form = InvestmentForm()
        return render(request, 'products/invest_create.html', {'form': form})
    else:
        return HttpResponse("You must be an investor to make an investment.")
    



def community_discuss(request):
    discussions = CommunityDiscussion.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CommunityDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.created_by = request.user.profile
            discussion.save()
            return redirect('community_discuss')
    else:
        form = CommunityDiscussionForm()
    
    return render(request, 'products/community_discuss.html', {
        'discussions': discussions,
        'form': form
    })


def community_thread_detail(request, discussion_id):
    discussion = get_object_or_404(CommunityDiscussion, pk=discussion_id)
    replies = discussion.replies.all()
    
    if request.method == 'POST':
        reply_form = CommunityReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.discussion = discussion
            reply.replied_by = request.user.profile
            reply.save()
            return redirect('community_thread_detail', discussion_id=discussion.id)
    else:
        reply_form = CommunityReplyForm()

    return render(request, 'products/community_thread_detail.html', {
        'discussion': discussion,
        'replies': replies,
        'reply_form': reply_form
    })



from django.conf import settings

def zoom_login(request):
    zoom_oauth_url = (
        "https://zoom.us/oauth/authorize"
        f"?response_type=code&client_id={settings.ZOOM_CLIENT_ID}"
        f"&redirect_uri={settings.ZOOM_REDIRECT_URI}"
    )
    return redirect(zoom_oauth_url)

def zoom_callback(request):
    code = request.GET.get('code')
    token_data = get_zoom_access_token(code)
    
    # Save tokens in session (can be saved to the database if needed)
    request.session['zoom_access_token'] = token_data['access_token']
    request.session['zoom_refresh_token'] = token_data['refresh_token']

    # Redirect to event creation page
    return redirect('create_event')


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user.profile
            
            # Zoom integration
            zoom_access_token = request.session.get('zoom_access_token')
            if zoom_access_token:
                zoom_meeting = create_zoom_meeting(
                    zoom_access_token,
                    event.title,
                    event.date_time,
                    60  # Duration in minutes (customize as needed)
                )
                event.link = zoom_meeting['join_url']  # Zoom meeting link
                event.save()
            else:
                return redirect('zoom_login')  # Redirect to Zoom login if not authenticated
            
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'products/create_event.html', {'form': form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'products/event_detail.html', {'event': event})


def event_list(request):
    events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'products/event_list.html', {'events': events})