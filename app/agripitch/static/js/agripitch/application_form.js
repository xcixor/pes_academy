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
/**
 * Select all form navigation buttons, and loop through them.
 */
document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    /**
     * Add a click event listener to the button.
     */
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

$('.form-input-validate').on('change', evt =>{
    let formSection = $(evt.target).parent().parent().parent();
    let actionButtons = formSection.find(".btn-navigate-form-step");
    for (let i = 0; i < actionButtons.length; i++) {
        $(actionButtons[i]).removeAttr('disabled').css('background-color', '#14A562');
        $(evt.target).css('border-color', '#ccc');
        $(`label[for="id_${evt.target.name}"]`).css('color', 'unset');
    }
});

function validateSection(formSection){
    let isValid = true;
    let inputs = formSection.find(".form-input-validate");
    for (i = 0; i < inputs.length; i++) {
        if($(inputs[i]).val() == ""){
            $(inputs[i]).css('border-color', 'red');
            $(`label[for="id_${inputs[i].name}"]`).css('color', 'red');
            isValid = false;
        }
    }
    return isValid;
}