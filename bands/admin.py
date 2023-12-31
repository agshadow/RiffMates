from django.contrib import admin

# Register your models here.

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bands.models import Musician, Band, Venue, Room, UserProfile
from datetime import datetime, date
from django.utils.html import format_html, mark_safe
from django.urls import reverse


class DecadeListFilter(admin.SimpleListFilter):
    title = "decade born"
    parameter_name = "decade"

    def lookups(self, request, model_admin):
        result = []

        this_year = datetime.today().year
        this_decade = (this_year // 10) * 10
        start = this_decade - 10
        for year in range(start, start - 100, -10):
            result.append((str(year), f"{year}-{year+9}"))
        return result

    def queryset(self, request, queryset):
        start = self.value()
        if start is None:
            return queryset

        start = int(start)
        result = queryset.filter(
            birth__gte=date(start, 1, 1), birth__lte=date(start + 9, 12, 31)
        )
        return result


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "birth",
        "show_weekday",
        "show_bands",
    )
    list_filter = (DecadeListFilter,)
    search_fields = (
        "last_name",
        "first_name",
    )

    def show_weekday(self, obj):
        return obj.birth.strftime("%A")

    show_weekday.short_description = "Birth Weekday"

    def show_bands(self, obj):
        bands = obj.band_set.all()
        if len(bands) == 0:
            return format_html("<i>None</i>")

        plural = ""
        if len(bands) > 1:
            plural = "s"

        parm = "?id__in=" + ",".join([str(b.id) for b in bands])
        url = reverse("admin:bands_band_changelist") + parm
        print(url)
        return format_html('<a href="{}">Band{}</a>', url, plural)

    show_bands.short_descriptions = "Bands"


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_members", "show_members1")
    search_fields = ("name",)

    def show_members(self, obj):
        members = obj.musicians.all()
        links = []

        url = reverse("admin:bands_musician_changelist")

        for member in members:
            parm = f"?id={member.id}"
            link = format_html('<a href="{}{}">{}</a>', url, parm, member.last_name)
            links.append(link)

        return mark_safe(", ".join(links))

    show_members.short_description = "Members"

    def show_members1(self, obj):
        musicians = obj.musicians.all()
        print(musicians)
        if len(musicians) == 0:
            return format_html("<i>None</i>")

        html_musicans = ""

        for m in musicians:
            print(obj.name)
            parm = "?id__in=" + str(m.id)
            url = reverse("admin:bands_musician_changelist") + parm

            print(url)
            html_musicans += f"<li><a href='{url}'>{m.first_name} {m.last_name}</a>"
            print(html_musicans)

        return mark_safe(html_musicans)  # used mark_safe as it is only one argument

    show_members1.short_description = "Members1"


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "show_venue_name", "show_rooms")
    # list_filter = (DecadeListFilter,)
    search_fields = ("name",)

    def show_rooms(self, obj):
        rooms = obj.room_set.all()
        if len(rooms) == 0:
            return format_html("<i>None</i>")
        html_rooms = ""

        for r in rooms:
            print(obj.name)
            parm = "?id__in=" + str(r.id)
            url = reverse("admin:bands_room_changelist") + parm

            print(url)
            html_rooms += "<li><a href='" + url + "'>" + r.name + "</a>"
            print(html_rooms)

        return format_html(html_rooms)  # could have used mark_safe here instaed

    show_rooms.short_description = "Rooms"

    def show_venue_name(self, obj):
        rooms = obj.room_set.all()
        if len(rooms) == 0:
            return format_html(obj.name)

        parm = "?id__in=" + ",".join([str(r.id) for r in rooms])
        url = reverse("admin:bands_room_changelist") + parm
        print(f"URL: {url}")

        return format_html("<a href = '{}'>" + obj.name + "</a>", url)

    show_venue_name.short_description = "Venue Name"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    # list_filter = (DecadeListFilter,)
    search_fields = ("name",)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
