import { useState } from 'react';
import { Row, Col, Button } from 'react-bootstrap';

import EditNicknameModal from '../components/Profile/EditNicknameModal';
import RestorePasswordModal from '../components/Profile/RestorePasswordModal';
import DeleteAccountModal from '../components/Profile/DeleteAccountModal';

import { set_app_state } from '../appcontoller';


function Profile(props) {

    const [state, setState] = useState("idle")
    const [editNicknameActive, setEditNicknameActive] = useState(false);
    const [changePassActive, setChangePassActive] = useState(false);
    const [deleteAccountActive, setDeleteAccountActive] = useState(false);

    let profileInfo = localStorage.getItem("profile_info")

    if (profileInfo === null)
        setState("error");
    else
        profileInfo = JSON.parse(profileInfo)

    let nickname = profileInfo.nickname;
    const user_id = profileInfo.id;
    const email = profileInfo.email;

    const onSetNickname = (nick) =>
    {
        profileInfo.nickname = nick;
        localStorage["profile_info"] = JSON.stringify(profileInfo)
        setEditNicknameActive(false)
    }

    return (
        <>  
            <EditNicknameModal 
                show={editNicknameActive} 
                closeModal={() => setEditNicknameActive(false)}
                user_id={user_id}
                setNicknameCallback = {onSetNickname}
            />
            <RestorePasswordModal show={changePassActive} closeModal={() => setChangePassActive(false)}/>
            <DeleteAccountModal show={deleteAccountActive} closeModal={() => setDeleteAccountActive(false)}/>
            <Col xs={6}>
                <Row style={{height: "30px"}}/>
                
                <Row>
                    <Col xs={8}>
                        <span style={{opacity: "75%"}}>{email}</span>
                    </Col>
                </Row>

                <Row style={{height: "30px"}}/>

                <Row>
                    <Col xs={8}>
                        <h3>{nickname}</h3>
                    </Col>
                    <Col xs={4}>
                        <Button style={{width: "100%"}} onClick={() => setEditNicknameActive(true)}>Edit nickname</Button>
                    </Col>
                </Row>

                <Row style={{height: "30px"}}/>

                <Row>
                    <Col xs={8}>
                        <h3>***********</h3>
                    </Col>
                    <Col xs={4}>
                        <Button style={{width: "100%"}} onClick={() => setChangePassActive(true)}>Change password</Button>
                    </Col>
                </Row>

                <Row style={{height: "30px"}}/>
                <Row>
                    <Col xs={3}>
                        <Button variant='outline-warning' style={{width: "100%"}} onClick={ () => { localStorage["token"] = null; window.location.reload(); }}>Logout</Button>
                    </Col>
                    <Col xs={5}/>
                    <Col xs={4}>
                        <Button variant='outline-secondary' style={{width: "100%"}} onClick={ () => { set_app_state("main-page"); props.app_rerender(); }}>Back</Button>
                    </Col>
                </Row>

                <Row style={{height: "320px"}}/>

                <hr/>
                <Row>
                    <Col xs={3}>
                        <Button variant='outline-danger' onClick={() => setDeleteAccountActive(true)}>Delete account</Button>
                    </Col>
                </Row>
            </Col>
            
        </>
    );
}

export { Profile }