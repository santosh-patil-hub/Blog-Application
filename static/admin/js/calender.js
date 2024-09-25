// static/calendar/js/calendar.js

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid', 'interaction'],
        editable: true,
        selectable: true,
        events: '{% url "event_list" %}',
        select: function (info) {
            // Open add event modal
            var form = document.getElementById('myForm');
            document.getElementById('start-date').value = info.startStr;
            document.getElementById('end-date').value = info.endStr || '';
            document.getElementById('form').classList.add('show');
        },
        eventClick: function (info) {
            // Handle event click to edit or delete
            // For simplicity, we'll use a prompt; you can use a modal instead.
            if (confirm('Do you want to edit or delete this event?')) {
                // Add your logic for editing or deleting
            }
        }
    });

    calendar.render();
});
