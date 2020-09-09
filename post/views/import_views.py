from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from post.forms import PostImportForm, PostForm
from django.db import transaction
from django.core import serializers
import json
from django.forms.models import model_to_dict
import base64
from post.models import Post, Content
from content.models import Image
import io
from django.core.files.base import ContentFile
from django.core.files import File  # you need this somewhere


class PostImportView(LoginRequiredMixin, View):
    form = None

    def get(self, request, title=None):
        form = PostImportForm()
        return render(request, template_name="post/import.html", context={"form": form})

    @transaction.atomic
    def post(self, request, title=None):
        form = PostImportForm(request.POST, files=request.FILES)

        if form.is_valid() is True:
            print("VALID")
            json_data_string = form.cleaned_data.get("file").read()
            json_data = json.loads(json_data_string)
            json_data["pk"] = None

            content_set = json_data["fields"].pop("content_set")

            json_data_string = json.dumps([json_data])

            deserialized_object = next(serializers.deserialize("json", json_data_string))
            instance = deserialized_object.object
            instance.slug_title = None

            instance.author = request.user
            data = model_to_dict(instance)

            post_form = PostForm(data)

            if post_form.is_valid() is True:
                instance = post_form.save()

                for content_json in content_set:
                    content_json["pk"] = None
                    content_json["fields"]["post"] = instance
                    # content_json["fields"]["sequence"] = None

                    image_base64_string = None

                    if content_json["fields"]["image"]:
                        image_base64_string = content_json["fields"]["image"]
                        content_json["fields"]["image"] = None

                    content_instance = Content.objects.create(**content_json["fields"])

                    if image_base64_string:
                        image = Image.objects.create(
                            content=content_instance)
                        image.image_file.save("", content=ContentFile(base64.b64decode(image_base64_string)))
                        print(content_json)
                        print(image.image_file)

                    instance.content_set.add(content_instance)

                return HttpResponseRedirect(
                    reverse_lazy("blog:post-detail", kwargs={"title": instance.slug_title}))
            else:
                return render(request, template_name="post/import.html", context={"form": form, "post_form": post_form})
