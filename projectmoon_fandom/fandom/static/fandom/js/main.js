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

    function showSticker(text, duration = 3000) {
        const sticker = document.createElement('div');
        sticker.className = 'sticker';
        sticker.innerText = text;
        document.body.appendChild(sticker);
        setTimeout(() => sticker.remove(), duration);
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
    const codeField = document.querySelector('#id_code');
    if (codeField) {
        codeField.addEventListener('blur', function() {
            const isFormatValid = validateAnomalyCode(this);
            const codeValue = this.value.trim();

            if (isFormatValid && codeValue !== '') {
                fetch(`/anomalies/check-code/?code=${codeValue}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_taken) {
                            codeField.classList.add('error-input');
                            showSticker('Ошибка: этот код аномалии уже занят!', 4000);
                        }
                    })
                    .catch(error => console.error('Ошибка AJAX-запроса:', error));
            }
        });

        codeField.addEventListener('input', function() {
            this.classList.remove('error-input');
        });
    }
    const deleteButtons = document.querySelectorAll('.ajax-delete-btn');

deleteButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        // Отменяем стандартное поведение ссылки (чтобы страница не перезагружалась)
        event.preventDefault();

        // Читаем ID аномалии из атрибута data-id
        const anomalyId = this.getAttribute('data-id');

        if (confirm('Вы уверены, что хотите удалить эту аномалию?')) {
            // Отправляем скрытый запрос на сервер Django
            fetch(`/anomalies/${anomalyId}/delete-ajax/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Находим строку таблицы по её уникальному ID
                        const rowToDelete = document.getElementById(`anomalie-row-${anomalyId}`);
                        if (rowToDelete) {
                            // Эффектное динамическое изменение стиля (строка бледнеет перед удалением)
                            rowToDelete.style.transition = 'opacity 0.5s ease';
                            rowToDelete.style.opacity = '0';

                            // Ждем 500 миллисекунд, пока анимация закончится, и удаляем из DOM
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