$(document).ready(function() {
    $('#lecture-select').on('change', function() {
        var lectureId = $(this).val();
        if (lectureId) {
            $.ajax({
                url: '/get_lecture_structures/' + lectureId + '/',
                method: 'GET',
                success: function(data) {
                    updateInstructionalActivities(data);
                }
            });

            $.ajax({
                url: '/get_observations/' + lectureId + '/',
                method: 'GET',
                success: function(data) {
                    updateObservations(data);
                }
            });
        }
    });
});

function updateInstructionalActivities(data) {
    var list = $('#instructional-activities-list');
    list.empty();
    data.forEach(function(item) {
        list.append('<li>' + item.activity + '</li>');
    });
}

function updateObservations(data) {
    var list = $('#observations-list');
    list.empty();
    data.forEach(function(item) {
        list.append('<li>' + item.observation_text + '</li>');
    });
}

function addLectureStructure() {
    var lectureId = $('#lecture-select').val();
    var activity = $('#activity-input').val();
    var materials = $('#materials-input').val();
    var startTime = $('#start-time-input').val();
    var endTime = $('#end-time-input').val();

    if (lectureId && activity && startTime && endTime) {
        $.ajax({
            url: '/add_lecture_structure/',
            method: 'POST',
            data: {
                lecture_id: lectureId,
                activity: activity,
                materials: materials,
                start_time: startTime,
                end_time: endTime,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                if (data.status === 'success') {
                    $('#activity-input').val('');
                    $('#materials-input').val('');
                    $('#start-time-input').val('');
                    $('#end-time-input').val('');
                    $('#lecture-select').trigger('change');  // Refresh the list
                }
            }
        });
    }
}

function addObservation() {
    var lectureId = $('#lecture-select').val();
    var observationText = $('#observation-text').val();
    var startTime = $('#obs-start-time-input').val();
    var endTime = $('#obs-end-time-input').val();

    if (lectureId && observationText && startTime && endTime) {
        $.ajax({
            url: '/add_observation/',
            method: 'POST',
            data: {
                lecture_id: lectureId,
                observation_text: observationText,
                start_time: startTime,
                end_time: endTime,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                if (data.status === 'success') {
                    $('#observation-text').val('');
                    $('#obs-start-time-input').val('');
                    $('#obs-end-time-input').val('');
                    $('#lecture-select').trigger('change');  // Refresh the list
                }
            }
        });
    }
}
