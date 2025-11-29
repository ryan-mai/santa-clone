const inner = document.querySelector('.inner');
let isDragging = false
let initialX = 0;
let rotation = 0;
const dragSpeed = 0.5;

inner.addEventListener("mousedown", (e) => {
    isDragging = true;
    initialX = e.clientX;
    inner.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - initialX;
    rotation += (dx * dragSpeed);
    inner.style.transform = `perspective(500px) rotateX(-15deg)
                rotateY(${rotation})`;
    initialX = e.clientX;
});

document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    inner.style.cursor = "grab"
});

inner.style.userSelect = 'none';
inner.style.cursor = 'grab';

