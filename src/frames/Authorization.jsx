import { useState, useCallback } from 'react';

import Container from 'react-bootstrap/Container';import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import SignInForm from '../components/Authorization/SignIn';
import SignUpForm from '../components/Authorization/SIgnUp';
import SignUpConfirm from '../components/Authorization/SignUpConfirm';


import { get_app_state, set_app_state } from '../appcontoller'


function Authorization()
{
    const [, updateState] = useState();
    const rerender = useCallback(() => updateState({}), []);

    const app_state = get_app_state();

    let header;
    let body;

    if (app_state === "authorization")
    {
        header = "Sign In";
        body = <SignInForm rerender={rerender}/>
    } 
    else if (app_state === "registration")
    {
        header = "Sign Up";
        body = <SignUpForm rerender={rerender}/>
    }
    else if (app_state === "registration-confirm")
    {
        header = "Confirm";
        body = <SignUpConfirm rerender={rerender}/>
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