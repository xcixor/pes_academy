const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = 0;

nextBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    let allAreFilled = checkRequiredFields($(btn).attr("data-title"));
    if (!allAreFilled){
      showErrorMessage($(btn).attr("data-title"));
      return;
    }else if(allAreFilled){
      formStepsNum++;
      updateFormSteps();
      updateProgressbar();
    }
  });
});

function showErrorMessage(data_title){
  $(`#error-${data_title}`).html("Please fill all the required fields")
  let formSection = $(`.${data_title}`)[0];
  formSection.querySelectorAll("[required]").forEach(function(i){
    if (i.type === "radio" && i.checked === false )  {
      $(`#label_${i.name}`).css("color","red");
    }
    if (i.type === "text" && !$(i).val() )  {
      $(`#label_${i.name}`).css("color","red");
    }
  })
}

prevBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    formStepsNum--;
    updateFormSteps();
    updateProgressbar();
  });
});

function updateFormSteps() {
  formSteps.forEach((formStep) => {
    formStep.classList.contains("form-step-active") &&
    formStep.classList.remove("form-step-active");
  });

  formSteps[formStepsNum].classList.add("form-step-active");
}

function updateProgressbar() {
  progressSteps.forEach((progressStep, idx) => {
    if (idx < formStepsNum + 1) {
      progressStep.classList.add("progress-step-active");
    } else {
      progressStep.classList.remove("progress-step-active");
    }
  });

  const progressActive = document.querySelectorAll(".progress-step-active");

  progress.style.width =
    ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}


const max = 3;

document.addEventListener('change', function(e) {
  if (e.target.tagName == 'INPUT') {
    if (document.querySelectorAll(".mil input[type='checkbox']:checked").length > max) {
      e.target.checked = false;
      console.log(`${max} You can only choose a maximum of 3!`);
    }
  }
});

function checkRequiredFields(data_title) {
  let allAreFilled = true;
  let formSection = $(`.${data_title}`)[0];
  formSection.querySelectorAll("[required]").forEach(function(i) {
    if (!allAreFilled) return;
    if (!i.value) allAreFilled = false;
    if (i.type === "radio") {
      let radioValueCheck = false;
     formSection.querySelectorAll(`[name=${i.name}]`).forEach(function(r) {
       if (r.checked) radioValueCheck = true;
      })
      allAreFilled = radioValueCheck;
    }
  });
  return allAreFilled;

}
