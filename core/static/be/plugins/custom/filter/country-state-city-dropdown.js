$(document).ready(function () {
    // AJAX calls for state and city dropdowns
    $("#id_country").change(function () {
        var url = $(".form").attr("data-states-url");
        var countryId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'country': countryId
            },
            success: function (data) {
                $("#id_state").html(data);
                $("#id_city").html('<option value="">Select a city</option>');
            }
        });
    });

    $("#id_state").change(function () {
        var url = $(".form").attr("data-cities-url");
        var stateId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'state': stateId
            },
            success: function (data) {
                $("#id_city").html(data);
            }
        });
    });
});