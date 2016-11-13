from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import json, requests

from datetime import date



from django.utils import timezone
from .models import Choice, Ingredient

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class QuestionOwnerMixin(object):

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk= self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(pk = pk, owner=self.request.user)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied

        return obj

class IndexView(LoggedInMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_ingredient_list'

    def get_queryset(self):
        """Return the last five published ingredients. But not in the future"""
        return Ingredient.objects.filter(owner=self.request.user).order_by('exp_date')


class DetailView(LoggedInMixin, generic.TemplateView):
    model = Ingredient
    template_name = 'polls/detail.html'
    def get(self, request, *args, **kwargs):
        jsonrequest = requests.get("http://food2fork.com/api/search?key=65f31e8e5a3144c1838a3bd3d15bc959&q=chicken")
        data = json.loads(jsonrequest.content)
        return render(request, self.template_name, {'recipes': data['recipes']})


class ResultsView(LoggedInMixin, QuestionOwnerMixin, generic.DetailView):
    model = Ingredient
    template_name = 'polls/results.html'


def vote(request):
    ingredient = Ingredient(
    owner = request.user,
    ingredient_name=request.POST['ingredient_name'],
    exp_date = date(int(request.POST['exp_date'][:4]), int(request.POST['exp_date'][5:7]),
    int(request.POST['exp_date'][8:])))
    ingredient.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:index'))
