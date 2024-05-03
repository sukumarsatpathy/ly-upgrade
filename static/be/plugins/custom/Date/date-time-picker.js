$(document).ready(function () {
    // Define form element
    const form = document.getElementsByClassName("datepicker");

    // Current date
    var currentDate = new Date();

    // Tempus Dominus Bootstrap Datepicker --- for more info, please visit: https://getdatepicker.com/
    tempusDominus.extend(tempusDominus.plugins.customDateFormat);

    // Initialize Tempus Dominus for startDate
    new tempusDominus.TempusDominus(document.getElementById('startDate'), {
        localization: {
            locale: 'en',
            format: 'yyyy-MM-dd HH:mm', // Adjust format as needed
        },
         restrictions: {
            minDate: currentDate
        }
    });

    // Initialize Tempus Dominus for endDate
    new tempusDominus.TempusDominus(document.getElementById('endDate'), {
        localization: {
            locale: 'en',
            format: 'yyyy-MM-dd HH:mm', // Adjust format as needed
        },
         restrictions: {
            minDate: currentDate
        }
    });
});