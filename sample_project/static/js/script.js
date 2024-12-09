const validateFirstName = (firstName) => {
    const regex = /^[A-Za-z\s]+$/;
    const repeatedCharRegex = /(.)\1{2,}/;
    const maxLength = 20;

    if (!firstName) return "First name is required.";
    if (!regex.test(firstName.trim())) return "First name must not contain special characters or numbers.";
    if (firstName.trim().length < 3) return "First name must be at least 3 characters long.";
    if (firstName.trim().length > maxLength) return `First name must be at most ${maxLength} characters long.`;
    if (repeatedCharRegex.test(firstName.trim())) return "First name must not contain repeated characters.";
    return "";
};

const validateMiddleName = (middleName) => {
    const regex = /^[A-Za-z\s]+$/;
    const repeatedCharRegex = /(.)\1{2,}/;
    const maxLength = 20;

    if (middleName && !regex.test(middleName.trim())) return "Middle name must not contain special characters or numbers.";
    if (middleName && middleName.trim().length < 3) return "Middle name must be at least 3 characters long.";
    if (middleName && middleName.trim().length > maxLength) return `Middle name must be at most ${maxLength} characters long.`;
    if (middleName && repeatedCharRegex.test(middleName.trim())) return "Middle name must not contain repeated characters.";
    return "";
};

const validateLastName = (lastName) => {
    const regex = /^[A-Za-z\s]+$/;
    const repeatedCharRegex = /(.)\1{2,}/;
    const maxLength = 20;

    if (!lastName) return "Last name is required.";
    if (!regex.test(lastName.trim())) return "Last name must not contain special characters or numbers.";
    if (lastName.trim().length < 3) return "Last name must be at least 3 characters long.";
    if (lastName.trim().length > maxLength) return `Last name must be at most ${maxLength} characters long.`;
    if (repeatedCharRegex.test(lastName.trim())) return "Last name must not contain repeated characters.";
    return "";
};

const validateBirthday = (birthday, age) => {
    if (!birthday) return "Birthday is required.";

    const birthdayDate = new Date(birthday);
    const currentDate = new Date();
    const sixtyYearsAgo = new Date("1964-01-01");

    if (birthdayDate > currentDate) return "Birthday cannot be a future date.";
    if (birthdayDate < sixtyYearsAgo) return "The birthdate must not be earlier than January 1, 1964.";
    if (isNaN(birthdayDate.getTime())) return "Invalid date format.";

    const calculatedAge = currentDate.getFullYear() - birthdayDate.getFullYear();
    const isBirthdayPastThisYear = currentDate.getMonth() > birthdayDate.getMonth() ||
        (currentDate.getMonth() === birthdayDate.getMonth() && currentDate.getDate() >= birthdayDate.getDate());
    const finalCalculatedAge = isBirthdayPastThisYear ? calculatedAge : calculatedAge - 1;

    if (Number(finalCalculatedAge) !== Number(age)) {
        return `The age (${age}) does not match the birthday.`;
    }

    return "";
};

const validateAge = (age) => {
    if (!age) return "Age is required.";
    if (age < 18) return "Age does not align with your given birthday.";
    if (age > 60) return "Age does not align with your given birthday";
    return "";
};

const validateContactNumber = (contactNumber) => {
    const regex = /^09\d{9}$/;

    if (!contactNumber) return "Contact number is required.";

    const trimmedContactNumber = contactNumber.trim();

    if (!regex.test(trimmedContactNumber)) {
        return "Contact number must be a valid Philippine mobile number.";
    }

    if (/(\d)\1{3,}/.test(trimmedContactNumber)) {
        return "Contact number must not contain 4 or more repeating digits.";
    }

    return "";
};

const submitLink = document.getElementById("submitLink");

// Get the URL from the `url_for` function and ensure it's passed correctly
const redirectUrl = "{{ url_for('blueprint.info') }}";

// Event listener for the <a> tag
submitLink.addEventListener("click", (event) => {
    event.preventDefault();  // Prevent default <a> behavior (navigation)

    // Clear existing error messages
    const firstNameError = document.getElementById("firstNameError");
    const middleNameError = document.getElementById("middleNameError");
    const lastNameError = document.getElementById("lastNameError");
    const birthdayError = document.getElementById("birthdayError");
    const ageError = document.getElementById("ageError");
    const contactnumberError = document.getElementById("contactnumberError");
    const emailError = document.getElementById("emailError");

    firstNameError.textContent = "";
    middleNameError.textContent = "";
    lastNameError.textContent = "";
    birthdayError.textContent = "";
    ageError.textContent = "";
    contactnumberError.textContent = "";
    emailError.textContent = "";

    // Get validation messages from your validation functions
    const firstNameValidationMessage = validateFirstName(firstNameInput.value);
    const middleNameValidationMessage = validateMiddleName(middleNameInput.value);
    const lastNameValidationMessage = validateLastName(lastNameInput.value);
    const birthdayValidationMessage = validateBirthday(birthdayInput.value, ageInput.value);
    const ageValidationMessage = validateAge(ageInput.value);
    const contactnumberValidationMessage = validateContactNumber(contactnumberInput.value);
    const emailValidationMessage = validateEmail(emailInput.value);

    let hasErrors = false;

    // Check if there are validation errors
    if (firstNameValidationMessage) {
        firstNameError.textContent = firstNameValidationMessage;
        hasErrors = true;
    }
    if (middleNameValidationMessage) {
        middleNameError.textContent = middleNameValidationMessage;
        hasErrors = true;
    }
    if (lastNameValidationMessage) {
        lastNameError.textContent = lastNameValidationMessage;
        hasErrors = true;
    }
    if (birthdayValidationMessage) {
        birthdayError.textContent = birthdayValidationMessage;
        hasErrors = true;
    }
    if (ageValidationMessage) {
        ageError.textContent = ageValidationMessage;
        hasErrors = true;
    }
    if (contactnumberValidationMessage) {
        contactnumberError.textContent = contactnumberValidationMessage;
        hasErrors = true;
    }
    if (emailValidationMessage) {
        emailError.textContent = emailValidationMessage;
        hasErrors = true;
    }

    // If there are no errors, proceed with the redirection (submit)
    if (!hasErrors) {
        window.location.href = redirectUrl;  // Manually redirect to the desired page
    }
});
