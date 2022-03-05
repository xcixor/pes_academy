function saveDocument(event, document_name, application){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/applications/document/', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('Accept', 'application/json');
    var CSRFToken = $('input[name=csrfmiddlewaretoken]').val();
    xhr.setRequestHeader('X-CSRFToken', CSRFToken);
    xhr.addEventListener('readystatechange', function(e) {
        if (xhr.readyState === 4 && xhr.status == 201) {
            var message = JSON.parse(xhr.response);
            console.log(message);
        }
        else if (xhr.readyState === 4 && xhr.status != 200) {
            var errors = JSON.parse(xhr.response);
            Object.values(errors).forEach(val => {
            console.error(val);
            });
        }
    });
    var formData = new FormData();
    formData.append('document_name', document_name);
    formData.append('document', event.target.files[0]);
    formData.append('application', application);
    xhr.send(formData);
}