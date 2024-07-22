import { HOST } from './config'


export async function server_hi()
{
    const url = HOST + "hi";
    const options = { method: 'GET' };

    try {
        const response = await fetch(url, options);
        
        if (!response.ok) 
            return false;
        
        return true;
    } catch (error) {
        return false;
    }
}


export async function get_profile_info(token) 
{
    const url = HOST + "profile-info"
    const options = {
        method: 'GET',
        headers: { "Authorization": "Bearer " + token },
    }

    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
          throw new Error("Response status: " + response.status + "}");
        }
        
        return await response.json();

    } catch (error) {
        console.error(error.message);
    }

    return null
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


export async function sign_in(username, password)
{
    const formData = new FormData();

    formData.append("username", username);
    formData.append("password", password);

    const url = HOST + "token";
    const options = { method: 'POST', body: formData };

    try {
        const response = await fetch(url, options);

        if (!response.ok)
            return false

        const json = await response.json();

        localStorage["token"] = json["access_token"];
        return true
    } catch (e) {
        console.error(e);
    }

    return false
}


export async function sign_up(username, nickname, password)
{
    localStorage["sign_up_username"] = username;

    let data = new FormData();

    data.append("username", username);
    data.append("password", password);
    data.append("nickname", nickname);

    const url = HOST + "sign-up";
    const options = { method: 'POST', body: data };

    try {
        const response = await fetch(url, options);
        const ans = await response.json();

        if (!response.ok)
            return false;

        return ans;
    } catch (e) {
        console.error(e);
    }

    return false;
}


export async function sign_up_confirm(code)
{
    const sign_up_username = localStorage["sign_up_username"];
    localStorage.removeItem("sign_up_username")

    let data = new FormData();

    data.append("username", sign_up_username);
    data.append("confirm_seq", code);

    const url = HOST + "sign-up-confirm";
    const options = { method: 'POST', body: data };

    try {
        const response = await fetch(url, options);

        if (!response.ok)
            return false

        const json = await response.json();

        localStorage["token"] = json["access_token"];
        return true
    } catch (e) {
        console.error(e);
    }

    return false
}


export async function check_email_is_avalilable(email)
{
    const url = HOST + "username-exist?" + new URLSearchParams({username: email}).toString();
    const options = { method: 'POST' }

    try {
        const response = await fetch(url, options);

        if (!response.ok)
            return false

        return !(await response.json());
    } catch (e) {
        console.error(e);
    }

    return false;
}


export async function restore_password(username)
{
    let data = new FormData();

    data.append("username", username);

    const url = HOST + "restore-password";
    const options = { method: 'POST', body: data };

    try {
        const response = await fetch(url, options);

        if (!response.ok) 
            return false

        const ans = await response.json()

        if (ans)
            localStorage["restore_password_username"] = username;

        return true;
    } catch (e) {
        console.error(e);
    }

    return false
}

export async function restore_password_confirm(code)
{
    const restore_password_username = localStorage["restore_password_username"]

    let data = new FormData();

    data.append("username", restore_password_username);
    data.append("confirm_seq", code)

    const url = HOST + "restore-password-confirm";
    const options = { method: 'POST', body: data };

    try {
        const response = await fetch(url, options);

        if (!response.ok)
            return false

        return (await response.json())
    } catch (e) {
        console.error(e);
    }

    return false
}


export async function set_new_password(password)
{
    const restore_password_username = localStorage["restore_password_username"]

    let data = new FormData();

    data.append("username", restore_password_username);
    data.append("password", password)

    const url = HOST + "set-new-password";
    const options = { method: 'POST', body: data };

    try {
        const response = await fetch(url, options);

        if (!response.ok)
            return false

        const json = await response.json()

        localStorage["token"] = json["access_token"]

        return true
    } catch (e) {
        console.error(e);
    }

    return false
}