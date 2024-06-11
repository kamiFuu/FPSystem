$(document).ready(function() {
    $('#lecture-select').on('change', function() {
        var lectureId = $(this).val();
        if (lectureId) {
            $.ajax({
                url: '/FPapp/clicker/get_lecture_structures/' + lectureId + '/',
                method: 'GET',
                success: function(data) {
                    updateInstructionalActivities(data);
                }
            });

            $.ajax({
                url: '/FPapp/clicker/get_observations/' + lectureId + '/',
                method: 'GET',
                success: function(data) {
                    updateObservations(data);
                }
            });
        }
    });
});


function addLectureStructure() {
    var lectureId = $('#lecture-select').val();
    var activity = $('#activity-input').val();
    var materials = $('#materials-input').val();
    var startTime = $('#start-time-input').val();
    var endTime = $('#end-time-input').val();

    if (lectureId && activity && startTime && endTime) {
        $.ajax({
            url: '/FPapp/clicker/add_lecture_structure/',
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
            url: '/FPapp/clicker/add_observation/',
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
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('lecture').addEventListener('change', function() {
        var lectureId = this.value;
        if (lectureId) {
            fetch(`/FPapp/clicker/get_lecture_structures/${lectureId}/`)
                .then(response => response.json())
                .then(data => updateInstructionalActivities(data));

            fetch(`/FPapp/clicker/get_observations/${lectureId}/`)
                .then(response => response.json())
                .then(data => updateObservations(data));
        }
    });
});

function fetchLectures(courseId) {
    fetch(`/FPapp/clicker/get_lectures/${courseId}/`)
    .then(response => response.json())
    .then(data => {
        let lectureSelect = document.getElementById('lecture');
        lectureSelect.innerHTML = '';
        data.forEach(lecture => {
            let option = document.createElement('option');
            option.value = lecture.id;
            option.text = lecture.lecture_name;
            lectureSelect.add(option);
        });
    });
}

function sendClick(studentId) {
    let lectureId = document.getElementById('lecture').value;
    fetch("/FPapp/clicker/record_click/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
        body: new URLSearchParams({student_id: studentId, lecture_id: lectureId}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Click recorded successfully!');
        } else {
            alert('Error: ' + data.message);
        }
    });
}
function addLectureStructure() {
    let lectureId = document.getElementById('lecture').value;
    let structureName = document.getElementById('structure_name').value;
    let startTime = document.getElementById('structure_start_time').value;
    let endTime = document.getElementById('structure_end_time').value;
    
    fetch("{% url 'add_lecture_structure' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: new URLSearchParams({lecture_id: lectureId, structure_name: structureName, start_time: startTime, end_time: endTime}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Lecture Structure added successfully!');
        } else {
            alert('Error: ' + data.message);
        }
    });
}

function addLectureStructure() {
    let lectureId = document.getElementById('lecture').value;
    let structureName = document.getElementById('structure_name').value;
    let materials = document.getElementById('materials').value;
    let startTime = document.getElementById('structure_start_time').value;
    let endTime = document.getElementById('structure_end_time').value;

    // Debug: Kiểm tra giá trị của các biến
    console.log('lectureId:', lectureId);
    console.log('structureName:', structureName);
    console.log('materials:', materials);
    console.log('startTime:', startTime);
    console.log('endTime:', endTime);
    // Kiểm tra dữ liệu không hợp lệ
    if (!lectureId || !structureName || !materials || !startTime || !endTime) {
        alert('Please fill in all required fields.');
        return;
    }

    fetch("/FPapp/clicker/add_lecture_structure/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
        body: new URLSearchParams({
            lecture_id: lectureId,
            activity: structureName,
            materials: materials,
            start_time: startTime,
            end_time: endTime
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Lecture Structure added successfully!');
            document.getElementById('structure_name').value = '';
            document.getElementById('materials').value = '';
            document.getElementById('structure_start_time').value = '';
            document.getElementById('structure_end_time').value = '';
            document.getElementById('lecture').dispatchEvent(new Event('change'));
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding lecture structure. Please try again.');
    });
}


function addObservation() {
    let lectureId = document.getElementById('lecture').value;
    let observationText = document.getElementById('observation_text').value;
    let startTime = document.getElementById('observation_start_time').value;
    let endTime = document.getElementById('observation_end_time').value;

    fetch("/FPapp/clicker/add_observation/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
        body: new URLSearchParams({
            lecture_id: lectureId,
            observation_text: observationText,
            start_time: startTime,
            end_time: endTime
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Observation added successfully!');
            document.getElementById('observation_text').value = '';
            document.getElementById('observation_start_time').value = '';
            document.getElementById('observation_end_time').value = '';
            document.getElementById('lecture').dispatchEvent(new Event('change'));
        } else {
            alert('Error: ' + data.message);
        }
    });
}

function updateInstructionalActivities(data) {
    var list = document.getElementById('instructional-activities-list');
    list.innerHTML = '';
    data.forEach(function(item) {
        list.insertAdjacentHTML('beforeend', '<li>' + item.activity + ': ' + item.start_time +' - '+ item.end_time + '</li>');
    });
}

function updateObservations(data) {
    var list = document.getElementById('observations-list');
    list.innerHTML = '';
    data.forEach(function(item) {
        list.insertAdjacentHTML('beforeend', '<li>' + item.observation_text + ': ' + item.start_time +' - '+ item.end_time + '</li>');
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
