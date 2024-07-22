import { useState, useEffect } from 'react';
import { sign_up, set_new_password } from '../../backendapi';
import { set_app_state } from '../../appcontoller'
import { validate_password } from '../../utils';

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"


function SetNewPassword(props) {

    const [formState, setState] = useState(false);
    const { rerender } = props

    const custom_validation = () =>
        {
            document.getElementById('set_new_password_password').addEventListener('input', function() {
                this.setCustomValidity( validate_password(this.value) ? '' : 'err' );
            });

            document.getElementById('set_new_password_password_confirm').addEventListener('input', function() {
                const res = document.getElementById('set_new_password_password').value === this.value;
                this.setCustomValidity( res ? '' : 'err' );
            });
        }

    const handleSubmit = (event) => 
        { 
            const form = event.currentTarget;
        
            if (form.checkValidity() === true) 
            {
                setState("setting_password");
        
                set_new_password(
                    event.target.elements.set_new_password_password.value
                ).then( (result) => 
                    {
                        if (result)
                        {
                            setTimeout( () =>
                                {
                                    set_app_state("main-page");
                                    rerender();
                                },
                                1500
                            );
                            
                            setState("success");
                        } else 
                        {
                            setState("error");
                        }
                    }
                );
            } else
                setState("validated");
        
            event.preventDefault();
            event.stopPropagation();
        };

    useEffect(custom_validation)

    return (
        <>
            <Form noValidate validated={formState === "validated"} onSubmit={handleSubmit}>

                <Form.Group as={Row} controlId="set_new_password_password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                    required
                    type="password"
                    placeholder="***********"
                    autoFocus={true}
                />
                <Form.Control.Feedback>What a great password!</Form.Control.Feedback>
                <Form.Control.Feedback type='invalid'>From 8 to 32 characters</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "15px"}}></Row>

                <Form.Group as={Row} controlId="set_new_password_password_confirm">
                <Form.Label>Repeat password</Form.Label>
                <Form.Control
                    required
                    type="password"
                    placeholder="***********"
                />
                <Form.Control.Feedback>Absolute coincidence!</Form.Control.Feedback>
                <Form.Control.Feedback type='invalid'>Not alike</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "25px"}}></Row>
                <Row style={{display: formState !== "success" ? "flex" : "none"}}>
                    
                    {
                        formState === "setting_password" ?
                        <Spinner animation="grow" />:
                        <Button type="submit">Confirm</Button>
                    }
                    
                    <Row style={{height: "15px"}} ></Row>
                    
                    {
                        formState === "error" ?
                        <span className="text-danger">Something went wrong...</span>:
                        <></>
                    }
                    
                </Row>

                <Row style={{display: formState === "success" ? "flex" : "none"}}>
                    
                    <Col xs={10}><h4 className='text-success'>Successful!</h4></Col>
                    
                </Row> 


            </Form>
        </>
    );
}

export default SetNewPassword;