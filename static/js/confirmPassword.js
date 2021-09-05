function checkPassword(form) {
    var password1 = form.Password.value;
    var password2 = form.RetypePassword.value;
    let space = / /;
    let digit = /\d/;

    if (password1 != password2) {
        alert("\n Your Password doesn't match with Confirm Password.\n Please try again.");
        return false;
    } else {
        if (password1.length<8) {
            alert("\n Your Password should not be less than 8 characters.");
            return false;
        } else {
            if(space.test(password1)){
                alert("\n Password should not have space!");
                return false;
            };
            if(digit.test(password1) != true){
                alert("\n Password should contain at least one digit.\n example: abhisek3");
                return false;
            };
            return true;
        };
    };
};