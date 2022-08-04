/**
 * Define a function to navigate betweens form steps.
 * It accepts one parameter. That is - step number.
 */
const navigateToFormStep = (stepNumber) => {
    /**
     * Hide all form steps.
     */
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    /**
     * Mark all form steps as unfinished.
     */
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    /**
     * Show the current form step (as passed to the function).
     */
    document.querySelector("#step-" + stepNumber).classList.remove("d-none");
    /**
     * Select the form step circle (progress bar).
     */
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    /**
     * Mark the current form step as active.
     */
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");
    /**
     * Loop through each form step circles.
     * This loop will continue up to the current step number.
     * Example: If the current step is 3,
     * then the loop will perform operations for step 1 and 2.
     */
    for (let index = 0; index < stepNumber; index++) {
        /**
         * Select the form step circle (progress bar).
         */
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        /**
         * Check if the element exist. If yes, then proceed.
         */
        if (formStepCircle) {
            /**
             * Mark the form step as completed.
             */
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    formNavigationBtn.addEventListener("click", () => {
        var formSection = $(formNavigationBtn).parent().parent();
        var isValid = validateSection(formSection);
        if(isValid){
            const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
            navigateToFormStep(stepNumber);
        }else {
            $(formNavigationBtn).attr('disabled', 'disabled').css('background-color', '#8ad2b1');
            return;
        }
    });
});

$('.form-input').on('change', evt =>{
    let formSection = $(evt.target).closest(".form-step");
    let actionButtons = formSection.find(".btn-navigate-form-step");
    for (let i = 0; i < actionButtons.length; i++) {
        $(actionButtons[i]).removeAttr('disabled').css('background-color', '#14A562');
        $(evt.target).css('border-color', '#ccc');
        $(`label[for="id_${evt.target.name}"]`).css('color', 'unset');
    }evt.target.name
    if(evt.target.type === 'file'){
        $(`label[for="id_${evt.target.name}"]`).html(evt.target.name)
    }
    if(evt.target.type === 'radio'){
        var radios = document.getElementsByName(evt.target.name);
        let parentLabel = $(`label[for="${getRadiosParent(radios).attr('id')}_0"]`)[0];
        $(parentLabel).css('color', 'unset')
    }
});

function validateSection(formSection){
    let isValid = true;
    let inputs = formSection.find(".form-input-validate");
    for (i = 0; i < inputs.length; i++) {
        if($(inputs[i]).val() == "" && inputs[i].type != 'radio' && inputs[i].type){
            $(inputs[i]).css('border-color', 'red');
            $(`label[for="id_${inputs[i].name}"]`).css('color', 'red');
            isValid = false;
        }
        if (inputs[i].type === 'radio'){
            isValid = validateRadios(inputs[i].name)
        }
    }

    let file_inputs = formSection.find("input[type=file]");
    for (i = 0; i < file_inputs.length; i++) {
        if(file_inputs[i].files[0]){
            if(file_inputs[i].files[0].size > $(file_inputs[i]).attr('max_size')){
                $(`label[for="id_${file_inputs[i].name}"]`).css('color', 'red');
                let max_size = parseInt($(file_inputs[i]).attr('max_size')) / 1048576
                $(`label[for="id_${file_inputs[i].name}"]`).append(` is too big, maximum size should be ${max_size}MB!`)
                this.value = "";
                isValid = false;
            };
        }
    }
    if(isValid){
        for (i = 0; i < inputs.length; i++) {
            console.log(inputs[i].type)
            if(inputs[i].type != 'file'){
                saveDraftData(inputs[i].name, $(inputs[i]).val())
            }
        }
        for (i = 0; i < file_inputs.length; i++) {
            if($(file_inputs[i])[0].files[0]){
                saveDraftData(file_inputs[i].name, $(file_inputs[i])[0].files[0])
            }
        }
    }
    return isValid;
}

function validateRadios(name){
    var radios = document.getElementsByName(name);
    var formValid = false;
    var i = 0;
    while (!formValid && i < radios.length) {
        if (radios[i].checked) formValid = true;
        i++;
    }
    if (!formValid) {
        let parentLabel = $(`label[for="${getRadiosParent(radios).attr('id')}_0"]`)[0];
        $(parentLabel).css('color', 'red')
    }
    return formValid;
}

function getRadiosParent(radios){
    return $(radios).closest("ul")
}

function saveDraftData(field, value) {
    let application = $('#currentApplication').val();
    var url = `/agripitch/${application}/application/`;
    var CSRFToken = $('input[name=csrfmiddlewaretoken]').val();

    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-CSRFToken', CSRFToken);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.setRequestHeader('enctype', 'multipart/form-data');

    xhr.addEventListener('readystatechange', function(e) {
        if (xhr.readyState === 4 && xhr.status == 201) {
            var response = JSON.parse(xhr.response);
            console.log(response)
        }
        else if (xhr.readyState === 4 && xhr.status === 400) {
            var errors = JSON.parse(xhr.response);
            Object.values(errors).forEach(val => {
                console.log(val);
            });
        }
    });
    formData.append(field, value);
    xhr.send(formData);
}
