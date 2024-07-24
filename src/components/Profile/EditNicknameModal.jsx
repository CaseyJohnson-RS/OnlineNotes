import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { ButtonGroup, Spinner } from 'react-bootstrap';

import { set_nickname } from '../../backendapi';
import { useEffect, useState } from 'react';


function EditNicknameModal(props) {
  
    const [state, setState] = useState("idle")
    const { closeModal, show, setNicknameCallback } = props;
    

    const onSetNickname = () => 
    {
        setState("loading")

        const value = document.getElementById("setNickname_field").value;

        set_nickname(value)
        .then( (resolve) =>
        {
            if (resolve)
            {
                setState("idle");
                setNicknameCallback(value);
            }
            else
                setState("error")
        })
    }

    const handleSubmit = (event) => 
    { 
        const value = event.target.elements.setNickname_field.value;

        event.preventDefault();
        event.stopPropagation();

        if (value.length < 2)
            return;

        onSetNickname();
    };

    const loading = state === "loading"
    const error = state === "error"

    return (
    <>
        <Modal show={show}>
            <Modal.Header>
                Set new nickname
            </Modal.Header>
            <Modal.Body style={{display: loading ? "none" : "block"}} >
                
                <Form noValidate validated={true} onSubmit={handleSubmit}>
                    <Form.Group controlId="setNickname_field" style={{display: error ? "none" : "block"}}>
                        <Form.Control
                            type='text'
                            maxLength={64}
                            minLength={2}
                        />
                    </Form.Group>
                    <span style={{display: error ? "inline" : "none", height: "30px"}}>Sorry, something went wrong...</span>
                    <br />
                    <ButtonGroup style={{width: "100%"}}>
                        <Button  variant="primary" type='submit'>Save</Button>
                        <Button variant="outline-secondary" onClick={ () => {setState("idle"); closeModal("idle"); } }>Close</Button>
                    </ButtonGroup>

                </Form>
           
            </Modal.Body>
            <Spinner animation='grow' style={{display: loading ? "inline" : "none"}}/>
        </Modal>
    </>
    );
}

export default EditNicknameModal;