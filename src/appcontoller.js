import { get_active_token, check_server_connection } from './utils'

let auth_states = [
    "authorization",
    "registration",
    "registration-confirm",
    "restore-password",
    "restore-password-confirm",
    "set-new-password",
]

let session_states = [
    "main-page",
]

let special_states = [
    "server-error"
]

let states = session_states + auth_states + special_states
Object.freeze(states)

let app_state = null
let token = null

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export function set_app_state(state)
{
    console.log("set_app_state(" + state + ")")
    if (states.includes(state)) 
    {
        app_state = state;
        localStorage["app_state"] = app_state;
    }
    else
        console.log("State '" + state + "' is not registred!");
}

export function get_app_state() 
{ 
    if (app_state === "server-error")
        return app_state
    
    if (token === null)
        set_app_state("authorization")
    else
    {
        if (app_state !== null && !auth_states.includes(app_state))
            return app_state

        let saved_state = localStorage.getItem("app_state");

        if (saved_state === null || auth_states.includes(saved_state))
            set_app_state("main-page")
    }

    return app_state
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

let server_is_ready = await check_server_connection()

if (server_is_ready)
{
    token = await get_active_token()

    if (token === null)
        console.log("No token. Need authrization...")
    else 
        console.log("Token is valid. Authorized")
}
else set_app_state("server-error")