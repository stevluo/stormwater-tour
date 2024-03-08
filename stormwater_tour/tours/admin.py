from django.contrib import admin

from .models import *


class SiteOrderAdmin(admin.TabularInline):
    model = Site
    ordering = ['tour_order']
    fields = ('title', 'site_slug', 'tour_order',)

    def has_add_permission(self, request):
        return False


class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'tour_slug', 'id')
    fieldsets = (
        (None, {
            'fields': ('name', 'tour_slug', 'site_nickname',
                       'travel_method'),
        }),
        ('Required Pages', {
            'fields': ('landing_page', 'map_page', 'feedback_page',
                       'about_page',)
        }),
        ('Custom CSS', {
            'fields': ('tour_css',)
        })
    )
    inlines = [
        SiteOrderAdmin,
    ]


class SiteImageInline(admin.TabularInline):
    model = SiteImage
    extra = 1


class SiteInfoTabInline(admin.StackedInline):
    model = InfoTab
    extra = 0
    fieldsets = (
        ("Details", {
            'classes': ('collapse',),
            'fields': ('title', 'description', 'elements', 'serve_as_html'),
        }),
    )


class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'site_slug', 'tour',)
    list_filter = ('tour',)
    fieldsets = (
        (None, {
            'fields': ('tour', 'title', 'site_slug', 'location',
                       'tour_order'),
        }),
        ('Information', {
            'fields': ('simple_directions', 'description', 'serve_as_html',),
        })
    )
    inlines = [
        SiteImageInline,
        SiteInfoTabInline,
    ]


class MapLandmarkMarkerInline(admin.StackedInline):
    model = MapLandmarkMarker
    extra = 0
    fieldsets = (
        ("Details", {
            'classes': ('collapse',),
            'fields': ('title', 'location', 'file_location'),
        }),
    )


class MapPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour')
    fieldsets = (
        ('Map Locations', {
            'fields': ('map_center', 'map_upper_bound', 'map_lower_bound'),
        }),
        ('Map Zoom Levels', {
            'fields': ('map_default_zoom', 'map_min_zoom', 'map_max_zoom'),
        }),
        ('Map Markers', {
            'classes': ('collapse',),
            'fields': ('current_site_marker', 'next_site_marker',
                       'site_visited_marker', 'site_unvisited_marker'),
        }),
    )
    inlines = [
        MapLandmarkMarkerInline
    ]


class AboutElementInline(admin.StackedInline):
    model = AboutElement
    extra = 0
    fieldsets = (
        ("Details", {
            'classes': ('collapse',),
            'fields': ('title', 'description', 'serve_as_html',),
        }),
    )


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour')
    inlines = [
        AboutElementInline,
    ]


class MapLocationAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour')


class ThankYouPageAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class FeedbackPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour')


class InfoTabElementAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Tour, TourAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(MapPage, MapPageAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(MapLocation, MapLocationAdmin)
admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(ThankYouPage, ThankYouPageAdmin)
admin.site.register(FeedbackPage, FeedbackPageAdmin)
admin.site.register(InfoTabElement, InfoTabElementAdmin)


class UserFeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('origin', 'background', 'method', 'feedback', )
    list_display = ('__str__', 'origin', 'background', 'method', 'feedback_trim',)

    def feedback_trim(self, instance):
        feedback = instance.feedback
        if len(feedback) > 30:
            return (instance.feedback[0:30] + '...')
        else:
            return instance.feedback

    def has_add_permission(self, request):
        return False

# This registration MUST be done AFTER the class 'UserFeedbackAdmin' is created
admin.site.register(UserFeedback, UserFeedbackAdmin)
