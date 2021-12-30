from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from .models import *


class PanelClient(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Work
    fields = ["name_work", "description_work"]
    success_message = "image added"
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(PanelClient, self).get_context_data(**kwargs)
        a=ClientProfile.objects.filter(user_p=self.request.user)
        if a.count()!=0:
            context["client"] = True
            context["UserProfile"] = a.get()
            context["work_list"] = Work.objects.filter(client_work=context["UserProfile"])
        else:
            context["client"] = False
            context["UserProfile"] = WorkerProfile.objects.filter(user_p=self.request.user).get()
            context["work_list"] = Work.objects.filter(assigned_work=context["UserProfile"])

        context["all_images_count"] = len(context["work_list"])
        context["labeled_images_count"]=len([0 for a in context["work_list"] if a.done_work])

        return context

    def form_valid(self, form):
        prof=ClientProfile.objects.filter(user_p=self.request.user).get()
        form.instance.client_work = prof
        return super().form_valid(form)


class WorkList(LoginRequiredMixin, ListView):
    model = Work
    template_name = 'work_list.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(WorkList, self).get_context_data(**kwargs)
        a=ClientProfile.objects.filter(user_p=self.request.user)
        if a.count()!=0:
            context["client"] = True
            context["UserProfile"] = a.get()
        else:
            context["client"] = False
            context["UserProfile"] = WorkerProfile.objects.filter(user_p=self.request.user).get()
        return context

    def get_queryset(self):
        return Work.objects.filter(assigned_work=None).order_by('-date_work')

    def test_func(self):
        worker=WorkerProfile.objects.filter(user_p=self.request.user)
        if worker.count()!=0:
            return True
        return False


class WorkDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Work
    template_name = 'work_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a=ClientProfile.objects.filter(user_p=self.request.user)
        if a.count()!=0:
            context["client"] = True
            class AssignedForm(forms.Form): job_done = forms.NullBooleanField(label='is the job done?')
            context["UserProfile"] = a.get()
        else:
            context["client"] = False
            class AssignedForm(forms.Form):
                assign_to_self = forms.NullBooleanField(label='want the job?')
                paid_for = forms.NullBooleanField(label='has the client paid up?')
            context["UserProfile"] = WorkerProfile.objects.filter(user_p=self.request.user).get()
        context["form"] = AssignedForm
        return context

    def post(self, request, pk, **kwargs):
        object = Work.objects.filter(pk=pk).get()
        a = ClientProfile.objects.filter(user_p=self.request.user)
        if a.count() != 0:
            on = request.POST['job_done']
            if on == "true": object.done_work = True
            else: object.done_work = False
        else:
            wp=WorkerProfile.objects.filter(user_p=self.request.user).get()
            on = request.POST['assign_to_self']
            if on == "true": object.assigned_work = wp
            else: object.assigned_work = None

            on = request.POST['paid_for']
            if object.assigned_work==wp and on == "true": object.Paid_work = True
            elif object.assigned_work==wp: object.Paid_work = False

        object.save()
        from django.shortcuts import redirect
        return redirect('work-detail', pk=pk)

    def test_func(self):
        a=ClientProfile.objects.filter(user_p=self.request.user)
        is_worker = a.count()==0
        if is_worker or a.get().user_p==self.request.user:
            return True
        return False


class WorkDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Work
    template_name = "base_panel/work_confirm_delete.html"

    def get_success_url(self):
        return reverse('base-panel')

    def test_func(self):
        work = self.get_object()
        if work.client_work.user_p == self.request.user:
            return True
        return False
