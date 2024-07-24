import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { ButtonGroup } from 'react-bootstrap';

function RestorePasswordModal(props) {
  
    const { closeModal, show } = props;

    const onChange = () => 
    {
        localStorage["token"] = null;
        localStorage["app_state"] = "restore-password";
        window.location.reload();
    }
    
    return (
    <>
        <Modal show={show}>
            <Modal.Header>
                Are you sure?
            </Modal.Header>
            <Modal.Body >
                
                <span>You will logout...</span>

                <ButtonGroup style={{width: "100%"}}>
                    <Button  variant="danger" onClick={onChange}>Change password</Button>
                    <Button variant="outline-secondary" onClick={ () => { closeModal(); } }>Close</Button>
                </ButtonGroup>

            </Modal.Body>

        </Modal>
    </>
    );
}

export default RestorePasswordModal;