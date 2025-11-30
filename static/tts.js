const letterImage = document.querySelector('.letter-image');
const body = document.body;
const cancelBtn = document.querySelector('.cancel-btn');

letterImage.addEventListener('click', () => {
    if (letterImage.classList.contains('expanded')) return;
    letterImage.classList.add('expanded');
    body.classList.add('blurred');
});

cancelBtn.addEventListener('click', (e) => {
    if (!letterImage.classList.contains('expanded')) return;
    e.stopPropagation();
    letterImage.classList.remove('expanded');
    body.classList.remove('blurred');
});