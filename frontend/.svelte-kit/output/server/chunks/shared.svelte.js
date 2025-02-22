import "clsx";
const PUBLIC_API_BASE_URL = "/api/v1";
const api_url = PUBLIC_API_BASE_URL;
class UserState {
  //localStorage is not reactive
  // => so I made user methods a part of this class so values can be kept up to date manually (in login, logout)
  token = localStorage.getItem("token");
  //wrapping this in $state() does not make it change when storage changes, 
  //but it is needed because name is displayed in UI
  //(else the UI (in +layout.svelte shows nothing):
  name = localStorage.getItem("username");
  //derived didnt work here, because token is not a $state() vriable (thats ok)
  loggedIn = this.token !== null;
  uuid = localStorage.getItem("uuid");
  isAdmin = localStorage.getItem("isAdmin");
  elo = localStorage.getItem("elo");
  wins = localStorage.getItem("wins");
  draws = localStorage.getItem("draws");
  losses = localStorage.getItem("losses");
  async login(username, password) {
    const request = await fetch(`${api_url}/login`, {
      method: "POST",
      body: JSON.stringify({ username, password }),
      headers: { "Content-Type": "application/json" }
    });
    if (request.ok) {
      this.loggedIn = true;
    } else {
      if (request.status == 404) {
        throw Error("Takového uživatele neznáme. \n Zkontrolujte, zda jste v přihlašovacím jméně nenapsali překlep.");
      }
      if (request.status == 401) {
        throw Error("Zkontrolujte, zda jste v hesle nenapsali překlep.");
      }
    }
    try {
      const response = await request.json();
      localStorage.setItem("token", response.token);
      localStorage.setItem("username", username);
      localStorage.setItem("uuid", response.uuid);
      localStorage.setItem("isAdmin", response.is_admin);
      this.token = response.token;
    } catch (e) {
      console.error(e);
    }
  }
  logout() {
    this.loggedIn = false;
    this.token = null;
    this.name = null;
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("uuid");
  }
  async signUp(username, email, password) {
    const request = await fetch(`${api_url}/users`, {
      method: "POST",
      body: JSON.stringify({ username, email, password, elo: 400 }),
      headers: { "Content-Type": "application/json" }
    });
    const data = await request.json();
    if (request.status == 409) {
      if (data.message == "User with this username already exists") {
        throw Error("Toto uživatelské jméno již někdo používá. \n Zvolte jiné");
      } else if (data.message == "User with this email already exists") {
        throw Error("Tento email již nějaký účet používá. \n Zvolte jiný");
      }
    }
    if (request.status == 400) {
      throw Error("Vyplňte prosím všechna pole formuláře.");
    }
    console.log("signUp response", data);
    this.name = username;
    this.elo = data.elo;
    this.wins = data.wins;
    this.draws = data.draws;
    this.losses = data.losses;
    this.uuid = data.uuid;
    localStorage.setItem("uuid", data.uuid);
    console.log("uuid", data.uuid);
    await this.login(username, password);
  }
  async delete() {
    const request = await fetch(`${api_url}/users/${this.uuid}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`
      }
    });
    if (request.status == 404) {
      throw Error("Uživatel nenalezen \n Pravděpodobně už jste účet smazali. \n Obnovte stránku.");
    }
    if (request.ok) {
      this.logout();
      return true;
    }
    return false;
  }
  async editUser(toChange) {
    console.log("Sending", JSON.stringify(toChange));
    const request = await fetch(`${api_url}/users/${this.uuid}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`
      },
      body: JSON.stringify(toChange)
    });
    await request.json();
    if (request.ok) {
      return true;
    }
    return false;
  }
  async changePassword(password) {
    if (password == void 0) {
      throw Error("Supply password string");
    }
    let changes = { "password": password };
    let ok = await this.editUser(changes);
    return ok;
  }
  async changeName(name2) {
    if (name2 == void 0 || name2 == null) {
      throw Error("Supply name string");
    }
    let changes = { "username": name2 };
    let ok = await this.editUser(changes);
    if (ok) {
      this.name = name2;
      localStorage.setItem("username", name2);
      return true;
    }
    return false;
  }
  async changeEmail(email) {
    if (name == void 0 || name == null) {
      throw Error("Supply name string");
    }
    let changes = { "email": email };
    let ok = await this.editUser(changes);
    return ok;
  }
  async getUsers() {
    const request = await fetch(`${api_url}/users`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`
      }
    });
    const response = await request.json();
    return response;
  }
}
let User = new UserState();
export {
  User as U
};
