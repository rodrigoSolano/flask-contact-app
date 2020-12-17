const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete) {
    const btn_array = Array.from(btnDelete);
    btn_array.forEach((btn) => {
        btn.addEventListener('Click', () => {
            if (!confirm('Are you sure')) {
                e.preventDefault();
            }
        });
    });
}