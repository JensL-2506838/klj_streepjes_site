const form = document.getElementById("login-form");

// this function checks the database for this username and returns if it exists (boolean)
async function getBackendResponse(username) {

}

// this event listener submits the username and routes based on the succes
form.addEventListener("submit", async (event) => {
    event.preventDefault();     // prevents the browsers default action, such as reloading the page

    // Read the submitted username
    const userName = (new FormData(form)).get("username");


})