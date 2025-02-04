document.addEventListener('DOMContentLoaded', function() {

    // Function to initialize form
    function initializeForm() {
        const servicesSelect = document.getElementById('id_services');
        const dateInput = document.getElementById('id_date');
        const startTimeInput = document.getElementById('id_start_time');
        const endTimeInput = document.getElementById('id_end_time');
        const serviceDurationsElement = document.getElementById('service-durations');

    const serviceDurations = JSON.parse(serviceDurationsElement.textContent);

    // Function to update the end time
    function updateEndTime() {
        const selectServices = Array.from(servicesSelect.selectedOptions);
        const totalDuration = selectServices.reduce((total, option) => {
            return total + (serviceDurations[option.text] || 0);
        }, 0);

        if (startTimeInput.value) {
            const [hours, minutes] = startTimeInput.value.split(':').map(Number);
            const startTime = new Date();
            startTime.setHours(hours, minutes);
            const endTime = new Date(startTime.getTime() + totalDuration * 60000);
            endTimeInput.value = endTime.toTimeString().slice(0, 5);
        }
    }

    // Events to update the end time
    servicesSelect.addEventListener("change", updateEndTime)
    startTimeInput.addEventListener("change", updateEndTime);

    // Initialize Select2
    $('#id_client').select2();
    $('#id_employee').select2();
    $('#id_services').select2();

    // Trigger initial update
    updateEndTime();
    }

    // Check if we're on the create appointment page
    if (document.getElementById('id_services')) {
        initializeForm();
    }
});