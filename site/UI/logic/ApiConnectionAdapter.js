import ApiConnection from "./ApiConnection.js"

export class ApiConnectionAdapter {
    #api;

    constructor() {
        this.#api = new ApiConnection();
    }

    async userExists(username) {
        try {
            return this.#api.userExists(username);
        } catch(e) {
            throw e;
        }
    }
}

