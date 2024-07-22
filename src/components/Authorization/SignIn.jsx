import { useState } from 'react';
import { sign_in } from '../../backendapi';
import { set_app_state } from '../../appcontoller'

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"

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
                <Form.Control.Feedback>Looks perfect!</Form.Control.Feedback>
                </Form.Group>

                <Row style={{height: "25px"}}></Row>
                <Row>
                    <Col xs={4}>
                    {
                        formState === "signing_in" ?
                        <Spinner animation="grow" />:
                        <Button type="submit">Sign in</Button>
                    }
                        
                    </Col>
                    <Col xs={8}>
                    {
                        formState === "wrong_data" ?
                        "Wrong username or password...":
                        <></>
                    }
                    </Col>
                </Row>

                <Row style={{height: "50px"}}></Row>

            </Form>
            <Row>
                Don't have an account? 
                <Row style={{height: "15px"}}></Row>
                <Row>
                    <Col xs={6}>
                        <Button variant="outline-secondary" onClick={go_to_registration}>Sign up!</Button>
                    </Col>
                </Row>
                
            </Row>
        </>
    );
}

export default SignInForm;