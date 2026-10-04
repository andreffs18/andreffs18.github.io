document.addEventListener('DOMContentLoaded', () => {
    if (typeof bootstrap === 'undefined') return;
    document.querySelectorAll('[data-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el, { placement: el.dataset.placement || 'top' });
    });
});
