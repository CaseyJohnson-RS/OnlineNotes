import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { ButtonGroup } from 'react-bootstrap';
import { delete_account } from '../../backendapi';

function DeleteAccountModal(props) {
  
    const { closeModal, show } = props;

    const onDelete = () => 
    {
        delete_account()
        .then( (res) =>
        {
            if (res)
            {
                localStorage.clear();
                window.location.reload();
            }
        });
        
    }
    
    return (
    <>
        <Modal show={show}>
            <Modal.Header>
                Are you sure? It will delete all notes.
            </Modal.Header>
            <Modal.Body >
                <ButtonGroup style={{width: "100%"}}>
                    <Button  variant="danger" onClick={onDelete}>Delete</Button>
                    <Button variant="outline-secondary" onClick={ () => { closeModal(); } }>Close</Button>
                </ButtonGroup>

            </Modal.Body>

        </Modal>
    </>
    );
}

export default DeleteAccountModal;