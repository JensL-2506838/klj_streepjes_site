export class ApiConnection {
    /**
     * Checks whether a username exists.
     * @param {string} username
     * @returns {Promise<boolean>}
     */
    async userExists(username) {
        const response = await fetch(
            `/api/isLoginValid?username=${encodeURIComponent(username)}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        return Boolean(data.valid);
    }
}