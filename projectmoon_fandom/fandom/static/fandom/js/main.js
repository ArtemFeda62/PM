function showSticker(text, duration = 3000) {
    const sticker = document.createElement('div');
    sticker.className = 'sticker';
    sticker.innerText = text;
    document.body.appendChild(sticker);
    setTimeout(() => sticker.remove(), duration);
}

document.addEventListener('DOMContentLoaded', function() {

    const upButton = document.createElement('button');
    upButton.innerText = '1';
    upButton.id = 'scrollUpBtn';
    upButton.title = 'Наверх';
    document.body.appendChild(upButton);

    window.addEventListener('scroll', function() {
        upButton.style.display = window.scrollY > 250 ? 'block' : 'none';
    });
    upButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    const openModalBtn = document.getElementById('openModalBtn');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModalBtn = document.getElementById('closeModalBtn');

    if (openModalBtn && modalOverlay && closeModalBtn) {
        openModalBtn.addEventListener('click', () => modalOverlay.style.display = 'flex');
        closeModalBtn.addEventListener('click', () => modalOverlay.style.display = 'none');
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) modalOverlay.style.display = 'none';
        });
    }
    setTimeout(() => showSticker('Добро пожаловать! Используйте подсказки справа.'), 2000);

    const slidePanel = document.getElementById('slideOutPanel');
    if (slidePanel) {
        slidePanel.addEventListener('click', (e) => {
            if (e.target.id === 'closePanelLink') {
                e.preventDefault();
                slidePanel.classList.remove('open');
            } else {
                slidePanel.classList.toggle('open');
            }
        });
        const panelContent = slidePanel.querySelector('.panel-content');
        if (panelContent) panelContent.addEventListener('click', (e) => e.stopPropagation());
    }

    function validateAnomalyCode(input) {
        const pattern = /^AN-\d{3}$/;
        const val = input.value.trim();
        if (val === '') return true;
        if (!pattern.test(val)) {
            showSticker('Неверный формат кода! Используйте AN-XXX (пример: AN-042)', 3000);
            input.classList.add('error-input');
            return false;
        } else {
            input.classList.remove('error-input');
            return true;
        }
    }

    const deleteButtons = document.querySelectorAll('.ajax-delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const anomalyId = this.getAttribute('data-id');
            if (confirm('Вы уверены, что хотите удалить эту аномалию?')) {
                fetch(`/anomalies/${anomalyId}/delete-ajax/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const rowToDelete = document.getElementById(`anomalie-row-${anomalyId}`);
                            if (rowToDelete) {
                                rowToDelete.style.transition = 'opacity 0.5s ease';
                                rowToDelete.style.opacity = '0';
                                setTimeout(() => {
                                    rowToDelete.remove();
                                    showSticker('Аномалия успешно перемещена в архив (удалена)!', 3000);
                                }, 500);
                            }
                        }
                    })
                    .catch(error => console.error('Ошибка при удалении:', error));
            }
        });
    });
    const params = new URLSearchParams(window.location.search);
    if (params.get('created') === '1') showSticker('Аномалия успешно создана!', 4000);
    if (params.get('updated') === '1') showSticker('Аномалия обновлена!', 4000);
    if (params.get('deleted') === '1') showSticker('Аномалия удалена.', 4000);
});

$(document).ready(function() {
    function checkAnomalyCodeDeferred(code) {
        var deferred = $.Deferred();
        $.ajax({
            url: '/anomalies/check-code/',
            data: { code: code },
            method: 'GET',
            dataType: 'json'
        })
        .done(function(response) {
            if (response.is_taken) {
                deferred.reject({ code: code, message: 'Этот код уже используется' });
            } else {
                deferred.resolve({ code: code, message: 'Код доступен' });
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            deferred.reject({ code: code, message: 'Ошибка сервера: ' + textStatus });
        });
        return deferred.promise();
    }

    var $codeField = $('#id_code');
    if ($codeField.length) {
        $codeField.off('blur');
        $codeField.on('blur', function() {
            var codeValue = $(this).val().trim();
            if (codeValue === '') return;

            var pattern = /^AN-\d{3}$/;
            if (!pattern.test(codeValue)) {
                showSticker('Неверный формат! Используйте AN-XXX', 3000);
                $(this).addClass('error-input');
                return;
            }

            var promise = checkAnomalyCodeDeferred(codeValue);
            promise
                .done(function(result) {
                    $codeField.removeClass('error-input');
                    showSticker('✓ ' + result.message, 2000);
                })
                .fail(function(error) {
                    $codeField.addClass('error-input');
                    showSticker('✗ ' + error.message, 4000);
                })
                .always(function() {
                    console.log('Проверка кода "' + codeValue + '" завершена');
                });
        });
    }
    function fetchSlowAnomalyData(anomalyId) {
        var deferred = $.Deferred();
        $.ajax({
            url: '/anomalies/slow-data/' + anomalyId + '/',
            method: 'GET',
            dataType: 'json',
            timeout: 10000
        })
        .done(function(response) {
            deferred.resolve(response);
        })
        .fail(function(xhr, status, error) {
            deferred.reject({ id: anomalyId, error: error || status });
        });
        return deferred.promise();
    }

    function showPreloader(show) {
        $('#preloader').css('display', show ? 'flex' : 'none');
    }

    function loadMultipleAnomalies(anomalyIds) {
        showPreloader(true);

        var requests = anomalyIds.map(function(id) {
            return fetchSlowAnomalyData(id);
        });

        $.when.apply($, requests)
            .done(function() {
                var results = Array.prototype.slice.call(arguments);
                console.log('Все данные загружены:', results);
                showSticker('Загружено ' + results.length + ' аномалий', 3000);
            })
            .fail(function() {
                showSticker('Один из запросов завершился ошибкой', 4000);
            })
            .always(function() {
                showPreloader(false);
            });
    }

    var currentPath = window.location.pathname;
    if (currentPath === '/anomalies/' || currentPath === '/') {
        var $table = $('table');
        if ($table.length) {
            var $btn = $('<button id="demoDeferredBtn" class="_urls"">Загрузить дополнительные данные</button>');
            $table.after($btn);

            $('#demoDeferredBtn').on('click', function() {
                var anomalyIds = [];
                $('table tbody tr').each(function(index) {
                    if (index < 3) {
                        var idText = $(this).find('td:first').text();
                        var id = parseInt(idText, 10);
                        if (!isNaN(id)) anomalyIds.push(id);
                    }
                });
                if (anomalyIds.length === 0) {
                    showSticker('Нет аномалий для загрузки', 2000);
                    return;
                }
                loadMultipleAnomalies(anomalyIds);
            });
        }
    }
});