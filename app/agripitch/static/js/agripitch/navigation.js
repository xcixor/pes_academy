$(document).ready(function () {
	$(".is-dependent").siblings().css("display", "none");
});



/**
 * Define a function to navigate betweens form steps.
 * It accepts one parameter. That is - step number.
 */
const navigateToFormStep = (stepNumber) => {
	localStorage.setItem("stepNumber", JSON.stringify(stepNumber));
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
		formStepHeader.classList.remove(
			"form-stepper-active",
			"form-stepper-completed"
		);
	});
	/**
	 * Show the current form step (as passed to the function).
	 */
	document.querySelector("#step-" + stepNumber).classList.remove("d-none");
	/**
	 * Select the form step circle (progress bar).
	 */
	const formStepCircle = document.querySelector(
		'li[step="' + stepNumber + '"]'
	);
	/**
	 * Mark the current form step as active.
	 */
	formStepCircle.classList.remove(
		"form-stepper-unfinished",
		"form-stepper-completed"
	);
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
			formStepCircle.classList.remove(
				"form-stepper-unfinished",
				"form-stepper-active"
			);
			formStepCircle.classList.add("form-stepper-completed");
		}
	}
};

document
	.querySelectorAll(".top-navigate-form-step")
	.forEach((formNavigationBtn) => {
		formNavigationBtn.addEventListener("click", () => {
			const stepNumber = parseInt(
				formNavigationBtn.getAttribute("step_number")
			);
			navigateToFormStep(stepNumber);
		});
	});

document
	.querySelectorAll(".btn-navigate-form-step")
	.forEach((formNavigationBtn) => {
		formNavigationBtn.addEventListener("click", () => {
			var formSection = $(formNavigationBtn).parent().parent();
			const stepNumber = parseInt(
				formNavigationBtn.getAttribute("step_number")
			);
			navigateToFormStep(stepNumber);
		});
	});
