const form = document.getElementById("login-form");

// this function checks the database for this username and returns if it exists (boolean)
async function isLoginValid(username) {
    const response = await fetch(
        `/api/isLoginValid?username=${encodeURIComponent(username)}`
    );

    const data = await response.json();

    if (data.status !== 200) {
        throw new Error("Backend function failed");
    }

    return data.valid; // will be true if the username exists
}

// this function redirects the user based on if the username is valid
function redirectUser(valid) {
    if (valid) {
        console.log("login successful")
        window.location.href = "../HTML/dashboard.html";
    } else {
        window.alert("username is not registered")
        window.location.reload();
    }
}

// this event listener submits the username and routes based on the success
form.addEventListener("submit", async (event) => {
    event.preventDefault();     // prevents the browsers default action, such as reloading the page

    // Read the submitted username
    const userName = (new FormData(form)).get("username");

    // validate the username and redirect the user
    try {
        const valid = await isLoginValid(userName);
        redirectUser(valid);
    } catch (e) {
        console.error(e)
        return false;
    }
})