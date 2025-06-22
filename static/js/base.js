document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('main-navbar');
    const scrollLogo = document.getElementById('scroll-logo');

    document.addEventListener('scroll', () => {
        const scrollY = window.scrollY;

        if (scrollY > 60) {
            navbar.classList.add('show-logo');
            scrollLogo?.classList.remove('d-none');
        } else {
            navbar.classList.remove('show-logo');
            scrollLogo?.classList.add('d-none');
        }
    });

    // Auto-dismiss alert messages after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    const excludedClasses = ['no-auto-dismiss'];

    if (alerts.length > 0 && !alerts[0].classList.contains('no-auto-dismiss')) {
        setTimeout(() => {
            alerts.forEach(alert => {
                if (!excludedClasses.some(cls => alert.classList.contains(cls))) {
                    alert.classList.add('fade');
                    setTimeout(() => {
                        alert.remove();
                    }, 500);
                }
            });
        }, 3000);
    }

    // Max images upload limit
    // Ensure the input file elements are set to allow multiple files
    //<input type="file" class="form-control" id="image-upload" multiple accept="image/*" data-preview-container="image-grid">
    document.addEventListener('DOMContentLoaded', () => {
        const MAX_IMAGES = 8;

        document.querySelectorAll('input[type="file"][multiple]').forEach(input => {
            input.addEventListener('change', function () {
                const containerId = this.dataset.previewContainer || 'image-grid';
                const existingImages = document.querySelectorAll(`#${containerId} .draggable-image`).length;
                const newFiles = Array.from(this.files);

                if (existingImages + newFiles.length > MAX_IMAGES) {
                    alert(`You can only upload up to ${MAX_IMAGES} images in total.`);
                    this.value = "";
                }
            });
        });
    });

});
