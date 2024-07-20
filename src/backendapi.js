import { HOST } from './config'


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