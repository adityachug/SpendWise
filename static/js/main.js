// main.js — students will add JavaScript here as features are built

// Video Modal Functionality
(function() {
    const modal = document.getElementById('videoModal');
    const openBtn = document.getElementById('openVideoBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const videoFrame = document.getElementById('videoFrame');

    // YouTube video URL (placeholder - Spendly demo)
    const videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    // Open modal
    if (openBtn) {
        openBtn.addEventListener('click', function() {
            modal.classList.add('active');
            videoFrame.src = videoUrl;
            document.body.style.overflow = 'hidden';
        });
    }

    // Close modal function
    function closeModal() {
        modal.classList.remove('active');
        videoFrame.src = '';
        document.body.style.overflow = '';
    }

    // Close on close button click
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    // Close on overlay click (outside modal)
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
