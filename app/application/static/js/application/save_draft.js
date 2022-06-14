$('.draftable').on('change', function(){
    saveDraft(this.name, this.value);
});

$('.personal').on('change', function(){
    saveUserProfileDraft(this.name, this.value);
});

$('input:radio').change(function() {
  switch (this.name){
    case 'age':
      saveUserProfileDraft(this.name, this.value);
      break;
    case 'gender':
      saveUserProfileDraft(this.name, this.value);
      break;
    case 'preferred_language':
      saveUserProfileDraft(this.name, this.value);
      break;
    default:
      saveDraft(this.name, this.value);
      break;
  }
});

$('input:checkbox').change(function() {
    saveDraft(this.name, this.value);
});


function saveDraft(field, value) {
  var url = '/applications/application/draft/';
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

function saveUserProfileDraft(field, value) {
  var url = '/applications/user/info/';
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