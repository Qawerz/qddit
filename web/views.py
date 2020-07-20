from datetime import datetime, time

from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, request, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import context, RequestContext
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin, FormView

from web.forms import PublicationForm, RegisterUserForm, AuthUserForm, CommentsForm, EditProfileForm, ProfileForm
from web.models import Publication, Profile, Comments


##########################
###  Простые страницы  ###
##########################


# Стартовая страница с текстом
def index(request):
    return render(request, 'index_bb.html')


def reddit_clone(request):
    return render(request, 'reddit_clone.html')


# Страница с контактами
def contacts(request):
    return render(request, 'contacts.html')


#################
###  Аккаунт  ###
#################


# Форма логина
class MyProjectLoginView(LoginView):
    template_name = 'login_page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


# Форма регистрации
class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid

    def get_success_url(self):
        return self.success_url


# Выход из аккаунта
class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('home')


# Просмотр Профиля
class ProfileTemplateViewNew(TemplateView):
    model = Profile, Publication
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        """Получене название профиля из поисковой строки"""
        rget = str(request)
        usern = rget[25:-2]

        """Выборка объекта из модел User и его элементы"""
        user_account_user = User.objects.filter(username=usern)
        for user_user in user_account_user:
            id = user_user.id
            username = user_user.username
            date_joined = user_user.date_joined
            first_name = user_user.first_name
            last_name = user_user.last_name
            email = user_user.email

        """Выборка объекта из модел Profile и его элементы"""
        user_account_profile = Profile.objects.filter(username_id=id)
        for user_prof in user_account_profile:
            bio = user_prof.bio
            birth_date = user_prof.birth_date
            user_karma = user_prof.karma
            favcolor = user_prof.favcolor
            avatar = user_prof.avatar

        """Передача информации о постах пользователя"""
        user_posts = Publication.objects.filter(author=id).order_by('-id')

        """Список элементов контекста"""
        context = {
            ##########################################
            'id': id,
            'username': user_user.username,
            'date_joined': user_user.date_joined,
            'first_name': user_user.first_name,
            'last_name': user_user.last_name,
            'email': user_user.email,
            'bio': user_prof.bio,
            'birth_day': user_prof.birth_date,
            'user_karma': user_prof.karma,
            'favcolor': user_prof.favcolor,
            'avatar': user_prof.avatar,
            'publications': user_posts,
            ##########################################
        }

        return render(request, 'profile.html', context)


# Просмотр Профиля
class ProfileTemplateViewTop(TemplateView):
    model = Profile, Publication
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        """Получене название профиля из поисковой строки"""
        rget = str(request)
        usern = rget[25:-6]
        print(usern)

        """Выборка объекта из модел User и его элементы"""
        user_account_user = User.objects.filter(username=usern)
        for user_user in user_account_user:
            id = user_user.id
            username = user_user.username
            date_joined = user_user.date_joined
            first_name = user_user.first_name
            last_name = user_user.last_name
            email = user_user.email

        """Выборка объекта из модел Profile и его элементы"""
        user_account_profile = Profile.objects.filter(username_id=id)
        for user_prof in user_account_profile:
            bio = user_prof.bio
            birth_date = user_prof.birth_date
            user_karma = user_prof.karma
            favcolor = user_prof.favcolor
            avatar = user_prof.avatar

        """Передача информации о постах пользователя"""
        user_posts = Publication.objects.filter(author=id).order_by('-karma')

        """Список элементов контекста"""
        context = {
            ##########################################
            'id': user_user.id,
            'username': user_user.username,
            'date_joined': user_user.date_joined,
            'first_name': user_user.first_name,
            'last_name': user_user.last_name,
            'email': user_user.email,
            'bio': user_prof.bio,
            'birth_day': user_prof.birth_date,
            'user_karma': user_prof.karma,
            'favcolor': user_prof.favcolor,
            'avatar': user_prof.avatar,
            'publications': user_posts,
            ##########################################
        }
        return render(request, 'profile.html', context)

#################################################################
# def ProfileUpdate(request, username):
#     if request.method == "POST":
#         print(username)
#         qu_user = User.objects.filter(username=username)
#         for user_get in qu_user:
#             id = user_get.id
#         qu_profile = Profile.objects.filter(username_id=id)
#         for profile_info in qu_profile:
#             bio = profile_info.bio
#             print(bio)
#         Profile(
#
#             bio=bio
#             ).save()
#     context = {}
#     return render(request, 'update_profile.html', context)
#################################################################


def ProfileUpdate(request, username):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        args['user_form'] = form
        args['profile_form'] = profile_form
        return render(request, 'update_profile.html', args)


####################
###  Публикации  ###
####################


