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


# class FollowFormMixin():
#     def form_valid(self,form):
#         self.obj = form.save(commit=False)
#         self.obj.from_user = self.request.user
#
#         self.obj.to_user = get_object_or_404(MyUser,self.request.kwargs.get('user_name'))
#         self.obj.save()
#         return super().form_valid(form)




