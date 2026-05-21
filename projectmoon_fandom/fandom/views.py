from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

from .forms import AnomaliesForm
from .models import Anomalies, EGO, MediaFiles

def anomalie_list(request):
    anomalies = Anomalies.objects.filter(removed=False)
    return render(request, 'fandom/list.html', {'anomalies': anomalies})

def anomalie_detail(request, pk):
    anomalie = get_object_or_404(Anomalies, pk=pk, removed=False)
    return render(request, 'fandom/detail.html', {'anomalie': anomalie})


def create_anomalie(request):
    if request.method == "POST":
        form = AnomaliesForm(request.POST, request.FILES)
        if form.is_valid():
            anomalie = Anomalies.objects.create(
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code'],
                risk_level=form.cleaned_data['risk_level'],
                description=form.cleaned_data['description'],
            )
            if form.cleaned_data.get('ego_name') and form.cleaned_data.get('ego_slot'):
                EGO.objects.create(
                    anomaly=anomalie,
                    name=form.cleaned_data['ego_name'],
                    slot=form.cleaned_data['ego_slot'],
                    effect=form.cleaned_data.get('ego_effect', '')
                )
            if form.cleaned_data.get('image_file'):
                MediaFiles.objects.create(
                    anomaly=anomalie,
                    title=form.cleaned_data.get('image_title', ''),
                    file=form.cleaned_data['image_file']
                )
            messages.success(request, f'Аномалия "{anomalie.name}" успешно создана.')
            return redirect(reverse('fandom:anomalie_detail', args=[anomalie.pk]) + '?created=1')
        else:
            pass
    else:
        form = AnomaliesForm()
    return render(request, 'fandom/create.html', {'form': form})

def anomalie_edit(request, pk):
    anomalie = get_object_or_404(Anomalies, pk=pk, removed=False)
    if request.method == 'POST':
        form = AnomaliesForm(request.POST, request.FILES)
        if form.is_valid():
            anomalie.name = form.cleaned_data['name']
            anomalie.code = form.cleaned_data['code']
            anomalie.risk_level = form.cleaned_data['risk_level']
            anomalie.description = form.cleaned_data['description']
            anomalie.save()

            if form.cleaned_data.get('ego_name') and form.cleaned_data.get('ego_slot'):
                anomalie.ego_gifts.all().delete()
                EGO.objects.create(
                    anomaly=anomalie,
                    name=form.cleaned_data['ego_name'],
                    slot=form.cleaned_data['ego_slot'],
                    effect=form.cleaned_data.get('ego_effect', '')
                )
            else:
                anomalie.ego_gifts.all().delete()

            if form.cleaned_data.get('image_file'):
                anomalie.images.all().delete()
                MediaFiles.objects.create(
                    anomaly=anomalie,
                    title=form.cleaned_data.get('image_title', ''),
                    file=form.cleaned_data['image_file']
                )

            messages.success(request, f'Аномалия "{anomalie.name}" успешно обновлена.')
            return redirect(reverse('fandom:anomalie_detail', args=[anomalie.pk]) + '?updated=1')
        else:
            messages.error(request, 'Ошибка редактированиия. Проверьте форму.')
    else:
        initial_data = {
            'name': anomalie.name,
            'code': anomalie.code,
            'risk_level': anomalie.risk_level,
            'description': anomalie.description,
        }
        ego = anomalie.ego_gifts.first()
        if ego:
            initial_data.update({
                'ego_name': ego.name,
                'ego_slot': ego.slot,
                'ego_effect': ego.effect,
            })
        image = anomalie.images.first()
        if image:
            initial_data['image_title'] = image.title
        form = AnomaliesForm(initial=initial_data)
    return render(request, 'fandom/edit.html', {'form': form, 'anomalie': anomalie})

def anomalie_delete(request, pk):
    anomalie = get_object_or_404(Anomalies, pk=pk, removed=False)
    if request.method == 'POST':
        anomalie.removed = True
        anomalie.save()
        messages.success(request, f'Аномалия "{anomalie.name}" помечена как удалённая.')
        return redirect(reverse('fandom:anomalie_list') + '?deleted=1')
    return render(request, 'fandom/confirm_delete.html', {'anomalie': anomalie})


def check_code_uniqueness(request):
    code = request.GET.get('code', None)
    code_exists = Anomalies.objects.filter(code__iexact=code).exists()
    return JsonResponse({'is_taken': code_exists})


def delete_anomaly_ajax(request, pk):
    anomaly = get_object_or_404(Anomalies, pk=pk)
    anomaly.removed = True
    anomaly.save()
    return JsonResponse({'success': True})