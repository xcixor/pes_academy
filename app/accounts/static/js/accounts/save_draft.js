$('.draftable').on('change', function(){
    saveDraft(this.name, this.value);
});

$('input:radio').change(function() {
    let radioId = this.id;
    saveDraft(this.name, radioId);
});

$('input:checkbox').change(function() {
    saveDraft(this.name, $(`#${this.id}`).is(":checked"));
});


function saveDraft(field, value) {
    console.log(field, value);
  var url = '/accounts/application/draft/';
  var CSRFToken = $('input[name=csrfmiddlewaretoken]').val();

  var xhr = new XMLHttpRequest();
  var formData = new FormData();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('X-CSRFToken', CSRFToken);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.setRequestHeader('Accept', 'application/json');

  xhr.addEventListener('readystatechange', function(e) {
    if (xhr.readyState === 4 && xhr.status == 201) {
      var response = JSON.parse(xhr.response);
      console.log(response);
    }
    else if (xhr.readyState === 4 && xhr.status != 200) {
      var errors = JSON.parse(xhr.response);
      Object.values(errors).forEach(val => {
        console.log(val);
      });
    }
  });
  formData.append(field, value);
  xhr.send(formData);
}