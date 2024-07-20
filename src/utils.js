import { get_profile_info } from './backendapi'


async function validate_token(token) 
{ 
    const res = await get_profile_info(token)

    return !(res === null) 
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

