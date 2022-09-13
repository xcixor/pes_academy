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
	.querySelectorAll(".btn-navigate-form-step")
	.forEach((formNavigationBtn) => {
		formNavigationBtn.addEventListener("click", () => {
			var formSection = $(formNavigationBtn).parent().parent();
			var isValid = validateSection(formSection);
			if (isValid) {
				const stepNumber = parseInt(
					formNavigationBtn.getAttribute("step_number")
				);
				navigateToFormStep(stepNumber);
			} else {
				$(formNavigationBtn)
					.attr("disabled", "disabled")
					.css("background-color", "#8ad2b1");
				return;
			}
		});
	});

$(".form-input").on("change", (evt) => {
	let formSection = $(evt.target).closest(".form-step");
	let actionButtons = formSection.find(".btn-navigate-form-step");
	for (let i = 0; i < actionButtons.length; i++) {
		$(actionButtons[i])
			.removeAttr("disabled")
			.css("background-color", "#14A562");
		$(evt.target).css("border-color", "#ccc");
		$(`label[for="id_${evt.target.name}"]`).css("color", "unset");
	}
	evt.target.name;
	if (evt.target.type === "file") {
		$(`label[for="id_${evt.target.name}"]`).html(evt.target.name);
	}
	if (evt.target.type === "radio") {
		var radios = document.getElementsByName(evt.target.name);
		let parentLabel = $(
			`label[for="${getRadiosParent(radios).attr("id")}_0"]`
		)[0];
		$(parentLabel).css("color", "unset");
	}
	if (evt.target.type === "checkbox") {
		let parentLabel = $(`label:contains(${evt.target.name})`);
		$(parentLabel).css("color", "unset");
	}
});

function validateSection(formSection) {
	let isValid = true;
	let inputs = formSection.find(".form-input-validate");
	for (i = 0; i < inputs.length; i++) {
		let inputsValidity = true;
		let radiosValidity = true;
		let checkBoxesValidity = true;
		if (
			isEmptyOrSpaces($(inputs[i]).val()) &&
			inputs[i].type != "radio" &&
			inputs[i].type != "checkbox" &&
			inputs[i].type
		) {
			$(inputs[i]).css("border-color", "red");
			$(`label[for="id_${inputs[i].name}"]`).css("color", "red");
			inputsValidity = false;
		}
		if (inputs[i].type === "radio") {
			radiosValidity = validateRadios(inputs[i].name);
		}
		if (inputs[i].type === "checkbox") {
			let checkBoxes = document.getElementsByName(inputs[i].name);
			let numberOfCheckedItems = 0;
			for (let i = 0; i < checkBoxes.length; i++) {
				let parentLabel = $(`label:contains(${checkBoxes[i].name})`);
				if (checkBoxes[i].checked) {
					numberOfCheckedItems++;
				}
				if (numberOfCheckedItems === 0) {
					$(parentLabel).css("color", "red");
					checkBoxesValidity = false;
				} else {
					checkBoxesValidity = true;
					$(parentLabel).css("color", "unset");
				}
			}
		}
		if (!inputsValidity || !radiosValidity || !checkBoxesValidity) {
			isValid = false;
		}
	}

	let file_inputs = formSection.find("input[type=file]");
	for (i = 0; i < file_inputs.length; i++) {
		if (file_inputs[i].files[0]) {
			if (file_inputs[i].files[0].size > $(file_inputs[i]).attr("max_size")) {
				$(`label[for="id_${file_inputs[i].name}"]`).css("color", "red");
				let max_size = parseInt($(file_inputs[i]).attr("max_size")) / 1048576;
				$(`label[for="id_${file_inputs[i].name}"]`).append(
					` is too big, maximum size should be ${max_size}MB!`
				);
				this.value = "";
				isValid = false;
			}
		}
	}
	if (isValid) {
		for (i = 0; i < inputs.length; i++) {
			if (
				inputs[i].type != "file" &&
				inputs[i].type != "radio" &&
				inputs[i].type != "checkbox" &&
				$(inputs[i]).val()
			) {
				saveDraftData(inputs[i].name, $(inputs[i]).val());
			}
			if (inputs[i].type == "radio") {
				if ($(inputs[i]).is(":checked")) {
					saveDraftData(inputs[i].name, $(inputs[i]).val());
				}
			}

			if (inputs[i].type == "checkbox") {
				if ($(inputs[i]).hasClass("multiple_checkbox")) {
					let checkBoxes = document.getElementsByName(inputs[i].name);
					let inputValues = [];
					for (let i = 0; i < checkBoxes.length; i++) {
						if ($(checkBoxes[i]).val()) {
							inputValues.push($(checkBoxes[i]).val());
						}
					}
					console.log(inputValues, checkBoxes[0].name);
					saveDraftData(checkBoxes[0].name, inputValues);
				}else {
				saveDraftData(inputs[i].name, $(inputs[0]).val());
                }
			}
		}
		for (i = 0; i < file_inputs.length; i++) {
			if ($(file_inputs[i])[0].files[0]) {
				saveDraftData(file_inputs[i].name, $(file_inputs[i])[0].files[0]);
			}
		}
	}
	if (!isValid) {
		$("#formErrors").text(
			"Please fill in all the required fields. * Means an input required."
		);
	} else {
		$("#formErrors").text("");
	}
	console.log(isValid);
	return isValid;
}

function validateRadios(name) {
	var radios = document.getElementsByName(name);
	var formValid = false;
	var i = 0;
	while (!formValid && i < radios.length) {
		if (radios[i].checked) formValid = true;
		i++;
	}
	if (!formValid) {
		let parentLabel = $(
			`label[for="${getRadiosParent(radios).attr("id")}_0"]`
		)[0];
		$(parentLabel).css("color", "red");
	}
	return formValid;
}

function getRadiosParent(radios) {
	return $(radios).closest("ul");
}

function saveDraftData(field, value) {
	let application = $("#currentApplication").val();
	var url = `/agripitch/${application}/application/`;
	var CSRFToken = $("input[name=csrfmiddlewaretoken]").val();

	var xhr = new XMLHttpRequest();
	var formData = new FormData();
	xhr.open("POST", url, true);
	xhr.setRequestHeader("X-CSRFToken", CSRFToken);
	xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("enctype", "multipart/form-data");

	xhr.addEventListener("readystatechange", function (e) {
		if (xhr.readyState === 4 && xhr.status == 201) {
			var response = JSON.parse(xhr.response);
			// console.log(response)
		} else if (xhr.readyState === 4 && xhr.status === 400) {
			var errors = JSON.parse(xhr.response);
			Object.values(errors).forEach((val) => {
				console.log(val);
			});
		}
	});
	formData.append(field, value);
	xhr.send(formData);
}

function isEmptyOrSpaces(str) {
	return str === null || str.match(/^ *$/) !== null;
}
