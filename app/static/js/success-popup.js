// static/js/success-popup.js
// Auto-show success popup + auto-close after 10 seconds

document.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('successPopup');
    const overlay = document.getElementById('popupOverlay');
    const closeBtn = document.getElementById('closePopup');

    // Only run if popup exists and has data
    if (!popup || !popup.dataset.date) return;

    // Extract data
    const date = popup.dataset.date || '—';
    const doctor = popup.dataset.doctor || '—';

    // Update content
    document.getElementById('popupDate').textContent = date;
    document.getElementById('popupDoctor').textContent = doctor;

    // Show popup
    popup.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scroll

    // Auto-close after 10 seconds
    const autoCloseTimer = setTimeout(closePopup, 10000);

    // Manual close
    function closePopup() {
        popup.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        clearTimeout(autoCloseTimer);
    }

    closeBtn.addEventListener('click', closePopup);
    overlay.addEventListener('click', closePopup);

    // Optional: Press Escape to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePopup();
    });

    // Show countdown (optional — beautiful touch)
    let secondsLeft = 10;
    const countdownEl = document.createElement('p');
    countdownEl.className = 'text-sm text-gray-600 mt-3';
    countdownEl.innerHTML = `Closing in <strong>${secondsLeft}</strong> seconds...`;
    document.querySelector('.success-message').appendChild(countdownEl);

    const countdownInterval = setInterval(() => {
        secondsLeft--;
        countdownEl.innerHTML = `Closing in <strong>${secondsLeft}</strong> seconds...`;
        if (secondsLeft <= 0) {
            clearInterval(countdownInterval);
            countdownEl.remove();
        }
    }, 1000);

    // Clean up on close
    popup.addEventListener('transitionend', () => {
        if (!popup.classList.contains('active')) {
            clearInterval(countdownInterval);
            countdownEl.remove();
        }
    });
});