const letter = document.querySelector('.letter-image');
const textarea = letter.querySelector('.letter-textarea');
letter.addEventListener('click', (e) => {
    letter.classList.toggle('expanded');
    if (letter.classList.contains('expanded')) textarea.focus();
});