function validateMyForm() {
    const days = document.getElementById("days").value;
    const login = localStorage.getItem("login")
    if(login == "true"){
        let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
        modal.show();
    }
    else{
        alert("You have to login first")  
    }

    
}

function validateContactForm() {
    let modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('exampleModal'))
    modal.show();
}

function logout() {
    localStorage.setItem("login", false)
    window.location.href = "https://grid013.github.io/bikerental/";
}

var navs = document.getElementById("navlist")
const login = localStorage.getItem("login")
if (login == "true") {
    navs.innerHTML += `<li class="nav-item">
    <a class="nav-link fw-bold" onclick="logout()" role="button">Logout</a>
</li>`

}
else {
    navs.innerHTML += `<li class="nav-item">
    <a class="nav-link fw-bold" href="login.html">Login</a>
</li>
<li class="nav-item">
    <a class="nav-link fw-bold" href="register.html">Register</a>
</li>`

}
