from django.shortcuts import HttpResponse
from django.http import JsonResponse 


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

