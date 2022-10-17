$(document).ready(function () {
	$(".is-dependent").siblings().css("display", "none");
});
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
	.querySelectorAll(".top-navigate-form-step")
	.forEach((formNavigationBtn) => {
		formNavigationBtn.addEventListener("click", () => {
			const stepNumber = parseInt(
				formNavigationBtn.getAttribute("step_number")
			);
			navigateToFormStep(stepNumber);
		});
	});

document.addEventListener("mousedown", (event) => {
	activateNavigationButtons();
});

document.addEventListener("keypress", (event) => {
	activateNavigationButtons();
});

function activateNavigationButtons() {
	let navigationButtons = $(".btn-navigate-form-step");

	Array.from(navigationButtons).forEach((button) => {
		if ($(button).attr("disabled")) {
			console.log('clicked')
			$(button).removeAttr("disabled");
			$(button).css("background-color", "#14A562");
		}
	});
}

document
	.querySelectorAll(".btn-navigate-form-step")
	.forEach((formNavigationBtn) => {
		formNavigationBtn.addEventListener("click", () => {
			var formSection = $(formNavigationBtn).parent().parent();
			const stepNumber = parseInt(
				formNavigationBtn.getAttribute("step_number")
			);
			if ($(formNavigationBtn).text() === "Next") {
				var isValid = true;
				let notRequiredFieldsValidation =
					saveNonRequiredFilledFields(formSection);
				let requiredFieldsValidation = validateSection(formSection);
				if (!notRequiredFieldsValidation || !requiredFieldsValidation) {
					isValid = false;
				}
				if (isValid) {
					navigateToFormStep(stepNumber);
				} else {
					$(formNavigationBtn)
						.attr("disabled", "disabled")
						.css("background-color", "#8ad2b1");
					return;
				}
			} else {
				if (isValid) {
					$("#formErrors").text("");
				}
				navigateToFormStep(stepNumber);
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

$(".has-dependent-question").on("change", (evt) => {
	let elementWithDependant = $(evt.target);
	toggleDependantQuestion(elementWithDependant);
});

function toggleDependantQuestion(elementWithDependant) {
	let dependentElements = $(
		`.${$(elementWithDependant).attr("data-dependant-question-id")}`
	);
	for (let i = 0; i <= dependentElements.length; i++) {
		var dependentElement = $(dependentElements[i]);
		toggleDependant(elementWithDependant, dependentElement);
	}
}

function toggleDependant(elementWithDependant, dependentElement) {
	let dependantChildren = $(dependentElement).find("input");
	if (
		$(elementWithDependant).val() ===
		$(elementWithDependant).attr("data-determinant-answer")
	) {
		$(dependentElement).addClass("form-input-validate form-input");
		$(dependentElement).removeClass("is-dependent");
		$(dependentElement).siblings().css("display", "block");
		if (
			$(dependentElement).hasClass("form-radio") ||
			$(dependentElement).hasClass("multiple_checkbox")
		) {
			$(dependentElement).css("display", "block");
			for (i = 0; i < dependantChildren.length; i++) {
				$(dependentElement[i])
					.find("input")
					.addClass("form-input-validate form-input");
				$(dependantChildren[i]).removeClass("is-dependent");
			}
		}
	} else {
		$(dependentElement).val("");
		$(dependentElement).trigger("change");
		$(dependentElement).removeClass("form-input-validate");
		console.log($(dependentElement).attr("name"));
		removeResponseFromDb($(dependentElement).attr("name"));
		dependentElement.siblings().css("display", "none");
		$(dependentElement).addClass("is-dependent");

		if ($(dependentElement).hasClass("form-radio")) {
			for (i = 0; i < dependantChildren.length; i++) {
				$(dependentElement[i]).find("input").removeClass("form-input-validate");
				$(dependentElement).css("display", "none");
				$(dependantChildren[i]).addClass("is-dependent");
			}
			$(dependentElement)
				.find("input[type=checkbox]:checked")
				.removeAttr("checked");
		}
	}
}

function removeResponseFromDb(name) {
	var url = `/agripitch/subcriteria/responses/delete/`;
	var CSRFToken = $("input[name=csrfmiddlewaretoken]").val();

	var xhr = new XMLHttpRequest();
	xhr.open("POST", url, true);
	xhr.setRequestHeader("X-CSRFToken", CSRFToken);
	xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	xhr.setRequestHeader("Accept", "application/json");

	xhr.addEventListener("readystatechange", function (e) {
		if (xhr.readyState == 4 && xhr.status == 204) {
			var response = JSON.parse(xhr.response);
			console.log(response);
		} else {
			var errors = xhr.status;
			console.error(errors);
		}
	});
	formData = new FormData();
	formData.append("label", name);
	xhr.send(formData);
}

function saveNonRequiredFilledFields(formSection) {
	let isValid = true;

	let inputs = formSection.find(".not-required");
	for (i = 0; i < inputs.length; i++) {
		let inputsValidity = true;
		let radiosValidity = true;
		let checkBoxesValidity = true;
		let textAreaValidity = true;
		if (inputs[i].type === "radio" && $(inputs[i]).checked) {
			radiosValidity = validateRadios(inputs[i].name);
		}
		if (inputs[i].type === "textarea" && !isEmptyOrSpaces($(inputs[i]).val())) {
			textAreaValidity = validateCharacterLength($(inputs[i]));
			if (!textAreaValidity) {
				$(inputs[i]).css("border-color", "red");
				$(`label[for="id_${inputs[i].name}"]`).css("color", "red");
				$(`label[for="id_${inputs[i].name}"]`).text(
					`${inputs[i].name}: Number of words should not exceed 500`
				);
			} else {
				$(`label[for="id_${inputs[i].name}"]`).text(`${inputs[i].name}`);
			}
		}
		let checkBoxParentLabel;
		if (inputs[i].type === "checkbox" && $(inputs[i]).is(":checked")) {
			let checkBoxes = document.getElementsByName(inputs[i].name);
			let checkBoxesSize = parseInt($(checkBoxes).attr("size"));
			let numberOfCheckedItems = 0;
			checkBoxParentLabel = $(`label:contains(${inputs[i].name})`);

			for (let i = 0; i < checkBoxes.length; i++) {
				if (checkBoxes[i].checked) {
					numberOfCheckedItems++;
				}
				if (numberOfCheckedItems === 0) {
					$(checkBoxParentLabel).css("color", "red");
					checkBoxesValidity = false;
				} else {
					checkBoxesValidity = true;
					$(checkBoxParentLabel).css("color", "unset");
				}
			}
			if (numberOfCheckedItems > checkBoxesSize) {
				$(checkBoxParentLabel).css("color", "red");

				if (!$(checkBoxParentLabel).attr("sizeErrorMessageAdded")) {
					$(checkBoxParentLabel)
						.html(
							`${$(
								checkBoxParentLabel
							).text()} Please select a maximum of ${checkBoxesSize} choices`
						)
						.attr("sizeErrorMessageAdded", true);
				}
				checkBoxesValidity = false;
			} else {
				$(checkBoxParentLabel).html(inputs[i].name);
			}
		}
		if (
			!inputsValidity ||
			!radiosValidity ||
			!checkBoxesValidity ||
			!textAreaValidity
		) {
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
				formData = new FormData();
				formData.append(inputs[i].name, $(inputs[i]).val());
				saveDraftData(formData);
			}
			if (inputs[i].type == "radio") {
				if ($(inputs[i]).is(":checked")) {
					formData = new FormData();
					formData.append(inputs[i].name, $(inputs[i]).val());
					saveDraftData(formData);
				}
			}

			if (inputs[i].type == "checkbox") {
				if ($(inputs[i]).hasClass("multiple_checkbox")) {
					let checkBoxes = document.getElementsByName(inputs[i].name);
					let inputValues = [];
					for (let i = 0; i < checkBoxes.length; i++) {
						if ($(checkBoxes[i]).is(":checked")) {
							inputValues.push($(checkBoxes[i]).val());
						}
					}
					formData = new FormData();
					inputValues.forEach((item) =>
						formData.append(checkBoxes[0].name, item)
					);
					saveDraftData(formData);
				} else {
					formData = new FormData();
					formData.append(inputs[i].name, $(inputs[0]).val());
					saveDraftData(formData);
				}
			}
		}
		for (i = 0; i < file_inputs.length; i++) {
			if ($(file_inputs[i])[0].files[0]) {
				formData = new FormData();
				formData.append(file_inputs[i].name, $(file_inputs[i])[0].files[0]);
				saveDraftData(formData);
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
	return isValid;
}

function validateSection(formSection) {
	let isValid = true;
	let inputs = formSection.find(".form-input-validate");
	for (i = 0; i < inputs.length; i++) {
		let inputsValidity = true;
		let radiosValidity = true;
		let checkBoxesValidity = true;
		let textAreaValidity = true;
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
		if (inputs[i].type === "textarea") {
			textAreaValidity = validateCharacterLength($(inputs[i]));
			if (!textAreaValidity) {
				$(inputs[i]).css("border-color", "red");
				$(`label[for="id_${inputs[i].name}"]`).css("color", "red");
				$(`label[for="id_${inputs[i].name}"]`).text(
					`${inputs[i].name}: Number of words should not exceed 500`
				);
			} else {
				$(`label[for="id_${inputs[i].name}"]`).text(`${inputs[i].name}`);
			}
		}
		let checkBoxParentLabel;
		if (inputs[i].type === "checkbox") {
			let checkBoxes = document.getElementsByName(inputs[i].name);
			let checkBoxesSize = parseInt($(checkBoxes).attr("size"));
			let numberOfCheckedItems = 0;
			checkBoxParentLabel = $(`label:contains(${inputs[i].name})`);

			for (let i = 0; i < checkBoxes.length; i++) {
				if (checkBoxes[i].checked) {
					numberOfCheckedItems++;
				}
				if (numberOfCheckedItems === 0) {
					$(checkBoxParentLabel).css("color", "red");
					checkBoxesValidity = false;
				} else {
					checkBoxesValidity = true;
					$(checkBoxParentLabel).css("color", "unset");
				}
			}
			if (numberOfCheckedItems > checkBoxesSize) {
				$(checkBoxParentLabel).css("color", "red");

				if (!$(checkBoxParentLabel).attr("sizeErrorMessageAdded")) {
					$(checkBoxParentLabel)
						.html(
							`${$(
								checkBoxParentLabel
							).text()} Please select a maximum of ${checkBoxesSize} choices`
						)
						.attr("sizeErrorMessageAdded", true);
				}
				checkBoxesValidity = false;
			} else {
				$(checkBoxParentLabel).html(inputs[i].name);
			}
		}
		if (
			!inputsValidity ||
			!radiosValidity ||
			!checkBoxesValidity ||
			!textAreaValidity
		) {
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
				formData = new FormData();
				formData.append(inputs[i].name, $(inputs[i]).val());
				saveDraftData(formData);
			}
			if (inputs[i].type == "radio") {
				if ($(inputs[i]).is(":checked")) {
					formData = new FormData();
					formData.append(inputs[i].name, $(inputs[i]).val());
					saveDraftData(formData);
				}
			}

			if (inputs[i].type == "checkbox") {
				if ($(inputs[i]).hasClass("multiple_checkbox")) {
					let checkBoxes = document.getElementsByName(inputs[i].name);
					let inputValues = [];
					for (let i = 0; i < checkBoxes.length; i++) {
						if ($(checkBoxes[i]).is(":checked")) {
							inputValues.push($(checkBoxes[i]).val());
						}
					}
					formData = new FormData();
					inputValues.forEach((item) =>
						formData.append(checkBoxes[0].name, item)
					);

					saveDraftData(formData);
				} else {
					formData = new FormData();
					formData.append(inputs[i].name, $(inputs[0]).val());
					saveDraftData(formData);
				}
			}
		}
		for (i = 0; i < file_inputs.length; i++) {
			if ($(file_inputs[i])[0].files[0]) {
				formData = new FormData();
				formData.append(file_inputs[i].name, $(file_inputs[i])[0].files[0]);
				saveDraftData(formData);
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
	return isValid;
}

function getTypedWords(typedWords) {
	let words = typedWords.split(" ");
	return words.length;
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

$("textarea").keyup(function () {
	validateCharacterLength($(this));
});

function validateCharacterLength(textarea) {
	var maxLength = 500;
	var words = $(textarea).val().split(" ");
	var len = maxLength - words.length;
	if (len > 0) {
		if ($(textarea).next().length) {
			$(textarea)
				.next()
				.replaceWith(
					$(
						`<p class="textarea-characters-remaining">${len} words remaining</p>`
					)
				);
		} else {
			$(
				`<p class="textarea-characters-remaining">${len} words remaining</p>`
			).insertAfter($(textarea));
		}
		return true;
	} else {
		$(textarea)
			.next()
			.replaceWith(
				$(
					`<p class="textarea-characters-remaining" style="color:red">0 characters remaining</p>`
				)
			);
		return false;
	}
}

function saveDraftData(formData) {
	let application = $("#currentApplication").val();
	var url = `/agripitch/${application}/application/`;
	var CSRFToken = $("input[name=csrfmiddlewaretoken]").val();

	var xhr = new XMLHttpRequest();
	xhr.open("POST", url, true);
	xhr.setRequestHeader("X-CSRFToken", CSRFToken);
	xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("enctype", "multipart/form-data");

	xhr.addEventListener("readystatechange", function (e) {
		if (xhr.readyState === 4 && xhr.status == 201) {
			var response = JSON.parse(xhr.response);
		} else {
			var errors = JSON.parse(xhr.response);
			Object.values(errors).forEach((val) => {
				console.log(val);
			});
		}
	});
	xhr.send(formData);
}

function isEmptyOrSpaces(str) {
	return str === null || str.match(/^ *$/) !== null;
}

// $('#confirmationModal').on('shown.bs.modal', function () {
//   $('#triggerModal').trigger('focus')

// })

// $('#triggerModal').on('click', function () {
//   $('#confirmationModal').modal("show");
// })
