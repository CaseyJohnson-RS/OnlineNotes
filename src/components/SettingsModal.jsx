import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';


function SettingModal(props) {
  
    const { closeModal, show } = props;

    const onSwitchDarkTheme = () => 
    {
        const value = document.getElementById("darkTheme_switch").checked;

        console.log(value);

        localStorage["app_theme"] = value ? "dark" : "light";

        document.getElementById("main-body").setAttribute("data-bs-theme",localStorage["app_theme"])
    }


    return (
    <>
        <Modal show={show}>
            <Modal.Body>
                
                <Form >
                    <Form.Check 
                        type="switch"
                        id="darkTheme_switch"
                        label="Dark theme"
                        defaultChecked={localStorage["app_theme"] === "dark"}
                        onClick={onSwitchDarkTheme}
                        size="lg"
                    />
                    <br />

                    <Button style={{width: "100%"}} variant="outline-secondary" onClick={closeModal}>Close</Button>

                </Form>
           
            </Modal.Body>
        </Modal>
    </>
    );
}

export default SettingModal;