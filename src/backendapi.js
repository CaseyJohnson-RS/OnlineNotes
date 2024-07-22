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
    return new Promise( (resolve, reject) => 
    {
        setTimeout( ()=>resolve(false), 1000 );
    });
}

let last_username = null

export async function sign_up(username, nickname, password)
{
    return new Promise( (resolve) => 
    {
        setTimeout( ()=>resolve(false), 1000 );
    });
}

export async function sign_up_confirm(code)
{
    return new Promise( (resolve) => 
        {
            setTimeout( ()=>resolve(true), 1000 );
        });
}


export async function check_email_is_avalilable(email)
{
    return new Promise( (resolve) => 
    {
        setTimeout( ()=>resolve(true), 1000 );
    });
}


export async function restore_password(username)
{
    return new Promise( (resolve) => 
    {
        setTimeout( ()=>resolve(true), 1000 );
    });
}