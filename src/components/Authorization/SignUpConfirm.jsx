import { useState, useEffect } from 'react';
import { sign_up_confirm } from '../../backendapi';
import { set_app_state } from '../../appcontoller'

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"


function SignUpConfirm(props) {

    const [formState, setState] = useState(false);
    const { rerender } = props

    const valid_numbers = () =>
        {
            document.getElementById('confirm_code').addEventListener('input', function() {
                if (!/^\d+$/.test(this.value.slice(-1)))
                    this.value = this.value.substring(0,-1)

                if(this.value.length === 6)
                    setState("valid")
                else
                    setState("invalid")
            });   
        }

    const handleSubmit = (event) => 
        { 
            setState("checking")
            sign_up_confirm(event.target.confirm_code.value).then( (result) =>
                {
                    if (result)
                    {
                        setState("confirmed")
                        rerender();

                        setTimeout( () =>
                        {
                            set_app_state("main-page");
                            rerender();
                        }, 3000)
                    } else 
                    {
                        event.target.confirm_code.setCustomValidity('err')
                        setState("wrong_code")
                    }
                }
            )
        
            event.preventDefault();
            event.stopPropagation();
        };
    
    const go_to_registration = () =>
        {
            set_app_state("registration");
            rerender();
        }

    useEffect(valid_numbers)

    return (
        <> 
            <Form 
                noValidate 
                validated={formState === "wrong_code"} 
                onSubmit={handleSubmit}
                style={{display: ["checking", "confirmed"].includes(formState) ? "none" : "block"}}
            >

                <Form.Group as={Row} controlId="confirm_code">
                <Form.Label>We have sent the code to your email</Form.Label>
                <Form.Control
                    required
                    type="text"
                    placeholder="123456"
                    size='lg'
                    className='text-center'
                    style={{fontSize: "30px"}}
                    maxLength={6}
                    autoFocus={true}
                />
                <Form.Control.Feedback type='invalid'>Wrong code. Try again...</Form.Control.Feedback>
                </Form.Group>
                
                <Row style={{height: "25px"}}></Row>

                <Row>
                    {
                        formState === "signing_in" ?
                        <Spinner animation="grow" />:
                        <Button type="submit" disabled={ formState !== "valid" } >Confirm</Button>
                    }
                </Row>

            </Form>

            <Row style={{height: "25px", display: formState === "checking" ? "block" : "none"}}></Row>
            <Row style={{display: formState === "checking" ? "block" : "none"}}>
                
                <Col xs={10}><h4>Checking...</h4></Col>
                <Col xs={2}><Spinner animation="grow" /></Col>
                
            </Row>

            <Row style={{height: "25px", display: formState === "confirmed" ? "block" : "none"}}></Row>
            <Row style={{display: formState === "confirmed" ? "block" : "none"}}>
                
                <Col xs={10}><h4 className='text-success'>Successful!</h4></Col>
                
            </Row> 

            <Row style={{height: "25px"}}></Row>

            <Row style={{display: formState === "confirmed" ? "none" : "block"}}>
                <Button variant="outline-secondary" onClick={go_to_registration}>Back</Button>
            </Row>
        </>
    );
}
/*

*/

export default SignUpConfirm;