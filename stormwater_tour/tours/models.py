from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class MapLocation(models.Model):
    title = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        help_text="In decimal degree format. Supports six decimal places."
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="In decimal degree format. Supports six decimal places."
    )

    def __str__(self):
        if self.title:
            return "%s" % (self.title)
        return "Location %f, %f" % (self.latitude, self.longitude)


class LandingPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title and Description.'
    )

    def __str__(self):
        return "%s" % (self.title)


class ThankYouPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title and Description.'
    )

    def __str__(self):
        return "%s" % (self.title)


class FeedbackPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    feedback_request_checkpoint = models.PositiveSmallIntegerField(
        default=3,
        help_text="The number of sites that are visited before a request for feedback is made."
    )
    thank_you_page = models.OneToOneField(ThankYouPage)
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title and Description.'
    )

    def __str__(self):
        return "%s" % (self.title)


class AboutPage(models.Model):
    title = models.CharField(max_length=100)
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title.'
    )

    def __str__(self):
        return "%s" % (self.title)


class AboutElement(models.Model):
    about_page = models.ForeignKey(AboutPage)
    title = models.CharField(max_length=100)
    description = models.TextField()
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title and Description.'
    )

    def __str__(self):
        return "%s" % (self.title)


class MapPage(models.Model):
    map_center = models.OneToOneField(
        MapLocation,
        related_name="map_center"
    )
    map_default_zoom = models.PositiveSmallIntegerField(
        help_text="The zoom amount of the map when page is first loaded."
    )
    map_upper_bound = models.OneToOneField(
        MapLocation,
        related_name="map_upper_bound",
        help_text="The top right of the map. Be generous with how much space is provided."
    )
    map_lower_bound = models.OneToOneField(
        MapLocation,
        related_name="map_lower_bound",
        help_text="The bottom left of the map. Be generous with how much space is provided."
    )
    map_min_zoom = models.PositiveSmallIntegerField(
        help_text="How far the map can be zoomed out",
        verbose_name="Map minimum zoom"
    )
    map_max_zoom = models.PositiveSmallIntegerField(
        help_text="How far the map can be zoomed in",
        verbose_name="Map maximum zoom"
    )
    current_site_marker = models.FileField(
        upload_to='tours/map_markers/', null=True, blank=True,
        help_text='Suggested image size: 32px x 32px')
    next_site_marker = models.FileField(
        upload_to='tours/map_markers/', null=True, blank=True,
        help_text='Suggested image size: 32px x 32px')
    site_visited_marker = models.FileField(
        upload_to='tours/map_markers/', null=True, blank=True,
        help_text='Suggested image size: 32px x 32px')
    site_unvisited_marker = models.FileField(
        upload_to='tours/map_markers/', null=True, blank=True,
        help_text='Suggested image size: 32px x 32px')

    def __str__(self):
        return "Map Page %d" % (self.id)


class MapLandmarkMarker(models.Model):
    title = models.CharField(max_length=100)
    location = models.OneToOneField(MapLocation, null=True)
    map_page = models.ForeignKey(MapPage)
    file_location = models.FileField(upload_to='tours/images/')

    def __str__(self):
        return "Building Marker: %s" % (self.title)


class Tour(models.Model):
    name = models.CharField(max_length=100)
    tour_slug = models.SlugField(
        unique=True,
        help_text="A unique identifier used to differentiate this tour's url from any other.")
    site_nickname = models.CharField(
        max_length=100,
        help_text="Another name for the sites on the tour. Used for generating text for buttons."
    )
    TRAVEL_CHOICES = (
        ('DRIVING', 'DRIVING'),
        ('WALKING', 'WALKING'),
        ('BICYCLING', 'BICYCLING'),
        ('TRANSIT', 'TRANSIT')
    )
    travel_method = models.CharField(
        max_length=9,
        choices=TRAVEL_CHOICES,
        help_text="Determines how the Google Maps API will give best path."
    )
    landing_page = models.OneToOneField(LandingPage)
    feedback_page = models.OneToOneField(FeedbackPage)
    about_page = models.OneToOneField(AboutPage)
    map_page = models.OneToOneField(MapPage)
    tour_css = models.FileField(
        upload_to='tours/css/',
        blank=True,
        null=True,
        help_text='When used adds the uploaded css file to every page of the tour.'
    )

    def __str__(self):
        return "%s - id:%d" % (self.name, self.id)


class Site(models.Model):
    tour = models.ForeignKey(Tour)
    title = models.CharField(max_length=100)
    site_slug = models.SlugField(
        help_text="A unique identifier used to differentiate this site's url from any other.")
    location = models.OneToOneField(MapLocation)
    simple_directions = models.TextField(
        help_text="Directions given when traveling to the site. Should be applicable to all incoming directions to support all tour orders."
    )
    description = models.TextField(
        help_text="Short description given under image slider."
    )
    tour_order = models.PositiveSmallIntegerField()
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Description.'
    )

    class Meta:
        unique_together = (
            ("tour", "title"),
            ("tour", "site_slug"),
            ("tour", "tour_order")
        )

    def __str__(self):
        return "%s" % (self.title)


class SiteImage(models.Model):
    name = models.CharField(max_length=100)
    site = models.ForeignKey(Site)
    file_location = models.FileField(
        upload_to='tours/images/',
        help_text="Insure all images are the same size for best results on the image slider."
    )

    def __str__(self):
        return "Image: %s" % (self.name)


class InfoTabElement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='tours/images/')
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Title and Description.'
    )

    def __str__(self):
        return "%s" % (self.title)


class InfoTab(models.Model):
    site = models.ForeignKey(Site)
    title = models.CharField(max_length=20)
    description = models.TextField()
    elements = models.ManyToManyField(InfoTabElement, blank=True)
    serve_as_html = models.BooleanField(
        default=False,
        help_text='Enables full html use in text fields. Affects: Description.'
    )

    class Meta:
        unique_together = (
            ("site", "title"),
        )

    def __str__(self):
        return "Tour %s: %s" % (self.site, self.title)


class UserFeedback(models.Model):
    ORIGIN_CHOICES = (
        ('Local (Sacramento and its neighboring counties)', 'Local (Sacramento and its neighboring counties)'),
        ('Northern California', 'Northern California'),
        ('Southern California', 'Southern California'),
        ('Outside of California', 'Outside of California')
    )
    BACKGROUND_CHOICES = (
        ('Student', 'Student'),
        ('Industry Professional', 'Industry Professional'),
        ('General Public', 'General Public')
    )
    METHOD_CHOICES = (
        ('I physically travelled between sites', 'I physically travelled between sites'),
        ('I did not visit more than one physical installation', 'I did not visit more than one physical installation')
    )
    origin = models.CharField(
        max_length=100,
        choices=ORIGIN_CHOICES,
        blank=True)
    background = models.CharField(
        max_length=100,
        choices=BACKGROUND_CHOICES,
        blank=True)
    method = models.CharField(
        max_length=100,
        choices=METHOD_CHOICES,
        blank=True)
    feedback = models.TextField(
        max_length=1000,
        blank=True)

    class Meta:
        verbose_name_plural = "user feedback"

    def clean(self):
        # Verify that at least one field is not blank
        if not self.origin and not self.background and not self.feedback and not self.method:
            raise ValidationError(_(
                'While all fields are optional, submission requires that at '
                'least one field must have content.'
            ))

    def __str__(self):
        return "user feedback %s" % (self.id)
