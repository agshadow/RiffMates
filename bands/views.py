from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from bands.models import Musician, Band
from collections import namedtuple


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


def bands(request):
    all_bands = Band.objects.all().order_by("name")
    for i in all_bands:
        print(i.name)
        print("all bands = ", i.musicians.all().order_by("last_name"))

    # set up paginator
    paginator = Paginator(all_bands, 5)  # 5 items per page

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

    data = {
        "bands": page.object_list,
        "page": page,
        "page_tracker": page_tracker,
    }
    print(data)
    return render(request, "bands.html", data)


def musicians(request):
    all_musicians = Musician.objects.all().order_by("last_name")
    paginator = Paginator(all_musicians, 5)  # 5 items per page

    page_num = request.GET.get("page", 1)  # defaults to 1 if none exist
    page_num = int(page_num)  # convert into integer

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    page_tracker = Page_tracker(page_num, paginator.num_pages)

    data = {
        "musicians": page.object_list,
        "page": page,
        "page_tracker": page_tracker,
    }
    print(data)
    print("musicians")

    return render(request, "musicians.html", data)
