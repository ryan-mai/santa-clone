const letterImage = document.querySelector('.letter-image');
const body = document.body;
const cancelBtn = document.querySelector('.cancel-btn');
const form = document.querySelector('form');

if (!letterImage || !form) console.error('How did we even get here??')

letterImage.addEventListener('click', () => {
    if (letterImage.classList.contains('expanded')) return;
    letterImage.classList.add('expanded');
    body.classList.add('blurred');
});

cancelBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (!letterImage.classList.contains('expanded')) return;
    e.stopPropagation();
    letterImage.classList.remove('expanded');
    body.classList.remove('blurred');
});

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    if (!letterImage.classList.contains('expanded')) return;

    const formData = new FormData(form);

    try {
        const res = await fetch(form.action, {
            method: form.method || 'POST',
            body: formData,
        });

        if (!res.ok) {
            alert('Santa could not get your message! Try again please!')
            return;
        }

        letterImage.classList.remove('expanded');
        body.classList.remove('blurred');

        await new Promise(r => setTimeout(r, 600));

        letterImage.classList.add('fly');

        await new Promise(resolve => {
            const timeout = setTimeout(() => {
                letterImage.removeEventListener('transitionend', finished);
                resolve();
            }, 1400);

            function finished(e) {
                if (e.target === letterImage) {
                    clearTimeout(timeout);
                    letterImage.removeEventListener('transitionend', finished);
                    resolve();
                }
            }

            letterImage.addEventListener('transitionend', finished);
        });

        window.location.href = '/';
    } catch (err) {
        alert('Oopsies! Santa is busy');
    }
})

document.body.addEventListener('click', () => {
    const audio = document.getElementById('bg-music');
    audio.volume = 0.167 // 676767
    audio.play().catch(e => console.log("Can't play santa's music :(", e));
}, { once: false });