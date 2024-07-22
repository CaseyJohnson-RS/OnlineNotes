import { useState, useEffect } from 'react';
import { sign_up, check_email_is_avalilable } from '../../backendapi';
import { set_app_state } from '../../appcontoller'
import { validate_email, validate_password } from '../../utils';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"


function SignUpForm(props) {

    const [formState, setState] = useState(false);
    const { rerender } = props
    let email_available_check_timeout = null;

    const custom_validation = () =>
        {
            document.getElementById('signUp_email').addEventListener('input', function() {
        
                if (validate_email(this.value))
                {
                    if (email_available_check_timeout !== null)
                        clearTimeout(email_available_check_timeout)

                    email_available_check_timeout = setTimeout(() => {
                        check_email_is_avalilable(this.value).then( (available) =>
                        {
                            if (available && validate_email(this.value))
                                this.setCustomValidity('');
                            else 
                                this.setCustomValidity('err');
                        })
                    }, 800)  
                } 
                else 
                    this.setCustomValidity('err');
            });

            document.getElementById('signUp_nickname').addEventListener('input', function() {
                this.setCustomValidity( this.value.length >= 2 ? '' : 'err' );
            });

            document.getElementById('signUp_password').addEventListener('input', function() {
                this.setCustomValidity( validate_password(this.value) ? '' : 'err' );
            });

            document.getElementById('signUp_password_confirm').addEventListener('input', function() {
                const res = document.getElementById('signUp_password').value === this.value;
                this.setCustomValidity( res ? '' : 'err' );
            });
        }

    const handleSubmit = (event) => 
        { 
            const form = event.currentTarget;
        
            if (form.checkValidity() === true) 
            {
                setState("signing_in");
        
                sign_up(
                    event.target.elements.signUp_email.value,
                    event.target.elements.signUp_nickname.value,
                    event.target.elements.signUp_password.value
                ).then( (result) =>
                {
                    if (result) 
                    {
                        set_app_state("registration-confirm")
                        rerender();
                    } else 
                    {
                        setState("server_error");
                    }
                })
            } else
                setState("validated");
        
            event.preventDefault();
            event.stopPropagation();
        };
    
    const go_to_authorization = () =>
        {
            set_app_state("authorization");
            rerender();
        }

    useEffect(custom_validation)

    return (
        <>
            <Form noValidate validated={formState === "validated"} onSubmit={handleSubmit}>

                <Form.Group as={Row} controlId="signUp_email">
                <Form.Label>Email</Form.Label>
                <Form.Control
                    required
                    type="email"
                    placeholder="example@email.com"
                    autoFocus={true}
                />
                <Form.Control.Feedback>Wonderful!</Form.Control.Feedback>
                <Form.Control.Feedback type="invalid">It's not email address or this address is already taken</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "15px"}}></Row>

                <Form.Group as={Row} controlId="signUp_nickname">
                <Form.Label>Nickname</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Casey"
                    required
                />
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                <Form.Control.Feedback type='invalid'>Is this really a nickname?</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "15px"}}></Row>

                <Form.Group as={Row} controlId="signUp_password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                    required
                    type="password"
                    placeholder="***********"
                />
                <Form.Control.Feedback>What a great password!</Form.Control.Feedback>
                <Form.Control.Feedback type='invalid'>From 8 to 32 characters</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "15px"}}></Row>

                <Form.Group as={Row} controlId="signUp_password_confirm">
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
                <Row>
                    
                    {
                        formState === "signing_in" ?
                        <Spinner animation="grow" />:
                        <Button type="submit">Sign Up</Button>
                    }
                    
                    <Row style={{height: "15px"}} ></Row>
                    
                    {
                        formState === "server_error" ?
                        <span className="text-danger">Sorry. Server error. Try later...</span>:
                        <></>
                    }
                    
                </Row>

                <Row style={{height: "25px"}}></Row>

            </Form>
            <Row>
                Already have an account? 
                <Row style={{height: "15px"}}></Row>
                <Button variant="outline-secondary" onClick={go_to_authorization}>Sign in!</Button>
                
            </Row>
        </>
    );
}

export default SignUpForm;