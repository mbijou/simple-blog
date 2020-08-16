from post.models import Content, image_choice


def save_image_form(content_instance: Content, image_form, transaction):
    if content_instance.type == image_choice:
        image_form.instance.content = content_instance

        if image_form.is_valid() is True:
            image_form.save()
        else:
            print(image_form.errors)
            transaction.set_rollback(True)
        print(f'www:{image_form.is_valid()}')
