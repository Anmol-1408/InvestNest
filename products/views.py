# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, CommunityDiscussion, CommunityReply, Event
from .forms import ProductForm, InvestmentForm, CommunityDiscussionForm, CommunityReplyForm, EventForm
from django.conf import settings
from .utils import get_zoom_access_token, create_zoom_meeting
from django.db.models import Q
from collections import Counter
from itertools import chain


# Landing Page
def landing(request):
    if request.user.is_authenticated:
        return redirect('explore')
    return render(request, 'products/landing.html')

def explore(request):
    query = request.GET.get('q', '')

    selected_tags = [tag.strip().lower() for tag in query.split(',') if tag.strip()]
    products = Product.objects.filter(is_published=True)

    if selected_tags:
        q_objects = Q()
        for tag in selected_tags:
            q_objects |= Q(tags__icontains=tag)
        products = products.filter(q_objects)

    products = products.order_by('-pub_date')


    # Insert featured products in between
    featured_products = Product.objects.filter(is_featured=True, is_published=True).order_by('-pub_date')
    combined_products = []
    regular_count = 0
    featured_index = 0

    for product in products:
        combined_products.append(product)
        regular_count += 1
        if regular_count % 2 == 0 and featured_index < featured_products.count():
            combined_products.append(featured_products[featured_index])
            featured_index += 1

    # 🔥 Get all tags from published products
    all_tags = list(chain.from_iterable([p.tag_list() for p in Product.objects.filter(is_published=True)]))
    tag_counts = Counter(all_tags)
    popular_tags = tag_counts.most_common(10)

    return render(request, 'products/explore.html', {
        'products': combined_products,
        'query': query,
        'popular_tags': popular_tags,
        'selected_tags': selected_tags,
        'featured_products': featured_products,
    })

# Fetch More Featured Products
@login_required
def fetch_more_featured_products(request):
    featured_products = Product.objects.filter(is_featured=True, is_published=True)[:5]
    products_data = [{'id': product.id, 'title': product.title, 'summary': product.summary(), 'icon_url': product.icon.url} for product in featured_products]
    return JsonResponse({'featured_products': products_data})

# Product Details
def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.goal > 0:
        funding_percentage = (product.funding / product.goal) * 100
    else:
        funding_percentage = 0  # Avoid division by zero if goal is zero or not set
    context = {
        'product': product,
        'funding_percentage': funding_percentage
    }
    return render(request, 'products/product.html', context)

# Product Creation
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.developer = request.user.profile
            product.pub_date = product.pub_date or timezone.now()
            product.save()
            return redirect('explore')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

# Product Update
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

# Product Delete
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('explore')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# Coming Soon Page
def comingsoon(request):
    query = request.GET.get('q')

    # Start with published products
    products = Product.objects.filter(is_published=False)

    # Filter by tags if search query exists
    if query:
        tag_list = [tag.strip().lower() for tag in query.split(',')]
        q_objects = Q()
        for tag in tag_list:
            q_objects |= Q(tags__icontains=tag)
        products = products.filter(q_objects)

    products = products.order_by('-pub_date')
    # 🔥 Get all tags from published products
    all_tags = list(chain.from_iterable([p.tag_list() for p in Product.objects.filter(is_published=True)]))
    tag_counts = Counter(all_tags)
    popular_tags = tag_counts.most_common(10)
    return render(request, 'products/product_comingsoon.html', {'products': products,
        'query': query,
        'popular_tags': popular_tags,})

# Investment Creation
@login_required
def invest_create(request):
    if not request.user.profile.is_investor:
        return HttpResponse("You must be an investor to make an investment.")
    product_id = request.GET.get('product')
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.investor = request.user.profile
            investment.save()
            return redirect('explore')
    else:
        form = InvestmentForm(initial={'product': product})  # Pre-fill the product in the form
    return render(request, 'products/invest_create.html', {'form': form})

# Community Discussion
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

    return render(request, 'products/community_discuss.html', {'discussions': discussions, 'form': form})

# Community Thread Detail
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

    return render(request, 'products/community_thread_detail.html', {'discussion': discussion, 'replies': replies, 'reply_form': reply_form})

# Zoom Login
def zoom_login(request):
    zoom_oauth_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={settings.ZOOM_CLIENT_ID}&redirect_uri={settings.ZOOM_REDIRECT_URI}"
    return redirect(zoom_oauth_url)

# Zoom Callback
def zoom_callback(request):
    code = request.GET.get('code')
    token_data = get_zoom_access_token(code)
    request.session['zoom_access_token'] = token_data['access_token']
    request.session['zoom_refresh_token'] = token_data['refresh_token']
    return redirect('create_event')

# Event Creation
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user.profile
            zoom_access_token = request.session.get('zoom_access_token')
            if zoom_access_token:
                zoom_meeting = create_zoom_meeting(zoom_access_token, event.title, event.date_time, 60)
                event.link = zoom_meeting['join_url']
                event.save()
            else:
                return redirect('zoom_login')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'products/create_event.html', {'form': form})

# Event Detail
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'products/event_detail.html', {'event': event})

# Event List
def event_list(request):
    events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'products/event_list.html', {'events': events})
