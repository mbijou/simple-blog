from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from post.models import Post
from django.http import JsonResponse
from django.core import serializers
import json
import base64


class PostExportView(View):
    def get(self, request, *args, **kwargs):
        post_instance = get_object_or_404(Post, slug_title=kwargs.get("title"))
        response = self.get_json_export(post_instance)
        return response

    def get_json_export(self, post_instance):
        return self.build_json_export(post_instance)

    def build_json_export(self, post_instance):
        json_string_as_list = serializers.serialize("json", [post_instance])
        json_data = json.loads(json_string_as_list)[0]
        content_set = self.build_content_set(post_instance)
        json_data["fields"]["content_set"] = content_set
        json_response = JsonResponse(json_data)
        return json_response

    def build_content_set(self, post_instance):
        content_set = []

        for content_instance in post_instance.content_set.all():
            json_string_as_list = serializers.serialize("json", [content_instance])
            content_json_data = json.loads(json_string_as_list)[0]
            content_set.append(content_json_data)

            image = content_instance.get_image()

            encoded_image_string = None

            if image:
                encoded_image_string = str(base64.b64encode(image.image_file.read()), "utf-8")

            content_json_data["fields"]["image"] = encoded_image_string
        return content_set
