from django.shortcuts import redirect, get_object_or_404

from apps.account.models import MyUser


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['title', 'image', 'caption', 'location', 'status', 'category']
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user

        if not self.obj.status == 'a':
            self.obj.status = 'p'

        return super().form_valid(form)


class PostUpdateFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['title', 'caption', 'location', 'status', 'category']
        return super().dispatch(request, *args, **kwargs)



