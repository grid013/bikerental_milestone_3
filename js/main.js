function validateMyForm() {
    const days = document.getElementById("days").value;
    let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
    modal.show();
}

function validateContactForm(){
    let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
    modal.show();
}