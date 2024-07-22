import { useState, useEffect } from 'react';
import { sign_in } from '../../backendapi';
import { set_app_state } from '../../appcontoller'
import { validate_email, validate_password } from '../../utils';

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"


const custom_validation = () =>
{
    document.getElementById('signIn_email').addEventListener('input', function() {
        this.setCustomValidity( validate_email(this.value) ? '' : 'err' );
    });

    document.getElementById('signIn_password').addEventListener('input', function() {
        this.setCustomValidity( validate_password(this.value) ? '' : 'err' );
    });
}


function SignInForm(props) {

    const [formState, setState] = useState(false);
    const { rerender } = props

    const handleSubmit = (event) => 
        { 
            const form = event.currentTarget;
        
            if (form.checkValidity() === true) 
            {
                setState("signing_in");
        
                sign_in(
                    event.target.elements.signIn_email.value,
                    event.target.elements.signIn_password.value
                ).then( (result) =>
                {
                    if (result) 
                    {
                        set_app_state("main-page")
                        rerender();
                    } else 
                    {
                        setState("wrong_data");
                    }
                })
            } else
                setState("validated");
        
            event.preventDefault();
            event.stopPropagation();
        };
    
    const go_to_registration = () =>
        {
            set_app_state("registration");
            rerender();
        }

    useEffect(custom_validation)

    return (
        <>
            <Form noValidate validated={formState === "validated"} onSubmit={handleSubmit}>

                <Form.Group as={Row} controlId="signIn_email">
                <Form.Label>Email</Form.Label>
                <Form.Control
                    required
                    type="email"
                    placeholder="example@email.com"
                />
                <Form.Control.Feedback type='invalid'>Forgot your email?..</Form.Control.Feedback>
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "15px"}}></Row>

                <Form.Group as={Row} controlId="signIn_password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                    required
                    type="password"
                    placeholder="***********"
                />
                <Form.Control.Feedback type='invalid'>I don't think this is your password...</Form.Control.Feedback>
                <Form.Control.Feedback>Looks perfect!</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "25px"}}></Row>

                <Row style={{display: formState !== "signing_in" ? "block" : "none"}}>
                    <Button type="submit">Sign in</Button>
                    <Row style={{height: "25px"}}></Row>
                    <Button variant="outline-danger">I forgot password</Button>
                </Row>
                <Row style={{display: formState === "signing_in" ? "block" : "none"}}>
                    <Spinner animation="grow" />
                </Row>

                <Row style={{height: "25px"}}></Row>

                <Row className='text-danger'>
                    {  
                        formState === "wrong_data" ?
                        "Wrong username or password...":
                        <></>
                    }
                </Row>

                <Row style={{height: "25px"}}></Row>

            </Form>
            <Row>
                Already have an account? 
                <Row style={{height: "15px"}}></Row>
                <Button variant="outline-secondary" onClick={go_to_registration}>Sign up!</Button>
            </Row>
        </>
    );
}

export default SignInForm;