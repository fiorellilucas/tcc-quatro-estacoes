from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from . import models, forms


class MyLoginView(LoginView):

    template_name = "quatroestacoes/login.html"
    next_page = "quatroestacoes:index"
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):

    next_page = "quatroestacoes:login"


class MudarSenhaView(PasswordResetView):

    extra_email_context = {
        "site_name": "Condomínio Quatro Estações"
    }
    template_name = "quatroestacoes/mudar-senha/email.html"


class MudarSenhaPronto(PasswordResetDoneView):

    template_name = "quatroestacoes/mudar-senha/pronto.html"


class MudarSenhaConfirmar(PasswordResetConfirmView):

    template_name = "quatroestacoes/mudar-senha/confirmar.html"
    form_class = forms.AlterarSenhaForm


class MudarSenhaCompletar(PasswordResetCompleteView):

    template_name = "quatroestacoes/mudar-senha/completar.html"


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "quatroestacoes/index.html"

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        context["avisos"] = models.Aviso.objects.all().order_by("-data_postagem")[:3]
        context["reservas"] = models.Reserva.objects.filter(data__gte=timezone.localdate()).order_by("data")[:5]
        context["data_atual"] = timezone.localdate()
        return context


class MoradoresListaView(LoginRequiredMixin, ListView):

    model = models.Morador
    context = models.Morador.objects.all()
    context_object_name = "moradores"
    template_name = "quatroestacoes/moradores/lista.html"


class MoradoresInfoView(LoginRequiredMixin, DetailView):

    model = models.Morador

    def get(self, request, id_morador):
        morador = models.Morador.objects.get(pk=id_morador)
        response = render(
            request, "quatroestacoes/moradores/info.html", {"morador": morador})

        return response


class MoradoresAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = models.Morador
    template_name = "quatroestacoes/moradores/adicionar.html"
    form_class = forms.MoradorCreationForm
    success_url = reverse_lazy("quatroestacoes:moradores_lista")

    redirect_field_name = None

    def test_func(self):
        return self.request.user.is_staff


class MoradoresUpdView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = models.Morador
    template_name = "quatroestacoes/moradores/alterar.html"
    form_class = forms.MoradorChangeForm
    success_url = reverse_lazy("quatroestacoes:moradores_lista")

    login_url = "quatroestacoes:index"
    redirect_field_name = None

    def test_func(self):
        return self.request.user.is_staff


class MoradoresDelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Morador
    template_name = "quatroestacoes/moradores/deletar.html"
    success_url = reverse_lazy("quatroestacoes:moradores_lista")
    context_object_name = "morador"

    login_url = "quatroestacoes:index"
    redirect_field_name = None

    def test_func(self):
        return self.request.user.is_staff


class CalendarioView(LoginRequiredMixin, TemplateView):
    
    template_name = "quatroestacoes/calendario.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reservas"] = list(models.Reserva.objects.all().values())
        context["moradores"] = list(models.Morador.objects.all().values("id", "first_name", "last_name"))      
        return context


class ReunioesListaView(LoginRequiredMixin, ListView):

    model = models.Reuniao
    context = models.Reuniao.objects.all()
    context_object_name = "reunioes"
    template_name = "quatroestacoes/reunioes/lista.html"


class ReunioesAddView(LoginRequiredMixin, CreateView):

    model = models.Reuniao
    template_name = "quatroestacoes/reunioes/adicionar.html"
    form_class = forms.ReuniaoForm
    success_url = reverse_lazy("quatroestacoes:reunioes_lista")


class ReclamacoesListaView(LoginRequiredMixin, ListView):

    model = models.Reclamacao
    context = models.Reclamacao.objects.all()
    context_object_name = "reclamacoes"
    template_name = "quatroestacoes/reclamacoes/lista.html"


class ReclamacoesInfoView(LoginRequiredMixin, DetailView):

    model = models.Reclamacao
    template_name = "quatroestacoes/reclamacoes/info.html"
    context_object_name = "reclamacao"


class ReclamacoesAddView(LoginRequiredMixin, CreateView):

    model = models.Reclamacao
    template_name = "quatroestacoes/reclamacoes/adicionar.html"
    form_class = forms.ReclamacaoForm
    success_url = reverse_lazy("quatroestacoes:reclamacoes_lista")
    
    
class ReclamacoesUpdView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = models.Reclamacao
    template_name = "quatroestacoes/reclamacoes/alterar.html"
    form_class = forms.ReclamacaoForm
    success_url = reverse_lazy("quatroestacoes:reclamacoes_lista")
    
    login_url = "quatroestacoes:index"
    redirect_field_name = None
    
    def test_func(self):
        return self.request.user.is_staff


class ReclamacoesDelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = models.Reclamacao
    template_name = "quatroestacoes/reclamacoes/deletar.html"
    success_url = reverse_lazy("quatroestacoes:reclamacoes_lista")
    context_object_name = "reclamacao"
    
    login_url = "quatroestacoes:index"
    redirect_field_name = None
    
    def test_func(self):
        return self.request.user.is_staff  


class AvisosListaView(LoginRequiredMixin, ListView):

    model = models.Aviso
    template_name = "quatroestacoes/avisos/lista.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avisos"] = models.Aviso.objects.all().order_by("-data_postagem")
        return context


class AvisosInfoView(LoginRequiredMixin, DetailView):

    model = models.Aviso
    template_name = "quatroestacoes/avisos/info.html"
    context_object_name = "aviso"


class AvisosAddView(LoginRequiredMixin, CreateView):

    model = models.Aviso
    template_name = "quatroestacoes/avisos/adicionar.html"
    form_class = forms.AvisoForm
    success_url = reverse_lazy("quatroestacoes:avisos_lista")
    
    
class AvisosUpdView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = models.Aviso
    template_name = "quatroestacoes/avisos/alterar.html"
    form_class = forms.AvisoForm
    success_url = reverse_lazy("quatroestacoes:avisos_lista")
    
    login_url = "quatroestacoes:index"
    redirect_field_name = None
    
    def test_func(self):
        return self.request.user.is_staff


class AvisosDelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = models.Aviso
    template_name = "quatroestacoes/avisos/deletar.html"
    success_url = reverse_lazy("quatroestacoes:avisos_lista")
    context_object_name = "aviso"
    
    login_url = "quatroestacoes:index"
    redirect_field_name = None
    
    def test_func(self):
        return self.request.user.is_staff    


class ReservasListaView(LoginRequiredMixin, ListView):

    model = models.Reserva
    template_name = "quatroestacoes/reservas/lista.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reservas"] = models.Reserva.objects.filter(data__gte=timezone.localdate()).order_by("data")
        return context


class ReservasAddView(LoginRequiredMixin, CreateView):

    model = models.Reserva
    template_name = "quatroestacoes/reservas/adicionar.html"
    form_class = forms.ReservaForm
    success_url = reverse_lazy("quatroestacoes:calendario")
