// Countdown timer for quiz page
document.addEventListener('DOMContentLoaded', function() {
    var timerElem = document.getElementById('time');
    var form = document.getElementById('quiz-form');
    if (timerElem && form) {
        var timeLeft = 60;
        var interval = setInterval(function() {
            timeLeft--;
            timerElem.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(interval);
                form.submit();
            }
        }, 1000);
    }
});
