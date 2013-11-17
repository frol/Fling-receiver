from coffin.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .forms import FlingReceiverAddForm, FlingReceiverEditForm
from .models import FlingReceiver


def root(request, template_name='root.html'):
    return TemplateResponse(request, template_name)

@login_required
def fling_receiver_list(request, template_name='fling_receiver/fling_receiver_list.html'):
    fling_receiver_list = FlingReceiver.objects.filter(user=request.user)
    return TemplateResponse(request, template_name, {'fling_receiver_list': fling_receiver_list})

@login_required
def fling_receiver_add(request, form_class=FlingReceiverAddForm,
        template_name='fling_receiver/fling_receiver_add.html'):
    form = form_class(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        form.save()
        return redirect('fling_receiver_list')
    return TemplateResponse(request, template_name, {'form': form})

@login_required
def fling_receiver_edit(request, fling_receiver_id, form_class=FlingReceiverEditForm,
        template_name='fling_receiver/fling_receiver_edit.html'):
    fling_receiver = get_object_or_404(FlingReceiver, id=fling_receiver_id, user=request.user)
    form = form_class(request.POST or None, instance=fling_receiver)
    if form.is_valid():
        form.save()
        return redirect('fling_receiver_list')
    return TemplateResponse(request, template_name,
        {'fling_receiver': fling_receiver, 'form': form})

@login_required
def fling_receiver_predelete(request, fling_receiver_id,
        template_name='fling_receiver/fling_receiver_predelete.html'):
    fling_receiver = get_object_or_404(FlingReceiver, id=fling_receiver_id, user=request.user)
    return TemplateResponse(request, template_name, {'fling_receiver': fling_receiver})

@login_required
def fling_receiver_delete(request):
    try:
        fling_receiver_id = int(request.POST['fling_receiver_id'])
    except (KeyError, ValueError):
        raise Http404
    fling_receiver = get_object_or_404(FlingReceiver, id=fling_receiver_id, user=request.user)
    fling_receiver.delete()
    return redirect('fling_receiver_list')

def fling_receiver_template(request, secret_key,
        template_name='fling_receiver/fling_receiver_template.html'):
    fling_receiver = get_object_or_404(FlingReceiver, secret_key=secret_key)
    return TemplateResponse(request, template_name, {'fling_receiver': fling_receiver})
