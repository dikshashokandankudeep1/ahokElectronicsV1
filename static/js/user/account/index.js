function funcEdit(idType) {
    if ('personalInfo' == idType) {
        hideId('personalInfo_def_edit');
        hideId('personalInfo_def_name');
        hideId('personalInfo_def_gender');

        showId('personalInfo_name');
        showId('personalInfo_gender');
        showId('personalInfo_cancel');
    } else if ('emailAddress' == idType) {
        hideId('emailAddress_def_email');
        hideId('emailAddress_def_edit');
        showId('emailAddress_email');
        showId('emailAddress_cancel');

    } else if ('mobileNumber' == idType) {
        hideId('mobileNumber_def_mobile');
        hideId('mobileNumber_def_edit');
        showId('mobileNumber_mobile');
        showId('mobileNumber_cancel');
    }
}

function funcCancel(idType) {
    if ('personalInfo' == idType) {
        showId('personalInfo_def_edit');
        showId('personalInfo_def_name');
        showId('personalInfo_def_gender');
        hideId('personalInfo_name');
        hideId('personalInfo_gender');
        hideId('personalInfo_cancel');

    } else if ('emailAddress' == idType) {
        showId('emailAddress_def_email');
        showId('emailAddress_def_edit');
        hideId('emailAddress_email');
        hideId('emailAddress_cancel');

    } else if ('mobileNumber' == idType) {
        showId('mobileNumber_def_mobile');
        showId('mobileNumber_def_edit');
        hideId('mobileNumber_mobile');
        hideId('mobileNumber_cancel');
    }
}

function proceedToPasswordChangeButtonValidation(button) {
    if (document.getElementById("newPassword").value != document.getElementById("retypeNewPassword").value) {
        button.setCustomValidity(
            'Password change failed. New Passwords do not match');
    } else {
        button.setCustomValidity('');
    }
}