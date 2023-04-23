from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import RegisterForm, PostForm, EditProfileForm, MessageForm, AvatarChange
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.views import logout_then_login
from .models import Post, Message, Avatar
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your views here.

@login_required
def index(request):
    latest_posts = Post.objects.order_by('pub_date')[:10]
    user = request.user
    avatar = None  # Asignar un valor predeterminado
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    context = {'latest_posts': latest_posts,'usuario':user,'avatar':avatar}
    return render(request, "index.html", context)

def details(request):
    return render (request, "details.html")

@login_required
def profile(request, user):
    user = request.user
    num_posts = Post.objects.filter(author=user).count()
    email = request.user.email
    user_posts = Post.objects.filter(author=user)
    context = {'num_posts': num_posts, 'email': email,'user_posts':user_posts}

    try:
        avatar = Avatar.objects.get(user=request.user)
        context['avatar'] = avatar
    except Avatar.DoesNotExist:
        pass

    return render(request, "profile.html", context)
   

def browse(request):
    return render (request, "browse.html")

def streams(request):
    return render (request, "streams.html")

def Login_Final(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.cleaned_data.get("username")
            password = form.cleaned.data_get('password')
            
            user = authenticate(username=user,password=password)
            
            if user is not None:
                login(request, user)

                next_url = request.GET.get('next', '')
                if next_url:
                    return redirect(next_url)

                return redirect(request, "../index/", {"mensaje": f"Welcome {user}"})
            else:
                return render(request,"respuesta.html",{"mensaje":"Error,datos incorrectos"})
        else:
                return render(request, "respuesta.html", {"mensaje": "Error, formulario erroneo"})
    
    form = AuthenticationForm()

    return render(request, "Login_Final_Proyect.html",{'form':form})

def Home(request):
    latest_posts = Post.objects.order_by('pub_date')[:10]
    user = request.user
    context = {'latest_posts': latest_posts,'usuario':user}
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html")

def Register_Final(request):
    if request.method == 'POST':
        # obtener los datos del formulario
        username = request.POST['username']
        password = request.POST['password1']
        email = request.POST['email']

        # verificar si el nombre de usuario ya está en uso
        if User.objects.filter(username=username).exists():
            return render(request, 'Register_Final.html', {'form': RegisterForm(), 'error': 'El nombre de usuario ya está en uso.'})

        # crear el usuario
        else:
            user = User.objects.create_user(username, email, password)
            user.save()

        # autenticar al usuario y redirigirlo a la página de inicio
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../index/')
        else:
            # mostrar un mensaje de error si las credenciales son incorrectas
            return render(request, 'Register_Final.html', {'form': RegisterForm(), 'error': 'Error al autenticar al usuario.'})
    else:
        form = RegisterForm()
    return render(request, 'Register_Final.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return logout_then_login(request, login_url=reverse_lazy('home'))

#return redirect('prueba:profile', user=request.user.username)
@login_required
def avatar_change(request):
    avatar = None
    if request.method == 'POST':
        form = AvatarChange(request.POST, request.FILES)
        if form.is_valid():
            avatar, created = Avatar.objects.update_or_create(
                user=request.user,
                defaults={'image': form.cleaned_data['image']}
            )
            return redirect(f'../profile/{request.user.username}')
    else:
        form = AvatarChange()
        try:
            avatar = Avatar.objects.get(user=request.user)
        except Avatar.DoesNotExist:
            pass
    return render(request, 'avatar_change.html', {'form': form, 'avatar': avatar})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post_url = reverse('prueba:detail', args=[post.id])
            return redirect(post_url)
    else: 
        form = PostForm()
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    return render(request, 'create_post.html', {'form':form,'avatar':avatar})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    
    return render(request, 'post_detail.html', {'post':post,'avatar':avatar})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    return render(request, 'post_detail.html', {'form': form})
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('prueba:post_list')

def post_list(request):
    latest_posts = Post.objects.order_by('pub_date')[::1]
    user = request.user
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    context = {'latest_posts': latest_posts,'usuario':user,'avatar':avatar}
    return render(request, 'post_list.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        username = RegisterForm(user=request.user, data=request.POST)
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(), username.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('prueba:profile')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación')
    else:
        form = PasswordChangeForm(user=request.user)
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    return render(request, 'profile_edit.html', {'form': form,'avatar':avatar})
#COMPLETO>>>



@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user)
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    context = {'messages': messages,'avatar':avatar}
    return render(request, 'inbox.html', context)

@login_required
def sent(request):
    messages_sent = request.user.sent_messages.all().order_by('-sent_date')
    return render(request, 'sent.html', {'messages_sent': messages_sent})

@login_required
def compose(request, recipient=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.sent_date = timezone.now()
            message.read = False
            message.save()
            messages.success(request, 'Message sent successfully')
            return HttpResponseRedirect(reverse('prueba:inbox'))
    else:
        form = MessageForm(initial={'receiver': recipient})
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    return render(request, 'compose.html', {'form': form,'avatar':avatar})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver == request.user:
        message.read = True
        message.save()
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    return render(request, 'message_detail.html', {'message': message,'avatar':avatar})


@login_required
def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient = form.cleaned_data['recipient']
            sender = request.user
            
            # Crear mensaje enviado
            sent_message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                sent_date=timezone.now()
            )
            
            # Crear mensaje recibido
            received_message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                sent_date=timezone.now(),
                received_date=timezone.now()
            )
            
            # Guardar ambos mensajes
            sent_message.save()
            received_message.save()
            
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('prueba:inbox')
    else:
        form = MessageForm()
    try:
        avatar = Avatar.objects.get(user=request.user)
    except Avatar.DoesNotExist:
        pass
    return render(request, 'create_message.html', {'form': form,'avatar':avatar})


def plantilla(request):
    return render(request, "Plantilla.html")