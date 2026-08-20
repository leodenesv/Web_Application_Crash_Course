from django.http import HttpResponseRedirect
from django.urls import reverse  # Corrigido: 'core.urlresolvers' não existe mais
from django.contrib.auth import logout

def logout_view(request):
    """Efetua o logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

# Create your views here.
