document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('essay-form');
    const essay = document.getElementById('essay');
    const wordCount = document.getElementById('word-count');
    const submitBtn = document.getElementById('submit-btn');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    const loading = document.getElementById('loading');
    const grade = document.getElementById('grade');

    function updateWordCount() {
        const words = essay.value.trim().split(/\s+/).length;
        wordCount.textContent = `Word count: ${words}`;
        submitBtn.disabled = words < 50;
    }

    essay.addEventListener('input', updateWordCount);

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        result.classList.add('hidden');
        error.classList.add('hidden');
        loading.classList.remove('hidden');
        
        fetch('/grade', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'essay=' + encodeURIComponent(essay.value)
        })
        .then(response => response.json())
        .then(data => {
            loading.classList.add('hidden');
            if (data.error) {
                error.textContent = data.error;
                error.classList.remove('hidden');
            } else {
                grade.textContent = data.grade;
                result.classList.remove('hidden');
            }
        })
        .catch((error) => {
            loading.classList.add('hidden');
            error.textContent = 'An error occurred. Please try again.';
            error.classList.remove('hidden');
            console.error('Error:', error);
        });
    });

    updateWordCount();
});