import { useState, useCallback } from 'react';
import { delete_user_account, get_user, set_user_active } from '../backendapi';
import { set_app_state } from '../appcontoller'

import { Row, Col, Button, Spinner, Form } from 'react-bootstrap';
import EditModal from '../components/Admin.jsx/EditModal';


let user;
let value;
let editField;


function SetActiveButton(props)
{
    const [state, setState] = useState("idle")

    const onClick = () => 
    {
        if (!user)
            return

        setState("loading")

        set_user_active(user.id, !user.active)
        .then( (res) =>{
            if (res) {
                user.active = !user.active;
                props.rerender();
            }
                
            setState("idle")
        })
    }

    return ( <>
        {
            state === "loading" ?
            <Spinner animation='grow' /> :
            <Button style={{width: "100%"}} onClick={onClick}>
                { 
                    (user && user.active) ?
                    "Deactivate" :
                    "Activate"
                }
            </Button>
        }    
    </>)
}


function DeleteButton(props)
{
    const [state, setState] = useState("idle")

    const onClick = () => 
    {
        if (!user)
            return

        setState("loading")

        delete_user_account(user.id)
        .then( (res) =>{
            if (res) {
                user = null;
                props.rerender();
            }
                
            setState("idle")
        })
    }

    return ( <>
        {
            state === "loading" ?
            <Spinner animation='grow' /> :
            <Button style={{width: "100%"}} onClick={onClick} variant='outline-danger'>Delete user</Button>
        }    
    </>)
}


function Admin(props) {

    const { app_rerender } = props;

    const [state, setState] = useState("no-info")
    const [modalState, setModalState] = useState(false)
    const [, updateState] = useState();
    const rerender = useCallback(() => updateState({}), []);

    const onEdit = (_editField, _value) =>
    {
        value = _value;
        editField = _editField;
        setModalState(true)
    }

    const onCloseModal = (_value) =>
    {
        if (_value !== null)
        {
            if (editField === "email")
                user.email = _value;
            else if (editField === "nickname")
                user.nickname = _value;
        }
        setModalState(false);
    }

    const handleSubmit = (event) =>
    {
        setState("loading")

        const value = document.getElementById("search").value;

        get_user(value)
        .then( (resp) =>
        {
            if (resp !== null)
            {
                user = resp;
                setState("user-edit")
            }
            else
                setState("no-info")
        })

        event.preventDefault();
        event.stopPropagation();
    }

    const no_info = <Row><h4 style={{opacity: "50%", textAlign: "center", padding: "30px"}}>No user to edit</h4></Row>
    const loading = <Row><h4 style={{opacity: "50%", textAlign: "center", padding: "30px"}}>Loading... <Spinner animation='grow' /></h4></Row>
    const user_edit = <Row>
        <EditModal closeModal={ onCloseModal } show={modalState} user_id={user && user.id} value={value} editField={editField} />
        <Col>
            <Row style={{margin: "50px 10px", opacity: "50%"}}>
                <Col xs={3}>
                    <h3>User id:</h3>
                </Col>
                <Col xs={6}>
                    <h3>{user && user.id}</h3>
                </Col>
            </Row>

            <Row style={{margin: "35px 10px"}}>
                <Row>
                    <Col xs={3}>
                        <h5>Email</h5>
                    </Col>
                    <Col xs={9} className='text-end'>
                        <h5>{user && user.email}</h5>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <Button style={{width: "100%"}} onClick={() => onEdit("email", user && user.email)}>Edit</Button>
                    </Col>
                </Row>
            </Row>

            <Row style={{margin: "35px 10px"}}>
                <Row>
                    <Col xs={3}>
                        <h5>Nickname</h5>
                    </Col>
                    <Col xs={9} className='text-end'>
                        <h5>{user && user.nickname}</h5>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <Button style={{width: "100%"}} onClick={() => onEdit("nickname", user && user.nickname)}>Edit</Button>
                    </Col>
                </Row>
            </Row>

            <Row style={{margin: "35px 10px"}}>
                <Row>
                    <Col xs={3}>
                        <h5>Password</h5>
                    </Col>
                    <Col xs={9} className='text-end'>
                        <h5>************</h5>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <Button style={{width: "100%"}} onClick={() => onEdit("password", "")}>Edit</Button>
                    </Col>
                </Row>
            </Row>

            <Row style={{margin: "35px 10px"}}>
                <Row>
                    <Col xs={3}>
                        <h5>Status</h5>
                    </Col>
                    <Col xs={9} className='text-end'>
                        <h5 className={'text-' + ((user && user.active) ? "success" : "danger")}>{ (user && user.active) ? "active" : "inactive" }</h5>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <SetActiveButton rerender={rerender}/>
                    </Col>
                </Row>
            </Row>

            <Row style={{margin: "70px 10px"}}>
                <Col xs={3}>
                    <DeleteButton rerender={ () => setState("no-info") }/>
                </Col>
            </Row>

        </Col>
    </Row>

    return (
    <>
        <Row style={{height: "30px"}}/>
        <Row> <Col xs={3}><Button onClick={() => { set_app_state("main-page"); app_rerender(); }} variant='outline-secondary'>Back</Button></Col></Row>
        <Row style={{height: "30px"}}/>
        <Row>
        <Col xs={8}>
            
            <Form noValidate onSubmit={handleSubmit}>
            <Row>
                <Col xs={10}>
                    <Form.Group controlId='search'>
                        <Form.Control 
                            type='email'
                            maxLength={256}
                            placeholder='Enter user email'
                            disabled={state === "loading"}
                        />
                    </Form.Group>
                </Col>
                <Col xs={2}>
                <Button 
                    type='submit' 
                    variant='outline-secondary'
                    disabled={state === "loading"}
                    style={{width: "100%"}}
                    > 
                    Search
                </Button>
                </Col>
                </Row>
            </Form>

            {
                state === "no-info" ?
                no_info :
                state === "loading" ?
                loading :
                state === "user-edit" ?
                user_edit : <></>
                
            }
            
        </Col>
        </Row>
    </>
    );
}

export { Admin }