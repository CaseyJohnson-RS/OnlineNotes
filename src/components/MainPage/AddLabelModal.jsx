import { useState, useEffect } from 'react';

import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';


import { create_label } from '../../backendapi';


function AddLabelModal(props) {

    const [state, setState] = useState("")
  
    const { closeModal, show, label_list, onAddLabel } = props;

    const custom_validation = () =>
    {
        if (!show)
            return
        document.getElementById('new_label_field').addEventListener('input', function() {
            if(this.value.length === 0 || label_list.includes(this.value))
            {
                setState("invalid")
                this.setCustomValidity('err');
            }
            else
            {
                setState("valid");
                this.setCustomValidity('');
            }            
        });
    }

    const handleSubmit = (event) => 
        { 
            setState("creating_label");
            create_label(event.target.elements.new_label_field.value)
            .then( (result) =>
            {
                if (result)
                {
                    setState("");
                    onAddLabel();
                } 
                else 
                    setState("error");

            })
        
            event.preventDefault();
            event.stopPropagation();
        };

    useEffect(custom_validation)


    return (
    <>
        <Modal show={show}>
            <Modal.Body>

                <Spinner animation='grow' style={{display: state === "creating_label" ? "inline-block" : "none"}}/> 
                <div style={{display: state === "error" ? "inline" : "none"}}>
                    <span >Something went wrong. Sorry...</span>
                </div>
                

                <Form validated={state !== ""} onSubmit={handleSubmit}>
                    <Form.Group className="mb-3" controlId="new_label_field" style={{display: state !== "error" && state !== "creating_label" ? "block" : "none"}}>
                        <Form.Label>New label</Form.Label>
                        <Form.Control type="text" placeholder="Some name" maxLength={16}/>
                        <Form.Control.Feedback type='invalid'>Label can't be empty or such a name already exists</Form.Control.Feedback>
                        <Form.Control.Feedback>Looks awesome!</Form.Control.Feedback>
                    </Form.Group>
                    <ButtonGroup style={{width: "100%"}}>
                        <Button variant="outline-secondary" onClick={closeModal}>Cancel</Button>
                        <Button variant="primary" type='submit' disabled={state !== "valid"}>Add</Button>
                    </ButtonGroup>
                </Form>
           
            </Modal.Body>
        </Modal>
    </>
    );
}

export default AddLabelModal;