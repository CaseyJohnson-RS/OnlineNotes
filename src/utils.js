import { get_profile_info, server_hi } from './backendapi'


async function validate_token(token) 
{ 
    const res = await get_profile_info(token)

    return !(res === null) 
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


export async function check_server_connection()
{
    return (await server_hi()) // return bool
}


export async function get_active_token() 
{ 
    const token = localStorage.getItem("token")

    if (token === null)
        return null;

    const token_is_valid = await validate_token(token)

    if (!token_is_valid)
    {
        localStorage.removeItem("token")
        return null;
    }

    return token
}


export function check_email_is_avalilable(email)
{
    
}


export function validate_email(email) 
{
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,})+$/.test(email));
}


export function validate_password(password)
{

}