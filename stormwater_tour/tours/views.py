from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from .models import *
from .forms import UserForm


def landing_page(request, tour_slug):
    # Uncomment to clear session
    # request.session.flush()

    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    tour_in_progress = False
    if 'current_site'+str(tour.id) in request.session:
        tour_in_progress = True
    context = {'tour': tour,
               'tour_slug': tour_slug,
               'tour_in_progress': tour_in_progress}
    return render(request,
                  'tours/landing_page.html',
                  context)


def tour_index(request):
    tours = Tour.objects.order_by('name')
    context = {'tours': tours}
    return render(request, 
                  'tours/tour_index.html', 
                  context)


def query_current(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    context = {'tour': tour,
               'tour_slug': tour_slug}
    return render(request,
                  'tours/query_current.html',
                  context)


def select_site(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    sites = Site.objects.filter(tour=tour).order_by('tour_order')
    if request.method == 'POST':
        if 'current_site_id' in request.POST:
            site_id = request.POST['current_site_id']
            site = get_object_or_404(Site, id=site_id)
            return HttpResponseRedirect(
                    reverse('tours:site',
                            kwargs={
                                'tour_slug': tour_slug,
                                'site_slug': site.site_slug
                            })
                )
        else:
            return HttpResponseRedirect(
                    reverse('tours:map_pa',
                            kwargs={
                                'tour_slug': tour_slug
                            })
                )

    context = {'tour': tour,
               'tour_slug': tour_slug,
               'sites': sites}
    return render(request,
                  'tours/select_site.html',
                  context)


def location_with_tabs_and_dropbar(request, tour_slug, site_slug):
    site = get_object_or_404(Site, site_slug=site_slug)
    info_tabs = site.infotab_set.all()
    # see if there is a tab / tab titled "Site Features"
    for index, info_tab in enumerate(info_tabs):
        if info_tab.title == "Site Features":
            # save the index of the "Site Features" tab
            a = index
            # place the "Site Features" tab in the front and add the other tabs after it
            # the exclude will skip over the "Site Features" tab, prevents duplicates
            tabs = [info_tabs[index]] + [tab for tab in info_tabs.exclude(title = "Site Features")]
            info_tabs = tabs
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    sites = Site.objects.filter(tour=tour).order_by('tour_order')
    context = {'site': site,
               'tour': tour,
               'info_tabs': info_tabs,
               'tour_slug': tour_slug}

    # Sets the current site
    request.session['current_site'+str(tour.id)] = site.id

    # Adds this site to the list of visited sites
    try:
        visited = []
        visited = request.session['sites_visited'+str(tour.id)]
        if site.id not in visited:
            visited.append(site.id)
            request.session['sites_visited'+str(tour.id)] = visited
    except KeyError:
        visited = []
        visited.append(site.id)
        request.session['sites_visited'+str(tour.id)] = visited

        # Determines next site
    if sites.count() == len(request.session['sites_visited'+str(tour.id)]):
        request.session['next_site'+str(tour.id)] = Site.objects.get(
            tour_order=site.tour_order, tour=tour).id
    else:
        next_site_found = False
        site_list = list(sites)
        site_counter = site_list.index(site)
        while next_site_found is False:
            site_counter = (site_counter + 1) % len(site_list)
            next_site_check = site_list[site_counter].id
            if next_site_check not in request.session['sites_visited'+str(tour.id)]:
                request.session['next_site'+str(tour.id)] = Site.objects.get(
                    id=next_site_check, tour=tour).id
                next_site_found = True

    return render(request,
                  'tours/location_with_tabs_and_dropbar.html',
                  context)


def map_page(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    sites = Site.objects.filter(tour=tour).order_by('tour_order')
    tour_map = tour.map_page
    feedback = tour.feedback_page
    landmark_markers = MapLandmarkMarker.objects.filter(map_page=tour_map)
    context = {
        'dev_map_key': settings.GOOGLE_MAP_API_KEY,
        'sites': sites,
        'tour': tour,
        'tour_slug': tour_slug,
        'map_page': tour_map,
        'feedback': feedback,
        'landmark_markers': landmark_markers
    }
    # Uncomment to clear session
    # request.session.flush()

    # Passes current site information into context
    try:
        current_site_id = request.session["current_site"+str(tour.id)]
        context['current_site'] = Site.objects.get(id=current_site_id)
    except KeyError:
        context['current_site'] = None

    # Passes next site information into context
    # Sets initial next site as site with the lowest tour order
    try:
        next_site_id = request.session["next_site"+str(tour.id)]
        context['next_site'] = Site.objects.get(id=next_site_id)
    except KeyError:
        if not sites:
            context['next_site'] = None
        else:
            site_list = list(sites)
            site_counter = 0
            first_site = 10000
            for site_counter in range(0, len(site_list)):
                next_site_check = site_list[site_counter]
                if first_site > next_site_check.tour_order:
                    first_site = next_site_check.tour_order
            context['next_site'] = Site.objects.get(tour_order=first_site, tour=tour)

    # Passes the sites that have been visted into context
    try:
        sites_visisted_ids = request.session["sites_visited"+str(tour.id)]
        context['sites_visited'] = Site.objects.filter(id__in=sites_visisted_ids)
    except KeyError:
        context['sites_visited'] = []

    # Passes whether or not feedback has been submitted
    try:
        context['feedback_submitted'] = request.session["feedback_submitted"+str(tour.id)]
    except KeyError:
        context['feedback_submitted'] = False

    try:
        context['no_feedback_prompt'] = request.session["no_feedback_prompt"+str(tour.id)]
    except KeyError:
        context['no_feedback_prompt'] = False

    return render(request, 'tours/map_page.html', context=context)


def about(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    about_elements = tour.about_page.aboutelement_set.all()
    context = {'tour': tour,
               'tour_slug': tour_slug,
               'about_elements': about_elements}
    return render(request, 'tours/about.html', context)


def feedback(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            completed = form.save()
            return HttpResponseRedirect(
                reverse('tours:thank_you', kwargs={'tour_slug': tour_slug})
            )
    else:
        form = UserForm()
    request.session['no_feedback_prompt'+str(tour.id)] = True
    context = {'tour': tour,
               'tour_slug': tour_slug,
               'form': form}

    try:
        context['feedback_submitted'] = request.session["feedback_submitted"+str(tour.id)]
    except KeyError:
        context['feedback_submitted'] = False

    return render(request, 'tours/feedback.html', context)


def thank_you(request, tour_slug):
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    context = {'tour': tour,
               'tour_slug': tour_slug}
    request.session['feedback_submitted'+str(tour.id)] = True
    return render(request,
                  'tours/thank_you_page.html', context)
