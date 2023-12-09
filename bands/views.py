from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from bands.models import Musician, Band, Venue, UserProfile
from collections import namedtuple
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404


Page_tracker = namedtuple("Page_tracker", ["current", "total"])


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    print(musician)
    data = {
        "musician": musician,
    }
    return render(request, "musician.html", data)


def band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    print(band)
    data = {
        "band": band,
    }
    print(data)
    return render(request, "band.html", data)


def venues(request):
    all_venues = Venue.objects.all().order_by("name")

    # set up paginator
    page_data = get_paginator(all_venues, request, 3)
    (page, page_tracker) = page_data

    # return data
    data = {
        "venues": page.object_list,
        "page": page,
        "page_tracker": page_tracker,
    }
    return render(request, "venues.html", data)


def venue_check(user):
    print("in venue_check")
    print(f"userid: {user.id}")
    print(f"userid: {user.get_username()}")
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("exception user profile not exist")
        return False
    # print(f"id: {profile.id}")
    # print(f"user_id: {profile.user_id}")
    # print(profile.venues_controlled.exists())

    try:
        if profile.venues_controlled.exists():
            print(f"Venue Check - User {profile.id} is allowed")
            return True
        else:
            # User is not this musician, check if they're a band-mate
            print(f"Venue Check - User {profile.id} not allowed")
            return False

    except UserProfile.DoesNotExist:
        print("exception user profile not exist")
        return False


@user_passes_test(venue_check)
def venues_restricted(request):
    return venues(request)


def bands(request):
    all_bands = Band.objects.all().order_by("name")

    # set up paginator
    page_data = get_paginator(all_bands, request, 3)
    (page, page_tracker) = page_data

    data = {
        "bands": page.object_list,
        "page": page,
        "page_tracker": page_tracker,
    }
    print(data)
    return render(request, "bands.html", data)


def musicians(request):
    all_musicians = Musician.objects.all().order_by("last_name")

    # set up paginator
    page_data = get_paginator(all_musicians, request, 3)
    (page, page_tracker) = page_data

    data = {
        "musicians": page.object_list,
        "page": page,
        "page_tracker": page_tracker,
    }
    return render(request, "musicians.html", data)


def get_paginator(all_objects, request, items_per_page):
    # set up paginator
    paginator = Paginator(all_objects, items_per_page)  # 5 items per page

    # take page number from request if it exists into page_num as a integer
    page_num = request.GET.get("page", 1)  # defaults to 1 if none exist
    page_num = int(page_num)  # convert into integer

    # do some validation
    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    # get the page from the pagnator
    page = paginator.page(page_num)
    page_tracker = Page_tracker(page_num, paginator.num_pages)
    return (page, page_tracker)


@login_required
def restricted_page(request):
    data = {
        "title": "Restricted Page",
        "content": "<h1>You are logged in</h1>",
    }

    return render(request, "general.html", data)


@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = request.user.userprofile
    allowed = False

    if profile.musician_profiles.filter(id=musician_id).exists():
        allowed = True
    else:
        # User is not this musician, check if they're a band-mate
        musician_profiles = set(profile.musician_profiles.all())
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if musician_profiles.intersection(band_musicians):
                allowed = True
                break
    if not allowed:
        raise Http404("Permission denied")
    content = f"""
        <h1>Musician Page: {musician.last_name}</h1>
        <p> <a href="/accounts/logout/">Logout</a> </p>
    """
    data = {
        "title": "Musician Restricted",
        "content": content,
    }
    return render(request, "general.html", data)
