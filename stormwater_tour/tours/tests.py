from django.test import TestCase
from .models import *
from .forms import UserForm
from django.template import defaultfilters as filters
# "csrf_client" can be used if a page (map_page) retrieves data from
# OUTSIDE the templates or fixtures we provide. By default, CSRF checks
# are turned OFF in testing, but this is how to enable them for a client.

# csrf_client = Client(enforce_csrf_checks=True)

# TEST_FIXTURE is a global variable, used so that we don't need to change the
# fixture file for each class--should the file name ever change.
TEST_FIXTURE = "march_data.json"


class FeedbackPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        response = self.client.get("/tour/owp/feedback/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/feedback.html")
        self.assertTemplateUsed(response, "tours/forms/feedback_form.html")

    def test_blank_form(self):
        form_data = {'origin': '', 'background': '', 'method': '', 'feedback': ''}
        response = self.client.post("/tour/owp/feedback/", data=form_data)
        self.assertEqual(response.status_code, 200)
        # This next line is specifically used for the form, and checks that
        # the correct error is supplied if no fields contain data.
        self.assertFormError(response, 'form', None, 'While all fields are optional, submission requires that at least one field must have content.')

    def save_and_redirect_on_submission(self):
        test_string = "Some string"
        form_data = {'origin': '', 'background': '', 'method': '', 'feedback': test_string}
        response = self.client.post("/tour/owp/feedback/", data=form_data)
        self.assertRedirects(response, "/tour/owp/feedback/thank_you/")
        # This try/except searches the db for the supposedly saved string
        try:
            # If the string is found, this line "passes"
            all_forms = UserFeedback.objects.get(feedback=test_string)
        except Exception as e:
            # If the string is not found, provide an error message
            self.fail("No matching form entry found in database when saved.")


class FeedbackFormTest(TestCase):
    # No fixture needed for testing the forms
    def test_blank_form(self):
        form_data = {'origin': '', 'background': '', 'method': '', 'feedback': ''}
        form = UserForm(data=form_data)
        # This line verifies that the form reads blank strings as "invalid".
        # Note that it asserts FALSE, as the form SHOULD be invaild.
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            ['While all fields are optional, submission requires that at least one field must have content.'])

    # This test confirms that forms are being saved to the database
    def test_valid_form_saved(self):
        test_string = "String to test for"
        form_data = {'origin': '', 'background': '', 'method': '', 'feedback': test_string}
        form = UserForm(data=form_data)
        # Also tests that a valid form is recognized as valid
        self.assertTrue(form.is_valid())
        form.save()
        # This try/except searches the db for the supposedly saved string
        try:
            # If the string is found, this line "passes"
            all_forms = UserFeedback.objects.get(feedback=test_string)
        except Exception as e:
            # If the string is not found, provide an error message
            self.fail("No matching form entry found in database when saved.")


class AboutPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        response = self.client.get("/tour/owp/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/about.html")


class QueryPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        response = self.client.get("/tour/owp/query_current/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/query_current.html")

    def test_redirects_from_buttons(self):
        response = self.client.get("/tour/owp/query_current/")
        yes_button = (
            '<a class="btn btn-lg btn-block btn-primary"' +
            'href="/tour/owp/select_site/" role="button">Yes</a>'
        )
        no_button = (
            '<a class="btn btn-lg btn-block btn-default"' +
            'href="/tour/owp/map/" role="button">No</a>'
        )
        self.assertContains(
            response,
            yes_button,
            status_code=200,
            html=True
        )
        self.assertContains(
            response,
            no_button,
            status_code=200,
            html=True
        )


class SiteSelectPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        response = self.client.get("/tour/owp/select_site/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/select_site.html")

    def test_redirect(self):
        response = self.client.get("/tour/owp/select_site/")
        first_button = (
            '<button class="btn btn-lg btn-block btn-primary"' +
            'type="submit" name="current_site_id" value="1">' +
            'Lot 7 Bioretention Planter</button>'
        )
        self.assertContains(
            response,
            first_button,
            status_code=200,
            html=True
        )


class LandingPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        response = self.client.get("/tour/owp/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/landing_page.html")

    def test_redirect_to_query_current(self):
        response = self.client.get("/tour/owp/")
        query_button = (
            '<a href="/tour/owp/query_current/" ' +
            'class="btn btn-lg btn-block btn-primary" ' +
            'role="button">Take the Tour</a>'
        )
        self.assertContains(
            response,
            query_button,
            status_code=200,
            html=True
        )

    def test_redirect_to_about(self):
        response = self.client.get("/tour/owp/")
        about_button = (
            '<a class="btn btn-lg btn-block btn-default" ' +
            'href="/tour/owp/about/" role="button">About the Project</a>'
        )
        self.assertContains(
            response,
            about_button,
            status_code=200,
            html=True
        )

    def test_redirect_to_feedback(self):
        response = self.client.get("/tour/owp/")
        feedback_button = (
            '<a class="btn btn-lg btn-block btn-default" ' +
            'href="/tour/owp/feedback/" role="button">Give Us Feedback</a>'
        )
        self.assertContains(
            response,
            feedback_button,
            status_code=200,
            html=True
        )


class ThankYouPageTest(TestCase):
    # fixtures is the data used to populate the "mock" or "fake" database
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        # response is an object that holds the page returned. Make sure to
        # include the slash at the end of the url, or you WILL get an error!
        # Also, include "/tour/" at the beginning, but NOT "localhost:8000"!
        response = self.client.get("/tour/owp/feedback/thank_you/")
        # This next line verifies that the code returned in "response" was
        # 200, or "OK". If you get "301" as the returned code, make sure
        # that the url you're using in "response" has the slash at the end.
        self.assertEqual(response.status_code, 200)
        # These next two lines declare what templaes will be used by the page.
        # If you want to quickly see what templates a page IS using, put in
        # a template that is NOT being used; the error produced will spell out
        # what templates ARE being used.
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/thank_you_page.html")

    # This test is to verify that the "Back to the Tour!" button is functioning
    def test_back_to_tour_redirect(self):
        response = self.client.get("/tour/owp/feedback/thank_you/")
        thank_you_button = (
            '<a href="/tour/owp/map/"' +
            'class="btn btn-lg btn-default"' +
            'role="button">Back To The Tour!</a>'
        )
        self.assertContains(
            response,
            thank_you_button,
            status_code=200,
            html=True
        )


class SitePageTest(TestCase):
    fixtures = [TEST_FIXTURE]
    # grab all the sites to test
    all_sites = Site.objects.all()
    # create the start of the tour url
    # this test will only work for /tour/owp/site/site_slug
    owp_start_string = "/tour/owp/site/"

    def test_index(self):
        # test that the page is loading with the current templates
        # and the correct http response (200)

        # for loop to go through each site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            self.assertEqual(response.status_code, 200)
            # check the templates that are used on the page
            self.assertTemplateUsed(response, "tours/base.html")
            self.assertTemplateUsed(
                response,
                "tours/location_with_tabs_and_dropbar.html")
            # test to make sure the javascript files are loading
            self.assertContains(response, 'slick_slider.js')
            self.assertContains(response, 'slick.min.js')
            # test to make sure the css files are loading
            self.assertContains(response, 'slick.css')
            self.assertContains(response, 'slick-theme.css')
            self.assertContains(response, 'location.css')

    # test that all sites has the next site button
    # test that all sites can be redirected to the map page
    def test_redirection_to_map(self):
        # loop through every site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            self.assertEqual(response.status_code, 200)
            next_site_button = '<a href="/tour/owp/map/"' + '>Next BMP Site</a>'
            self.assertContains(
                response,
                next_site_button,
                status_code=200,
                html=True)

    def test_site_descriptions_and_titles(self):
        # test to see if the site descriptions are loaded and correct

        # for loop to go through each site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            # checks if the site description is loaded and on the page
            self.assertContains(response, site.title)
            self.assertContains(response, site.description)

    def test_site_images(self):
        # test to see if the site images are loaded and correct

        # for loop to go through each site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            # make sure that gallery div is loaded
            self.assertContains(response, 'gallery')
            # checks if the site image(s) is loaded and on the page
            images = site.siteimage_set.all()
            for image in images:
                self.assertContains(response, image.file_location)

    def test_site_tabs(self):
        # test to see if the site tabs are loaded and correct

        # for loop to go through each site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            # Checks if tabs are loaded and on the page.
            tabs = site.infotab_set.all()
            for site_info_tab in tabs:
                self.assertContains(response, site_info_tab.title)

    def test_site_tabs_elements(self):
        # test to see if the site tab elements are loaded and correct

        # for loop to go through each site
        for site in self.all_sites:
            # concatenate the string to make /tour/owp/site/site_slug/
            site_string = self.owp_start_string + site.site_slug + "/"
            # get the http status code for the page
            response = self.client.get(site_string)
            # Iterate through each tab
            tabs = site.infotab_set.all()
            for site_info_tab in tabs:
                # Checks if the tab elements are loaded and on the page
                elements = site_info_tab.elements.all()
                for panel_element in elements:
                    self.assertContains(response, panel_element.title)
                    self.assertContains(response, panel_element.image.url)
                    # self.assertContains(response, panel_element.description)


