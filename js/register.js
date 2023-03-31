function register() {
    // Check if any users object exists in local storage or not
    let users = localStorage.getItem("users");
    if (users) {
        console.log("users")
    }
    else {
        users = []
        localStorage.setItem("users", JSON.stringify(users))
    }
    // -------------------------------------------
    const form = document.getElementById("register_form")
    var formData = new FormData(form)
    const email = formData.get("email")
    const password = formData.get("password")
    const confirm_password = formData.get("confirm_password")
    if(password != confirm_password){
        document.getElementById("msg").innerHTML=`<div class="error">Password and confirm password dosen't match!</div>`
        return false;

    }
    let result = users.includes(email);
    if (result) {
        // alert("this email already exists")
        const html = `<div class="error">This email already exists!!</div>`
        document.getElementById("msg").innerHTML=html
        return false;
    }
    else {
        console.log("registering user")
        var object = {};
        formData.forEach((value, key) => object[key] = value);
        var json = JSON.stringify(object);
        var uu = JSON.parse(localStorage.getItem("users"))
        uu.push(json)
        localStorage.setItem("users", JSON.stringify(uu))
        const html = `<div class="success">Thanks for registering with us..now you can login</div>`
        document.getElementById("msg").innerHTML=html
        form.reset()

    }

}