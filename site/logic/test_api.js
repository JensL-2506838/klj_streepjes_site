const test_message = await (await fetch('/api/test')).json();
window.alert(test_message)