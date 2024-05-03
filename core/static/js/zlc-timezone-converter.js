document.addEventListener('DOMContentLoaded', function() {
    const DateTime = luxon.DateTime;
    const Interval = luxon.Interval;

    function getNextEventDayDelta(now, eventDateTime, daysOfWeek) {
        // If today is an event day but we're past the event time, start from tomorrow
        let startDay = eventDateTime <= now && daysOfWeek.includes(now.weekday) ? now.plus({ days: 1 }) : now;

        // Find the next event day
        let nextEventDay = startDay;
        while (!daysOfWeek.includes(nextEventDay.weekday)) {
            nextEventDay = nextEventDay.plus({ days: 1 });
        }
        return nextEventDay.diff(now, 'days').days;
    }

    function formatCountdown(duration) {
        const parts = [];
        // Use Math.floor to round down to the nearest whole number
        const days = Math.floor(duration.days);
        const hours = Math.floor(duration.hours) % 24;
        const minutes = Math.floor(duration.minutes) % 60;
        const seconds = Math.floor(duration.seconds) % 60;

        if (days > 0) parts.push(`${days} ${days === 1 ? 'day' : 'days'}`);
        if (hours > 0 || days > 0) parts.push(`${hours} ${hours === 1 ? 'hour' : 'hours'}`);
        if (minutes > 0 || hours > 0 || days > 0) parts.push(`${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`);
        parts.push(`${seconds} ${seconds === 1 ? 'second' : 'seconds'}`);

        return parts.join(' ');
    }

    function updateEventTimes() {
        const now = DateTime.local();

        // Define the event times in IST
        const event1TimeIST = DateTime.fromObject({ hour: 7, minute: 30 }, { zone: 'Asia/Kolkata' });
        const event2TimeIST = DateTime.fromObject({ hour: 18, minute: 0 }, { zone: 'Asia/Kolkata' });

        // Calculate the next occurrence of the 7:30 AM event
        let event1NextOccurrence = event1TimeIST > now ? event1TimeIST : event1TimeIST.plus({ days: 1 });

        // Calculate the next occurrence of the 6:00 PM event, only on Monday, Wednesday, and Friday
        const event2DaysOfWeek = [1, 3, 5]; // Luxon's weekdays (1 is Monday, 5 is Friday)
        let event2NextOccurrence;
        if (event2DaysOfWeek.includes(now.weekday) && now < event2TimeIST) {
            event2NextOccurrence = event2TimeIST;
        } else {
            let daysUntilNextEvent = getNextEventDayDelta(now, event2TimeIST, event2DaysOfWeek);
            event2NextOccurrence = event2TimeIST.plus({ days: daysUntilNextEvent });
        }

        // Convert to local time for display
        const event1TimeLocal = event1NextOccurrence.toLocal();
        const event2TimeLocal = event2NextOccurrence.toLocal();

        document.getElementById('event-time-local').innerHTML = `${now.toLocaleString(DateTime.TIME_SIMPLE)}<br>${now.toLocaleString(DateTime.DATE_MED)}`;
        document.getElementById('event-time-ist').innerHTML = `${event1TimeLocal.toLocaleString(DateTime.TIME_SIMPLE)}<br>${event1TimeLocal.toLocaleString(DateTime.DATE_MED)}`;
        document.getElementById('cstm-event-time-local').innerHTML = `${now.toLocaleString(DateTime.TIME_SIMPLE)}<br>${now.toLocaleString(DateTime.DATE_MED)}`;
        document.getElementById('cstm-event-time-ist').innerHTML = `${event2TimeLocal.toLocaleString(DateTime.TIME_SIMPLE)}<br>${event2TimeLocal.toLocaleString(DateTime.DATE_MED)}`;

        // Update countdown display
        let event1CountdownDuration = Interval.fromDateTimes(now, event1TimeLocal).toDuration(['days', 'hours', 'minutes', 'seconds']);
        let event2CountdownDuration = Interval.fromDateTimes(now, event2TimeLocal).toDuration(['days', 'hours', 'minutes', 'seconds']);
        document.getElementById('time-remaining').innerHTML = "STARTS IN <br>" + formatCountdown(event1CountdownDuration);
        document.getElementById('cstm-time-remaining').innerHTML = formatCountdown(event2CountdownDuration);
    }
    updateEventTimes();
    function updateHeadings() {
        const now = DateTime.local();
        const event1TimeIST = DateTime.fromObject({ hour: 7, minute: 30 }, { zone: 'Asia/Kolkata' });
        const event2TimeIST = DateTime.fromObject({ hour: 18, minute: 0 }, { zone: 'Asia/Kolkata' });

        // Calculate the next occurrence of the events in the user's local timezone
        const event1TimeLocal = event1TimeIST.setZone(now.zoneName);
        const event2TimeLocal = event2TimeIST.setZone(now.zoneName);

        // Format the times for the headings
        const event1TimeFormatted = event1TimeLocal.toLocaleString(DateTime.TIME_SIMPLE);
        const event2TimeFormatted = event2TimeLocal.toLocaleString(DateTime.TIME_SIMPLE);

        // Update the heading texts
        const event1Heading = document.querySelector('.event1-heading');
        const event2Heading = document.querySelector('.event2-heading');

        if (event1Heading) {
            event1Heading.textContent = `${event1TimeFormatted} (Everyday)`;
        }
        if (event2Heading) {
            event2Heading.textContent = `${event2TimeFormatted} (MON, WED, FRI)`;
        }
    }
    updateHeadings();
    setInterval(updateEventTimes, 1000); // update every second
});
