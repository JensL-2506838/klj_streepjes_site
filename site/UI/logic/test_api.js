const test_message = await (await fetch("/api/test")).json();
const users = await (await fetch("/api/users")).json();
window.alert(test_message.message);
console.log(test_message);
console.log(users);
