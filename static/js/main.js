function validatecomment(loggedIn){
    if (loggedIn == "True") {
        document.getElementById("commentform").submit();
    }
    else {
        alert("You have to login first")
    }
}
function validateMyForm(loggedIn) {
    const days = document.getElementById("days").value;
    if (loggedIn == "True") {
        let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
        modal.show();
    }
    else {
        alert("You have to login first")
    }
}
function validateContactForm() {
    let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
    modal.show();
}