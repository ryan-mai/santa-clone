(() => {
    const chars = Array.from(document.querySelectorAll('.concept-four .char'));
    if (!chars.length) return;

    const layout = chars.map(c => c.textContent).join('');
    const groups = layout.split(':');
    const groupRanges = [];
    let idx = 0;

    for (let i = 0; i < groups.length; i++) {
        groupRanges.push({ start: idx, len: groups[i].length });
        idx += groups[i].length + 1;
    }

    function getChristmas() {
        const now = new Date();
        const thisYear = new Date(now.getFullYear(), 11, 25, 0, 0, 0, 0)
        if (now >= thisYear) {
            return new Date(now.getFullYear() + 1, 11, 25, 0, 0, 0, 0);
        }
        return thisYear;
    }

    let christmas = getChristmas();

    function format(num, len) {
        const s = String(num);
        if (s.length === len) return s;
        if (s.length < len) return s.padStart(len, '0');
        return s.slice(-len);
    }

    function updateStr(str) {
        const arr = str.split('');
        if (arr.length !== chars.length) return;
        for (let k = 0; k < chars.length; k++){
            chars[k].textContent = arr[k];
        }
    }

    function update() {
        const now = new Date();
        let diff = christmas - now;
        if (diff <= 0) {
            const reached = groups.map(g => '0'.repeat(g.length));
            updateStr(reached);
            clearInterval(intervalId);
            return;
        }

        const total = Math.floor(diff / 1000);
        const days = Math.floor(total / 86400);
        const hours = Math.floor((total % 86400) / 3600);
        const minutes = Math.floor((total % 3600) / 60);
        const seconds = total % 60;
        const values = [days, hours, minutes, seconds];

        const out = groups.map((g, i) => {
            return format(values[i] ?? 0, g.length);
        });

        updateStr(out.join(':'));
    }

    update();
    const intervalId = setInterval(update, 1000);

    setInterval(() => {
        const now = new Date();
        if (now > christmas) christmas = getChristmas();
    }, 60 * 1000);
})();