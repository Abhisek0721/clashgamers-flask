function validLogin(form) {
    var username = form.username.value;
    var password = form.password.value;

    let space = / /;
    if(space.test(username) & space.test(password)){
        alert("\n Username/Password should not have space!");
        return false;
    }else{
        return true;
    };

};
