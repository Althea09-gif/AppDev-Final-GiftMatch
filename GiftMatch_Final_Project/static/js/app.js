document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('[data-nav-toggle]');
    const navMenu = document.querySelector('[data-nav-menu]');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => navMenu.classList.toggle('show'));
    }

    const notificationToggle = document.querySelector('[data-notification-toggle]');
    const notificationPanel = document.querySelector('[data-notification-panel]');
    if (notificationToggle && notificationPanel) {
        notificationToggle.addEventListener('click', (event) => {
            event.stopPropagation();
            notificationPanel.classList.toggle('show');
        });
        document.addEventListener('click', (event) => {
            if (!notificationPanel.contains(event.target) && !notificationToggle.contains(event.target)) {
                notificationPanel.classList.remove('show');
            }
        });
    }

    const wizard = document.querySelector('[data-wizard]');
    if (wizard) {
        let step = 1;
        const steps = wizard.querySelectorAll('.wizard-step');
        const dots = wizard.querySelectorAll('.step-dot');
        const nextBtn = wizard.querySelector('[data-next]');
        const prevBtn = wizard.querySelector('[data-prev]');
        const submitBtn = wizard.querySelector('[data-submit]');
        const occasionSelect = wizard.querySelector('select[name="occasion_type"]');
        const recipientRadios = wizard.querySelectorAll('input[name="recipient_type"]');

        const occasionMap = {
            partner: ['anniversary', 'valentines', 'monthsary', 'birthday', 'christmas'],
            family: ['mothers_day', 'fathers_day', 'family_reunion', 'birthday', 'christmas', 'new_year'],
            friend: ['birthday', 'graduation', 'christmas', 'new_year'],
            coworker: ['birthday', 'promotion', 'retirement', 'christmas', 'graduation']
        };

        if (occasionSelect) {
            const originalOptions = Array.from(occasionSelect.options).map((option) => ({
                value: option.value,
                text: option.textContent
            }));
            const refreshOccasions = () => {
                const selectedRecipient = wizard.querySelector('input[name="recipient_type"]:checked')?.value || 'partner';
                const allowed = occasionMap[selectedRecipient] || originalOptions.map((o) => o.value);
                const previous = occasionSelect.value;
                occasionSelect.innerHTML = '';
                originalOptions
                    .filter((option) => allowed.includes(option.value))
                    .forEach((option) => {
                        const newOption = document.createElement('option');
                        newOption.value = option.value;
                        newOption.textContent = option.text;
                        occasionSelect.appendChild(newOption);
                    });
                if (allowed.includes(previous)) {
                    occasionSelect.value = previous;
                }
            };
            recipientRadios.forEach((radio) => radio.addEventListener('change', refreshOccasions));
            refreshOccasions();
        }

        const validateStep = () => {
            if (step === 1) return Boolean(wizard.querySelector('input[name="recipient_type"]:checked'));
            if (step === 2) return Boolean(occasionSelect?.value);
            if (step === 3) return wizard.querySelectorAll('input[name="interests"]:checked').length > 0;
            return true;
        };

        const showStep = (value) => {
            step = Math.max(1, Math.min(3, value));
            steps.forEach((el) => el.classList.toggle('active', Number(el.dataset.step) === step));
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index + 1 === step);
                dot.classList.toggle('done', index + 1 < step);
            });
            prevBtn.style.visibility = step === 1 ? 'hidden' : 'visible';
            nextBtn.classList.toggle('hidden', step === 3);
            submitBtn.classList.toggle('hidden', step !== 3);
        };
        nextBtn.addEventListener('click', () => {
            if (!validateStep()) return;
            showStep(step + 1);
        });
        prevBtn.addEventListener('click', () => showStep(step - 1));
        submitBtn.addEventListener('click', (event) => {
            if (!validateStep()) {
                event.preventDefault();
                alert('Please select at least one interest so GiftMatch can make accurate recommendations.');
            }
        });
        showStep(1);
    }

    const compareChecks = document.querySelectorAll('[data-compare-check]');
    const comparePanel = document.querySelector('[data-compare-panel]');
    const compareCount = document.querySelector('[data-compare-count]');
    const compareButton = document.querySelector('[data-compare-open]');
    const compareModal = document.querySelector('[data-compare-modal]');
    const compareBody = document.querySelector('[data-compare-body]');
    const compareClose = document.querySelector('[data-compare-close]');

    const selectedCompareItems = () => Array.from(compareChecks).filter((box) => box.checked);

    const updateComparePanel = () => {
        if (!comparePanel) return;
        const count = selectedCompareItems().length;
        comparePanel.classList.toggle('show', count > 0);
        if (compareCount) compareCount.textContent = count;
        if (compareButton) compareButton.disabled = count < 2;
    };

    compareChecks.forEach((box) => {
        box.addEventListener('change', () => {
            const selected = selectedCompareItems();
            if (selected.length > 3) {
                box.checked = false;
                alert('You can compare up to 3 gifts only.');
            }
            updateComparePanel();
        });
    });

    if (compareButton && compareModal && compareBody) {
        compareButton.addEventListener('click', () => {
            const rows = selectedCompareItems().map((box) => {
                const d = box.dataset;
                return `<tr>
                    <td><strong>${d.name}</strong></td>
                    <td>₱${d.price}</td>
                    <td>${d.store}</td>
                    <td>${d.score}%</td>
                    <td>${d.interest}</td>
                </tr>`;
            }).join('');
            compareBody.innerHTML = rows;
            compareModal.classList.add('show');
        });
    }
    if (compareClose && compareModal) {
        compareClose.addEventListener('click', () => compareModal.classList.remove('show'));
        compareModal.addEventListener('click', (event) => {
            if (event.target === compareModal) compareModal.classList.remove('show');
        });
    }
});
