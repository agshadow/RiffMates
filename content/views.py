# RiffMantes/content/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from content.forms import CommentForm, SeekingAdForm
from content.models import SeekingAd, MusicianBandChoice


def comment(request):
    if request.method == "GET":
        form = CommentForm()
    else:  # POST
        form = CommentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]

            message = f"""\
                Received comment form {name}\n\n
                {comment}
                """

            send_mail(
                "Received comment",
                message,
                "admin@example.com",
                ["admin@example.com"],
                fail_silently=False,
            )
            return redirect("comment_accepted")

    # Was a GET, or Form was not valid
    data = {
        "form": form,
    }

    return render(request, "comment.html", data)


def comment_accepted(request):
    data = {
        "content": """
            <h1> Comment Accepted </h1>
            <p> Thanks for submitting a comment to <i>RiffMates</i> </p>
            """
    }

    return render(request, "general.html", data)


def list_ads(request):
    data = {
        "seeking_musician": SeekingAd.objects.filter(
            seeking=MusicianBandChoice.MUSICIAN
        ),
        "seeking_band": SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND),
    }
    print(data)
    return render(request, "list_ads.html", data)


@login_required
def seeking_ad(request, ad_id=0):
    print("inside seeking_ad")
    if request.method == "GET":
        print("inside GET")
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            if request.user.is_staff:
                print(f"this user is a superuser:  {request.user.username}")
                ad = get_object_or_404(SeekingAd, id=ad_id)
            else:
                print(f"this is not a superuser: {request.user.username}")
                ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(instance=ad)
    else:  # POST
        print(f"inside POST - ad_id = {ad_id}")
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            if request.user.is_staff:
                ad = get_object_or_404(SeekingAd, id=ad_id)
            else:
                ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(request.POST, instance=ad)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()

            return redirect("list_ads")
    # Was a GET or Form was not valid:
    data = {
        "form": form,
    }

    return render(request, "seeking_ad.html", data)