class PublicationsListNew(CreateView):
    model = Publication, Profile
    template_name = 'publications_rl.html'
    form_class = PublicationForm
    success_url = reverse_lazy('publications')

    def get_context_data(self, **kwargs):
        kwargs['publications'] = Publication.objects.all().order_by('-id')
        kwargs['profiles'] = Profile.objects.all().order_by('-karma')[:10]
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PublicationsListTop(CreateView):
    model = Publication, Profile
    template_name = 'publications_rl.html'
    form_class = PublicationForm
    success_url = reverse_lazy('publications')

    def get_context_data(self, **kwargs):
        kwargs['publications'] = Publication.objects.all().order_by('-karma')
        kwargs['profiles'] = Profile.objects.all().order_by('-karma')[:10]
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def PublicationDetail(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST or None)
        if comment_form.is_valid():
            text = request.POST.get('text')
            comment = Comments.objects.create(publication=publication, author=request.user, text=text)
            comment.save()
            return HttpResponseRedirect(publication.get_absolute_url())

    else:
        comment_form = CommentsForm()

        rget = str(request)
        pageid = rget[25:-2]
        print(pageid, " - pageid")

        publications = Publication.objects.filter(id=pageid)
        for publication in publications:
            id = publication.id
            author = publication.author
            name = publication.name
            create_date = publication.create_date
            text = publication.text
            karma = publication.karma
            comments_publication = publication.comments_publication.all

        else:
            comments_form = CommentsForm()

        if publication.likes.filter(id=request.user.id).exists():
            is_liked = True
        else:
            is_liked = False

        if publication.dislikes.filter(id=request.user.id).exists():
            is_disliked = True
        else:
            is_disliked = False

        context = {
            'id': id,
            'author': author,
            'name': name,
            'create_date': create_date,
            'text': text,
            'karma': karma,
            'comments_publication': comments_publication,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
            'comment_form': comment_form,
        }
        return render(request, 'page_rl.html', context)


class PublicationDetailView(CreateView, FormMixin):
    model = Publication, Comments
    form_class = CommentsForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Получене название профиля из поисковой строки"""
        rget = str(request)
        pageid = rget[25:-2]
        # print(pageid, " - pageid")

        publications = Publication.objects.filter(id=pageid)
        for publication in publications:
            id = publication.id
            author = publication.author
            name = publication.name
            create_date = publication.create_date
            text = publication.text
            karma = publication.karma
            comments_publication = publication.comments_publication.all

        else:
            comments_form = CommentsForm()

        if publication.likes.filter(id=request.user.id).exists():
            is_liked = True
        else:
            is_liked = False

        if publication.dislikes.filter(id=request.user.id).exists():
            is_disliked = True
        else:
            is_disliked = False

        context = {
            'id': id,
            'author': author,
            'name': name,
            'create_date': create_date,
            'text': text,
            'karma': karma,
            'comments_publication': comments_publication,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
            'comments_form': comments_form,
        }
        return render(request, 'page_rl.html', context)

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('page', kwargs={'pk': self.get_object().id})
    #

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.publication = self.get_object()
    #     self.object.author = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)


class SubmitCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    template_name = 'submit.html'
    form_class = PublicationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    template_name = 'edit_page.html'
    form_class = PublicationForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись обновлена'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')


@login_required(login_url='/login')
def like_publication(request):
    pid = request.POST.get('publications_id')
    publication = get_object_or_404(Publication, id=pid)
    is_liked = False
    if publication.likes.filter(id=request.user.id).exists():
        publication.likes.remove(request.user)
        is_liked = False
    else:
        publication.likes.add(request.user)
        is_liked = True

    Publication.objects.filter(id=pid).update(karma=publication.total_karma())

    user_pub = Publication.objects.filter(id=pid)
    for pub in user_pub:
        author = pub.author

    at_pub = Publication.objects.filter(author=author)
    tot_karma = 0
    for at_karma in at_pub:
        karma = at_karma.karma

        tot_karma += karma

    print(tot_karma)

    Profile.objects.filter(username_id=author).update(karma=tot_karma)
    return HttpResponseRedirect(reverse_lazy('page', kwargs={'pk': pid}))


@login_required(login_url='/login')
def dislike_publication(request):
    pid = request.POST.get('publications_id')
    publication = get_object_or_404(Publication, id=pid)
    is_disliked = False
    if publication.dislikes.filter(id=request.user.id).exists():
        publication.dislikes.remove(request.user)
        is_dislikedliked = False
    else:
        publication.dislikes.add(request.user)
        is_dislikedliked = True

    Publication.objects.filter(id=pid).update(karma=publication.total_karma())

    user_pub = Publication.objects.filter(id=pid)
    for pub in user_pub:
        author = pub.author

    at_pub = Publication.objects.filter(author=author)
    tot_karma = 0
    for at_karma in at_pub:
        karma = at_karma.karma

        tot_karma += karma

    print(tot_karma)

    Profile.objects.filter(username_id=author).update(karma=tot_karma)
    return HttpResponseRedirect(reverse_lazy('page', kwargs={'pk': pid}))


