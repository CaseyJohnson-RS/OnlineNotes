import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { ButtonGroup, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import { set_user_email, set_user_nickname, set_user_password } from '../../backendapi';


function EditModal(props) {
  
    const { closeModal, show, user_id, value, editField } = props;
    const [state, setState] = useState("idle")

    
    const onSubmit = (event) =>
    {
        setState("loading")

        const value = document.getElementById("field").value;

        let promise;

        if (editField === "email")
            promise = set_user_email(user_id, value)

        if (editField === "nickname")
            promise = set_user_nickname(user_id, value)

        if (editField === "password")
            promise = set_user_password(user_id, value)

        promise.then( (response) =>
            {
                if (response)
                {
                    setState("idle")
                    closeModal(value);
                }
                else 
                    setState("error")
            } 
        );

        event.preventDefault();
        event.stopPropagation();
    }


    return (
    <>
        <Modal show={show}>
            <Modal.Body>
                
                <Form onSubmit={onSubmit}>
                    <Form.Control 
                        type="text"
                        id="field"
                        defaultValue={value}
                        size="lg"
                    />
                    <br />

                    {
                        state === "error" ?
                        <span> Something went wrong... sorry...</span> :
                        <></>
                    }

                    <ButtonGroup style={{width: "100%", display: (state === "loading") ? "none" : "block"}}>
                        <Button variant="primary" type='submit'>Save</Button>
                        <Button variant="outline-secondary" onClick={() => closeModal(null)}>Close</Button>
                    </ButtonGroup>

                    {
                        (state === "loading") ? 
                        <Spinner animation='grow' /> :
                        <></>
                    }
                    

                </Form>
           
            </Modal.Body>
        </Modal>
    </>
    );
}

export default EditModal;