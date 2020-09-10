from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from post.models import Post
from django.utils import translation


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context()

        instance = context.get("post")
        language_group = instance.language_group

        language_code = instance.language_code

        if language_code != translation.get_language():
            redirect_to_other_language = get_redirect_to_other_language(language_group, translation.get_language())

            if redirect_to_other_language:
                return redirect_to_other_language

            context["post"] = None

        return render(request, "blog/detail.html", context)

    def get_context(self):
        instance = self.get_instance()

        title = self.kwargs.get("title")

        post_language = self.get_post_language(instance)
        post_image = self.get_post_image(instance)

        return {
            "post": instance, "title": title, "post_language": post_language, "post_image": post_image
        }

    def get_instance(self):
        title = self.kwargs.get("title")

        if title:
            instance = get_post_from_all_languages(title)
            return instance

    @staticmethod
    def get_post_language(post: Post):
        if post is not None:
            return post.language_code

    @staticmethod
    def get_post_image(post: Post):
        return post.post_image


def get_post_from_all_languages(title):
    try:
        post = Post.objects_from_all_languages.get(slug_title=title)
        return post
    except Post.DoesNotExist:
        raise Http404('No %s matches the given query.' % Post._meta.object_name)


def get_redirect_to_other_language(language_group, language_code):
    if language_group is not None:
        try:
            language_instance = get_object_or_404(Post, language_group=language_group, language_code=language_code)
            return HttpResponseRedirect(
                reverse_lazy("blog:post-detail", kwargs={"title": language_instance.slug_title}))
        except Post.DoesNotExist:
            pass
