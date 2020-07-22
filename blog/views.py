from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView
from django.utils import timezone
from .models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from taggit.models import Tag
from qna.models import Question
from .forms import SearchForm

def home(request):
    if request.POST:
        query=request.POST['title']
        print(query)
        return redirect('search-result',query)
    blogs=Blog.objects.all().order_by('-posted_on')[:5]
    searchform=SearchForm()
    return render(request,'blog/home.html',{'blogs':blogs,'searchform':searchform})


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name="blogs"             # This value will be used to access objects in HTML
    paginate_by=7
    ordering=['-posted_on']


class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = "blog/create_blog.html"
    fields=["title","content","tags"]
    #success_url='/'

    def form_valid(self,form):
        form.instance.author=self.request.user
        form.instance.posted_on=timezone.now()
        return super().form_valid(form)
    


class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Blog
    template_name = "blog/update_blog.html"
    fields=["title","content"]

    def test_func(self):
        blog=self.get_object()
        if self.request.user==blog.author:
            return True
        return False

class BlogDetailView(DetailView):
    model = Blog
    context_object_name="blog"
    template_name = "blog/blog_detail.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags']=context['object'].tags.all()
        return context


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blog/delete_blog.html"
    context_object_name="blog"
    success_url='/'


def filtered_tag_questions(request,slug):
    tag = get_object_or_404(Tag, slug=slug)
    blogs=Blog.objects.filter(tags=tag).order_by('-posted_on')
    context = {
        'tag':tag,
        'blogs':blogs,
    }
    return render(request, 'blog/blog_list.html', context)


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name="tags"

def searchResult(request,slug):
    blogs,questions=[],[]
    for i in slug.split():
        b=Blog.objects.filter(title__icontains=i)
        q=Question.objects.filter(title__icontains=i)
        blogs.extend(b)
        questions.extend(q)
    blogs=list(set(blogs))[:4]
    questions=list(set(questions))[:4]
    context={'blogs':blogs,'questions':questions,'slug':slug}
    return render(request,'blog/search_results.html',context)


class BlogSearchListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    ordering=['-posted_on']
    paginate_by=2
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.kwargs['slug']
        blogs=[]
        for i in slug.split():
            b=Blog.objects.filter(title__icontains=i)
            blogs.extend(b)
        blogs=list(set(blogs))
        context={'blogs':blogs,'slug':slug}
        return context


class QuestionSearchListView(ListView):
    model = Question
    template_name = "qna/question_list.html"
    ordering=['-posted_on']
    paginate_by=2
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.kwargs['slug']
        questions=[]
        for i in slug.split():
            q=Question.objects.filter(title__icontains=i)
            questions.extend(q)
        questions=list(set(questions))
        context={'questions':questions,'slug':slug}
        return context

    
