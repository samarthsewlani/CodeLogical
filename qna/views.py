from django.shortcuts import render
from .models import Question,Answer,Upvote,Downvote
from django.views.generic import CreateView,DeleteView,ListView,DetailView
from django.utils import timezone
from .forms import AnswerForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    template_name = "qna/new_question.html"
    fields=["title","content","tags"]

    #We override this form_valid method to add the user and time variables to the form before saving.
    def form_valid(self,form):
        form.instance.asked_by=self.request.user
        form.instance.posted_on=timezone.now()
        return super().form_valid(form)


class QuestionListView(ListView):
    model = Question
    template_name = "qna/question_list.html"
    context_object_name="questions"
    paginate_by=7                   #By default the page object is reffered as 'page_obj' in HTML
    ordering=['-posted_on']

class QuestionDetailView(DetailView):
    model = Question
    template_name = "qna/question_detail.html"
    context_object_name="question"

    #Overriding get_context_data method to add answers of the question    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers']=Answer.objects.filter(question=self.object)
        return context
    


class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Question
    template_name = "qna/delete_question.html"
    context_object_name="question"
    success_url='/question/all'

    #To test that the user logged in is the user that posted question 
    def test_func(self):
        if self.get_object().asked_by ==self.request.user:
            return True
        return False


def add_anwer_to_question(request,pk):
    question=get_object_or_404(Question,pk=pk)      #Return 404 error if the object is not found
    print(request.method)
    print(question.tags.all())
    if request.method=="POST":
        form=AnswerForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            answer_instance=form.save(commit=False)
            answer_instance.question=question
            answer_instance.posted_by=request.user
            answer_instance.posted_on=timezone.now()
            answer_instance.save()
            return redirect('question-detail',pk=question.id)
        elif not request.user.is_authenticated:
            return redirect('login')
        else:
            print("Form Invalid")
            print(form.errors)
    else:
        form=AnswerForm()
        _answers=Answer.objects.filter(question=question).order_by('-upvotes','-posted_on')
        paginator=Paginator(_answers,5)
        page=request.GET.get('page',1)
        answers=paginator.page(page)
        context={'form':form,
                'question':question,
                'answers':answers,
                'tags':question.tags.all()}
    return render(request,'qna/question_answer.html',context)


class AnswerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Answer
    template_name = "qna/delete_answer.html"
    success_url='/question/all'

    #To alter the success_url to the particular question whose answer was deleted
    def delete(self,*args,**kwargs):
        pk=self.get_object().question.pk
        AnswerDeleteView.success_url='/question/'+str(pk)
        return super().delete(*args,**kwargs)

    def test_func(self):
        if self.get_object().posted_by ==self.request.user:
            return True
        return False

@login_required
def upvoteAnswer(request,pk):
    answer=get_object_or_404(Answer,pk=pk)
    check=Upvote.objects.filter(by=request.user,answer=answer)
    question=answer.question
    if len(check)==0:
        answer.upvotes+=1
        answer.save()
        upvote=Upvote.objects.create(by=request.user,answer=answer)
        upvote.save()
        check=Downvote.objects.filter(by=request.user,answer=answer)
        if len(check)>0:
            Downvote.objects.filter(by=request.user,answer=answer).delete()
            answer.downvotes-=1
            answer.save()
    else:
        Upvote.objects.filter(by=request.user,answer=answer).delete()
        answer.upvotes-=1
        answer.save()
    return redirect('question-detail',pk=question.id)

@login_required
def downvoteAnswer(request,pk):
    answer=get_object_or_404(Answer,pk=pk)
    check=Downvote.objects.filter(by=request.user,answer=answer)
    question=answer.question
    if len(check)==0:
        answer.downvotes+=1
        answer.save()
        downvote=Downvote.objects.create(by=request.user,answer=answer)
        downvote.save()
        check=Upvote.objects.filter(by=request.user,answer=answer)
        if len(check)>0:
            Upvote.objects.filter(by=request.user,answer=answer).delete()
            answer.upvotes-=1
            answer.save()
    else:
        Downvote.objects.filter(by=request.user,answer=answer).delete()
        answer.downvotes-=1
        answer.save()
    return redirect('question-detail',pk=question.id)

def filtered_tag_questions(request,slug):
    tag = get_object_or_404(Tag, slug=slug)
    questions=Question.objects.filter(tags=tag).order_by('-posted_on')
    context = {
        'tag':tag,
        'questions':questions,
    }
    return render(request, 'qna/question_list.html', context)


class TagListView(ListView):
    model = Tag
    template_name = "qna/tag_list.html"
    context_object_name="tags"