class MapPageTest(TestCase):
    # fixtures is the data used to populate the "mock" or "fake" database
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        # response is an object that holds the page returned. Make sure to
        # include the slash at the end of the url, or you WILL get an error!
        # Also, include "/tour/" at the beginning, but NOT "localhost:8000"!
        response = self.client.get("/tour/owp/map/")
        # This next line verifies that the code returned in "response" was
        # 200, or "OK". If you get "301" as the returned code, make sure
        # that the url you're using in "response" has the slash at the end.
        self.assertEqual(response.status_code, 200)
        # These next two lines declare what templaes will be used by the page.
        # If you want to quickly see what templates a page IS using, put in
        # a template that is NOT being used; the error produced will spell out
        # what templates ARE being used.
        self.assertTemplateUsed(response, "tours/base.html")
        self.assertTemplateUsed(response, "tours/map_page.html")
        # check for the map css
        self.assertContains(response, "tours/css/map_page.css")

    # check if all the sites for the owp tour are loaded
    # test if the buttons for the sites can redirect
    def test_site_buttons(self):
        # get the response for the map page
        owp_map_string = "/tour/owp/"
        map_response = self.client.get(owp_map_string)
        # grab all the sites
        all_sites = Site.objects.all()
        # start of /tour/owp/site/site_slug/
        owp_start_string = "/tour/owp/site/"
        # loop through all the sites
        for site in all_sites:
            owp_site_string = owp_start_string + site.site_slug + "/"

    # test the correct location for the site on the owp tour
    # test that the map has the marker at that location
    def test_site_location(self):
        # get the response for the map page
        owp_map_string = "/tour/owp/map/"
        map_response = self.client.get(owp_map_string)
        # grab all sites
        all_sites = Site.objects.all()
        for site in all_sites:
            new_site = str(site.id)
            # test if the site and its location are being used correctly in the javascript
            google_site_location = "var location_" + new_site + " = new google.maps.LatLng(" + str(site.location.latitude) + ", " + str(site.location.longitude) + ");"
            self.assertContains(map_response, google_site_location)
            # test if the markers are correct
            marker = "var marker_" + new_site + " = new google.maps.Marker({"
            position = "position: {lat: " + str(site.location.latitude) + ", lng: " + str(site.location.longitude) + "}"
            self.assertContains(map_response, marker)
            self.assertContains(map_response, position)


class indexPageTest(TestCase):
    fixtures = [TEST_FIXTURE]

    def test_index(self):
        # response is an object that holds the page returned. Make sure to
        # include the slash at the end of the url, or you WILL get an error!
        # Also, include "/tour/" at the beginning, but NOT "localhost:8000"

        response = self.client.get("")  # Should this field be left blank,
        # since there is no URL path being supplied?

        # This next line verifies that the code returned in "response" was
        # 200, or "OK". If you get "301" as the returned code, make sure
        # that the url you're using in "response" has the slash at the end.
        self.assertEqual(response.status_code, 200)

        # These next two lines declare what templaes will be used by the page.
        # If you want to quickly see what templates a page IS using, put in
        # a template that is NOT being used; the error produced will spell out
        # what templates ARE being used.
        self.assertTemplateUsed(response, "tours/tour_index.html")

    # This test is limited, as the buttons themselves are prone to change.
    # We should consider removing it altogether
    def test_redirection(self):
        response = self.client.get("")
        tour_button = (
            '<a class="btn btn-lg btn-block btn-primary" ' +
            'href="/tour/owp/" role="button" style="white-space: normal;">' +
            '<p class="lead text-left">OWP Facilities Tour</p>' +
            '<h5 class="text-left">Welcome to Sacramento State and to the ' +
            'stormwater Low Impact Development (LID) tour.  The tour is a ' +
            'guided walk past 7 stormwater management facilities, called ' +
            'Best Management Practices (BMPs), plus the stormwater discharge ' +
            'near the Guy West Bridge.  Although you may think they’re just ' +
            'planters, these BMPs are carefully designed to capture runoff ' +
            'and remove pollutants.  Take the tour to learn more.</h5></a>'
        )
        self.assertContains(
            response,
            tour_button,
            status_code=200,
            html=True
        )
