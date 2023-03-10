from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question



class IndexView(generic.ListView):
    template_name = 'ankiety/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Wyświetla 5 ostatnich ankiet które mają przeszłą date publikacji
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'ankiety/detail.html'
    def get_queryset(self):
        """
        Wyświetla wszystkie ankiety które mają przeszłą date publikacji
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ankiety/wyniki.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Błąd, ponowne wyświetlanie wyboru
        return render(request, 'ankiety/detail.html', {
            'question': question,
            'error_message': "Nic nie wybrałeś.",
        })
    else:
        selected_choice.votes = True
        selected_choice.save()
        # Przekierowanie po wysłaniu POST
        return HttpResponseRedirect(reverse('ankiety:wyniki', args=(question.id,)))