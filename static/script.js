const wrapper = document.querySelector('.wrapper');
const inner = document.querySelector('.inner');
let isDragging = false
let initialX = 0;
let rotation = 0;
const dragSpeed=  0.25;
const baseSpeed = 0.25;
let currentSpeed = baseSpeed;
let aniId;

function animate() {
    rotation += currentSpeed;
    inner.style.setProperty('--rotation', `${rotation}deg`);
    aniId = requestAnimationFrame(animate);
}

animate();

wrapper.addEventListener('mouseenter', () => {
    currentSpeed = baseSpeed / 1.5;
})

wrapper.addEventListener('mouseleave', () => {
    currentSpeed = baseSpeed;
})

inner.addEventListener("mousedown", (e) => {
    isDragging = true;
    initialX = e.clientX;
    inner.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - initialX;
    rotation += (dx * dragSpeed);
    inner.style.setProperty('--rotation', `${rotation}deg`);
    initialX = e.clientX;
});

document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    inner.style.cursor = "grab";
});

inner.style.userSelect = 'none';
inner.style.cursor = 'grab';