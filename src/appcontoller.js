import { get_active_token, check_server_connection, set_app_theme } from './utils'
import { get_profile_info } from './backendapi'

export const auth_states = [
    "authorization",
    "registration",
    "registration-confirm",
    "restore-password",
    "restore-password-confirm",
    "set-new-password",
]

export const session_states = [
    "main-page",
]

export const special_states = [
    "checking-server",
    "server-not-responding"
]

const states = session_states + auth_states + special_states


let app_state = "checking-server"
let token = null

let initialized = false

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export function set_app_state(state)
{
    console.log("App state: " + state)
    if (session_states.includes(state) || auth_states.includes(state)) 
    {
        app_state = state;
        localStorage["app_state"] = app_state;
    }
    else
        console.error("Setting state '" + state + "' is not alowed");
}


export function get_app_state() 
{ 
    if (app_state !== null && states.includes(app_state))
        return app_state

    const storaged_state = localStorage.getItem("app_state")

    if (token !== null)
    {
        if (storaged_state === null || !session_states.includes(storaged_state))
            app_state = "main-page"
        else
            app_state = storaged_state
    } else
    {
        if (storaged_state === null || !auth_states.includes(storaged_state))
            app_state = "authorization"
        else
            app_state = storaged_state
    }

    set_app_state(app_state)

    return app_state
}


export async function load_token()
{
    token = await get_active_token()

    if (token === null)
        console.log("No token: need authrization")
    else 
        console.log("Token is valid: authorized")
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


export async function initialize()
{
    if (initialized) return false;// Rerendering app flag

    set_app_theme();

    let is_server_ready = await check_server_connection();

    console.log("Server connection: " + is_server_ready)

    if (!is_server_ready) app_state = "server-not-responding";
    else {
        await load_token();
        const obj = await get_profile_info(token);
        if (obj !== null)
            localStorage["profile_info"] = JSON.stringify(obj);
        app_state = null;
    }
    
    initialized = true;
    return true; // Rerendering app flag
}