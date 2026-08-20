from django.http import HttpResponseRedirect
from django.urls import reverse  
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def logout_view(request):
    """Efetua o logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """Cadastra um novo usuário."""
    if request.method != 'POST':
        # Exibe um formulário de cadastro em branco
        form = UserCreationForm()
    else:
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            
            # FORMATO MODERNO: Loga o usuário criado diretamente e de forma segura
            login(request, new_user)
            
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
