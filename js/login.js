function login() {
    console.log("lgon");
    const form = document.getElementById("loginform")
    const username = form.username.value;
    const password = form.password.value;

    var users = localStorage.getItem("users")
    const msg = document.getElementById("message")
    if (users) {
        var uu = JSON.parse(users)
        console.log(uu)
        var result = uu.find(
            function (str) {
                const jj = JSON.parse(str)
                console.log(jj.email)
                return jj.email == username;
            }
        );
        if (result) {
            obj = JSON.parse(result)
            if (obj.password == password) {
                localStorage.setItem("login", true)
                window.location.href = "/";
            }
            else {
                msg.innerHTML = `<p style="color:red">Wrong password</p>`;
            }
        }
        else {
            msg.innerHTML = `<p style="color:red">No user exists with this email. Please register first.</p>`;
        }
    }
    else {
        msg.innerHTML = `<p style="color:red">No user exists with this email. Please register first.</p>`;
    }

}