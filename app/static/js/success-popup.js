document.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('successPopup');
    const overlay = document.getElementById('popupOverlay');
    const date = popup?.dataset.date;
    const doctor = popup?.dataset.doctor;

    if (date) {
        document.getElementById('popupDate').textContent = date;
        document.getElementById('popupDoctor').textContent = doctor || 'Any Available Doctor';
        popup.style.display = 'block';
        overlay.style.display = 'block';
    }

    document.getElementById('closePopup')?.addEventListener('click', () => {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    });
});