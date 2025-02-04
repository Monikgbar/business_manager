document.addEventListener('DOMContentLoaded', function() {
    const appointmentDataEl = document.getElementById('appointments_data');
    const calendarContainer = document.getElementById('calendars-container');
    const currentDateEl = document.getElementById('current-date');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const todayButton = document.getElementById('today');
    const monthViewButton = document.getElementById('month-view');


    if (!appointmentDataEl || !calendarContainer) {
        console.error('No found appointments_data element');
        return;
    }

    try {
        const appointmentData = JSON.parse(appointmentDataEl.textContent);

        // Make sure there is always at least one calendar
        if (appointmentData.length === 0) {
            appointmentData.push({
                employee_id: 'default',
                employee_name: 'Sin empleados',
                appointments: []
            });
        }

        // Object to store the calendar by employee
        const calendars = {};

        // Iterate over each employee to initialize a calendar for each one
        appointmentData.forEach(function(employeeData) {
            // Create an unique element for each employee's calendar
            const employeeCalendarContainer = document.createElement('div');
            employeeCalendarContainer.id = 'calendar-' + (employeeData.employee_id || 'default');
            employeeCalendarContainer.className = 'calendar-employee';
            calendarContainer.appendChild(employeeCalendarContainer);

            // Defines the calendar element (calendarEl) based on the newly created container
            const calendarEl = document.getElementById('calendar-' + (employeeData.employee_id || 'default'));

            const calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'timeGridDay',
                allDaySlot: false,
                slotDuration: '00:15:00',
                slotMinTime: '09:00:00',
                slotMaxTime: '20:30:00',
                firstDay: 1,
                weekends: false,
                locale: 'es',
                editable: true,
                selectable: true,
                eventDurationEditable: true,
                nowIndicator: true,
                headerToolbar: false,
                // Loading custom events for the employee
                events: employeeData.appointments.map(event => ({
                    ...event,
                    backgroundColor: event.extendedProps.employeeColor,
                    borderColor: event.extendedProps.categoryColor
                })),

                eventDidMount: function(info) {
                    if (info.event.extendedProps.employeeColor) {
                        info.el.style.backgroundColor = info.event.extendedProps.employeeColor;
                    }
                    if (info.event.extendedProps.categoryColor) {
                        info.el.style.border = `5px solid ${info.event.extendedProps.categoryColor}`;
                    }
                },

                eventContent: function(arg) {
                    // Split the title by line breaks
                    const titleLines = arg.event.title.split('\n');

                    // Create a container for the lines
                    const container = document.createElement('div');

                    titleLines.forEach((line, index) => {
                        const lineElement = document.createElement('div');
                        lineElement.textContent = line;
                        container.appendChild(lineElement);

                        // Add a margin only after the customer name
                        if (index === 0) {
                            lineElement.style.textAlign = 'center';
                            lineElement.style.marginBottom = '5px';
                            lineElement.style.marginTop = '0px';
                            lineElement.style.fontWeight = 'bold';
                        }else {
                            lineElement.style.textAlign = 'center';
                            lineElement.style.marginBottom = '10px';
                        }
                    });
                    return { domNodes: [container]};
                },

                eventClick: function(info) {
                    window.location.href = `detail/${info.event.id}/`;
                },

                dateClick: function(info) {
                    const calendarElement = info.dayEl.closest('.calendar-employee');
                    const employeeId = calendarElement.getAttribute('data-employee-id') || '';
                    const date = info.dateStr.split('T')[0];
                    const time = info.dateStr.includes('T') ? info.dateStr.split('T')[1].split('+')[0] : '09:00:00';

                    const formattedDateTime = `${date}T${time}`;
                    const url = `/appointment/create/?employee_id=${employeeId}&date=${formattedDateTime}`;

                    window.location.href = url;
                },

                themeSystem: 'bootstrap5',
            });
            // Save the calendar to the object
            calendars[employeeData.employee_id] = calendar;

            calendar.render();
        });

        function formatDate(date) {
            return date.toLocaleDateString('es-ES', {
                weekday: 'long',
                day: '2-digit',
                month: 'short',
            });
        }

        // Function to update the displayed date
        function updateDate() {
            const firstCalendarId = Object.keys(calendars)[0];
            if (firstCalendarId) {
                const currentDate = calendars[firstCalendarId].getDate();
                currentDateEl.textContent = formatDate(currentDate);
            }
        }

        // Configure button events
        prevButton.addEventListener('click', () => {
            Object.values(calendars).forEach(calendar => calendar.prev());
            updateDate();
        });

        nextButton.addEventListener('click', () => {
            Object.values(calendars).forEach(calendar => calendar.next());
            updateDate();
        });

        todayButton.addEventListener('click', () => {
            Object.values(calendars).forEach(calendar => {
                calendar.today();
                calendar.changeView('timeGridDay');
            });
            updateDate();
        });

        monthViewButton.addEventListener('click', () => {
            Object.values(calendars).forEach(calendar => calendar.changeView('dayGridMonth'));
        });

        // Initialize date to load
        updateDate();

    }catch (error) {
        console.error("Error parsing JSON data", error);
    }
});









