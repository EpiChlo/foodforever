from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from .models import Choice, Question

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
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. But not in the future"""
        return Question.objects.filter(owner=self.request.user).filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoggedInMixin, QuestionOwnerMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Don't let users access the future
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoggedInMixin, QuestionOwnerMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
