from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required


def credits(request):
    content = "Nicky\nYour Name"

    return HttpResponse(content, content_type="text/plain")


def about(request):
    content = """<!DOCTYPE html>
            <html>
            <body>

            <h1>About RiffMates</h1>
            <p>The site will cater to musicians looking for bands, bands looking for musicians, venues looking
for bands, and bands looking for gigs. </p>

            </body>
            </html>"""

    return HttpResponse(content, content_type="text/html")


def version(request):
    data = {"Version": "0.1 beta"}
    return JsonResponse(data)


def news(request):
    data = {
        "news": [
            "RiffMates now has a news page!",
            "RiffMates has its first web page",
        ],
    }
    return render(request, "news2.html", data)


def home(request):
    data = {
        "news": [
            "RiffMates now has a news page!",
            "RiffMates has its first web page",
        ],
    }
    return render(request, "home.html", data)


def news_advanced(request):
    data = {
        "news": [
            (
                datetime.fromisoformat("2023-10-03T12:15:00"),
                "RiffMates now has a news pages!",
            ),
            (
                datetime.fromisoformat("2023-10-03T12:12:00"),
                "RiffMates has its first web page",
            ),
            (
                datetime.fromisoformat("2023-10-01T12:12:00"),
                "RiffMates is cool",
            ),
            (
                datetime.fromisoformat("2023-10-02T12:12:00"),
                "RiffMates has its fourth news item",
            ),
        ],
    }

    return render(request, "news_advanced.html", data)
