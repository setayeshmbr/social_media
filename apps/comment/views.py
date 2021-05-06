from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView

from apps.comment.models import Comment


class DeleteComment(DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        slug = kwargs.get('slug')
        return reverse_lazy('blog:post_detail', kwargs={'slug' : slug})


