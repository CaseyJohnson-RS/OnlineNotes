import { useState, useEffect } from 'react';
import { restore_password } from '../../backendapi';
import { set_app_state } from '../../appcontoller'
import { validate_email } from '../../utils';

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Spinner from "react-bootstrap/Spinner"


function RestorePassword(props) {

    const [formState, setState] = useState(false);
    const { rerender } = props

    const custom_validation = () =>
        {
            document.getElementById('restore_pass_email').addEventListener('input', function() {
                this.setCustomValidity( validate_email(this.value) ? '' : 'err' );
            }); 
        }

    const handleSubmit = (event) => 
        { 
            setState("restoring")

            const form = event.currentTarget;
            
            if (form.checkValidity() === true) 
            {
                restore_password(event.target.restore_pass_email.value).then( (result) => 
                    {
                        if (result)
                            set_app_state("restore-password-confirm");
                        else
                            setState("error")

                        rerender();
                    }
                );
            } else
                setState("validated")

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

                <Form.Group as={Row} controlId="restore_pass_email">
                <Form.Label>Email</Form.Label>
                <Form.Control
                    required
                    type="email"
                    placeholder="example@email.com"
                    autoFocus={true}
                />
                <Form.Control.Feedback type='invalid'>Forgot your email?..</Form.Control.Feedback>
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>
                
                <Row style={{height: "25px"}}></Row>

                {
                    formState === "error" ?
                    <>
                        Sometihng went wrong... Sorry...
                        <Row style={{height: "25px"}}></Row>
                    </> : <></>
                }
                
                <Row>
                    <Button type="submit" style={{display: formState !== "restoring" ? "block" : "none"}}>Restore</Button>

                    <Row style={{display: formState === "restoring" ? "flex" : "none"}}>
                        <Col xs={11}>
                            <h4>Cheking...</h4>
                        </Col>
                        <Col xs={1}>
                            <Spinner animation="grow" />
                        </Col>
                    </Row>
                </Row>

            </Form>

            {/* <Row style={{height: "25px", display: formState === "checking" ? "block" : "none"}}></Row>
            <Row style={{display: formState === "checking" ? "block" : "none"}}>
                
                <Col xs={10}><h4>Checking...</h4></Col>
                <Col xs={2}><Spinner animation="grow" /></Col>
                
            </Row>

            <Row style={{height: "25px", display: formState === "confirmed" ? "block" : "none"}}></Row>
            <Row style={{display: formState === "confirmed" ? "block" : "none"}}>
                
                <Col xs={10}><h4 className='text-success'>Successful!</h4></Col>
                
            </Row>  */}

            <Row style={{height: "25px"}}></Row>

            <Row style={{display: formState === "restoring" ? "none" : "flex"}}>
                <Button variant="outline-secondary" onClick={go_to_authorization}>Back</Button>
            </Row>
        </>
    );
}
/*

*/

export default RestorePassword;