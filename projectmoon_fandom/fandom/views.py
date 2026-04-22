from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AnomaliesForm
from .models import Anomalies, EGO, MediaFiles


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
                    anomalie=anomalie,
                    name=form.cleaned_data['ego_name'],
                    slot=form.cleaned_data['ego_slot'],
                    effect=form.cleaned_data.get('ego_effect', '')
                )

            if form.cleaned_data.get('image'):
                MediaFiles.objects.create(
                    anomalie=anomalie,
                    title=form.cleaned_data.get('title', ''),
                    file=form.cleaned_data['image']
                )

            messages.success(request, f'Аномалия "{anomalie.name}" успешно создана.')
            return redirect('anomalie_detail', pk=anomalie.pk)
        else:
            messages.error(request, 'Ошибка при создании аномалии. Проверьте введённые данные.')
    else:
        form = AnomaliesForm()

    return render(request, 'fandom/create.html', {'form': form})


def anomalie_edit(request, pk):
    anomalie = get_object_or_404(Anomalies, pk=pk)

    if request.method == 'POST':
        form = AnomaliesForm(request.POST, request.FILES)
        if form.is_valid():
            anomalie.name = form.cleaned_data['name']
            anomalie.code = form.cleaned_data['code']
            anomalie.risk_level = form.cleaned_data['risk_level']
            anomalie.description = form.cleaned_data['description']
            anomalie.save()

            anomalie.ego_gifts.all().delete()
            if form.cleaned_data.get('ego_name') and form.cleaned_data.get('ego_slot'):
                EGO.objects.create(
                    anomalie=anomalie,
                    name=form.cleaned_data['ego_name'],
                    slot=form.cleaned_data['ego_slot'],
                    effect=form.cleaned_data.get('ego_effect', '')
                )


            if form.cleaned_data.get('media_file'):
                MediaFiles.objects.create(
                    anomalie=anomalie,
                    title=form.cleaned_data.get('media_title', ''),
                    file=form.cleaned_data['media_file']
                )

            messages.success(request, f'Аномалия "{anomalie.name}" успешно обновлена.')
            return redirect('anomalie_detail', pk=anomalie.pk)
        else:
            messages.error(request, 'Ошибка при редактировании. Проверьте форму.')
    else:

        initial_data = {
            'name': anomalie.name,
            'code': anomalie.code,
            'risk_level': anomalie.risk_level,
            'description': anomalie.description,
        }
        if anomalie.ego_gifts.exists():
            ego = anomalie.ego_gifts.first()
            initial_data['ego_name'] = ego.name
            initial_data['ego_slot'] = ego.slot
            initial_data['ego_effect'] = ego.effect
        form = AnomaliesForm(initial=initial_data)

    return render(request, 'fandom/edit.html', {'form': form, 'anomalie': anomalie})


def anomalie_delete(request, pk):
    anomalie = get_object_or_404(Anomalies, pk=pk)
    anomalie.removed = True
    anomalie.save()
    messages.success(request, f'Аномалия "{anomalie.name}" помечена как удалённая.')
    return redirect('anomalie_list')


def anomalie_list(request):
    anomalies = Anomalies.objects.filter(removed=False)
    return render(request, 'fandom/list.html', {'anomalies': anomalies})