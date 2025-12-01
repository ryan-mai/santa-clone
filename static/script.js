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


document.body.addEventListener('click', () => {
    const audio = document.getElementById('bg-music');
    audio.volume = 0.167 // 676767
    audio.play().catch(e => console.log("Can't play santa's music :(", e));
}, { once: false });

function snowfall() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.innerHTML = '❄';
    snowflake.style.left = Math.random() * 100 + 'vw';
    snowflake.style.animationDuration = Math.random() * 3 + 2 + 's';
    snowflake.style.opacity = Math.random() - 0.1;
    snowflake.style.fontSize = Math.random() * 10 + 10 + 'px';

    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 4000);

}

setInterval(snowfall, 200);

let prevSparkle = 0;
const SPARKLE_FREQ = 20;
let mouseX = null;
let mouseY = null;
const MAX_SPARKLES = 80;


document.addEventListener('mousemove', (e) => {
    if (isDragging) return;
    mouseX = e.clientY;
    mouseY = e.clientY;
});

document.addEventListener('mousemove', function(e) {
    if (isDragging) return;
    const now = performance.now();
    if (now - prevSparkle < SPARKLE_FREQ) return;
    prevSparkle = now;

    const sparkle = document.createElement('div');
    sparkle.classList.add('sparkle');

    mouseX = e.clientY;
    mouseY = e.clientY;



    const x = e.pageX + (Math.random() - 0.5) * 10;
    const y = e.pageY + (Math.random() - 0.5) * 10;

    sparkle.style.left = x + 'px';
    sparkle.style.top = y + 'px';
    sparkle.style.willChange = 'opacity, transform';
    sparkle.style.pointerEvents = 'none';

    document.body.appendChild(sparkle);
    setTimeout(() => {
        sparkle.remove();
    }, 800);
});