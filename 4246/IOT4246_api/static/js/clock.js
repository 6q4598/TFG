// Digital clock.
const time = document.getElementById('time');
const dayWeekend = document.getElementById('day');
const date = document.getElementById('date');

const dayWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

const interval = setInterval(() => {

    const local = new Date();
    let day = local.getDate(),
    month = local.getMonth(),
    year = local.getFullYear();
    dayWeekc = local.getDay()

    // Put the date in the HTML layout.
    time.innerHTML = local.toLocaleTimeString();
    dayWeekend.innerHTML = `${dayWeek[dayWeekc]}`;
    date.innerHTML = `${day}/${month}/${year}`;
    
}, 1000);

// Data picker.
