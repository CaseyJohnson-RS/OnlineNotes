import { useState, useCallback } from 'react';

import Container from 'react-bootstrap/Container';import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import SignInForm from '../components/Authorization/SignIn';
import SignUpForm from '../components/Authorization/SIgnUp';
import SignUpConfirm from '../components/Authorization/SignUpConfirm';
import RestorePassword from '../components/Authorization/RestorePassword';
import RestorePasswordConfirm from '../components/Authorization/RestorePasswordConfirm';


import { get_app_state, set_app_state } from '../appcontoller'


function Authorization(props)
{
    const [, updateState] = useState();
    const component_rerender = useCallback(() => updateState({}), []);
    const { parent_rerender } = props

    const app_state = get_app_state();

    let header;
    let body;

    if (app_state === "authorization")
    {
        header = "Sign In";
        body = <SignInForm rerender={component_rerender}/>
    } 
    else if (app_state === "registration")
    {
        header = "Sign Up";
        body = <SignUpForm rerender={component_rerender}/>
    }
    else if (app_state === "registration-confirm")
    {
        header = "Confirm";
        body = <SignUpConfirm rerender={component_rerender}/>
    }
    else if (app_state === "restore-password")
    {
        header = "Restore password"
        body = <RestorePassword rerender={component_rerender}/>
    }
    else if (app_state === "restore-password-confirm")
    {
        header = "Confirm"
        body = <RestorePasswordConfirm rerender={component_rerender} />
    }

    return (<main>
        <Container>
            <Row style={{height: "100px"}}></Row>
            <Row>
                <Col xs={1}></Col>
                <Col xs={4}>
                    <Row>
                        <h3>
                            { header }
                        </h3>
                    </Row>
                    { body }
                </Col>
                <Col xs={7}></Col>
            </Row>

        </Container>

    </main>);
}

export { Authorization }