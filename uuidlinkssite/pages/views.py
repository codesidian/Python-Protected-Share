from django.shortcuts import redirect, render
from pages.models import Page
import markdown
from .forms import PageForm, CreatePage
from common.crypt import (
    decrypt_page,
    get_derived_key,
    verify_key,
)


# Create your views here.
def default_view(request):
    context = {}
    return render(request, "home.html", context)


def submit_view(request):
    # Initiate your form
    page_form = CreatePage(request.POST or None)

    if request.method == "POST" and page_form.is_valid():
        password = page_form.cleaned_data["password"].strip()
        title = page_form.cleaned_data["title"]
        template = page_form.cleaned_data["template"]

        page_obj = Page(
            title=title,
            template=None,
            salt=None,
            hash=None,
        )
        page_id = page_obj.uuid
        page_obj.save(password=password, template_block=template)
        request.session[str(page_id)] = get_derived_key(
            page_id, password
        ).decode("utf8")
        return redirect("page_view", page_id=page_id)

    context = {"form": page_form}

    return render(request, "submit.html", context)


def page_view(request, page_id):
    key = request.session.get(str(page_id), None)
    if not key:
        page_form = PageForm(request.POST or None)
        if request.method == "POST":
            if page_form.is_valid():
                password = page_form.cleaned_data["password"]
                key = get_derived_key(page_id, password).decode("utf-8")
                if verify_key(page_id, key):
                    request.session[str(page_id)] = key
                    return __render_page(request, page_id)
        context = {"page_uuid": page_id, "form": page_form}
        return render(request, "password.html", context)
    else:
        return __render_page(request, page_id)


def __render_page(request, page_id):
    page_obj = Page.objects.get(uuid=page_id)
    key = request.session[str(page_id)]
    if verify_key(page_id, key):
        t = decrypt_page(page_id, key)
        context = {
            "page_uuid": page_id,
            "template": markdown.markdown(t),
            "title": page_obj.title,
        }
        return render(request, "template.html", context)
    else:
        request.session[str(page_id)] = None
        return redirect("page_view", page_id=page_id)


def delete_page(request, page_id):
    key = request.session[str(page_id)]
    if verify_key(page_id, key):
        page_to_delete = Page.objects.get(uuid=page_id)
        page_to_delete.delete()


def recent_view(request):
    pages = []
    i = 0
    for p in Page.objects.order_by("-created"):
        pages.append({"uuid": p.uuid, "title": p.title})
        i += 1
        if i >= 100:
            break
    context = {"pages": pages}
    return render(request, "all.html", context)
