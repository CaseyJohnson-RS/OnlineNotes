import { useEffect, useState } from 'react';
import { update_note } from '../../backendapi';

import { Row, Col, Spinner } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';



function NoteCover(props) {

    const { 
        title, 
        content, 
        color, 
        note_status, // active, archived, deleted
        note_id, 
        
        update_note_status_callback,
        open_note_callback
    } = props;
    

    const [noteState, setState] = useState("idle")
    const [updatingNoteStatus, setUNS] = useState(false)


    const onNoteHover = () => { setState("hover") }
    const onNoteOut = () => { setState("idle") }
    const onNoteClick = () => { open_note_callback(note_id) }

    useEffect( () => 
    {
        document.getElementById("note_" + note_id).
        addEventListener("mouseover", onNoteHover)

        document.getElementById("note_" + note_id).
        addEventListener("mouseout", onNoteOut)
    })

    const onUpdateNoteStatus = (note_id, status) =>
    {
        setUNS(true)
        update_note(note_id, {status: status})
        .then( (result) => 
            { 
                if (result) 
                    update_note_status_callback();
                else
                    setUNS(false)
            } 
        );
    }


    let buttons;

    if (updatingNoteStatus)
    {
        buttons = <Spinner animation='grow' />
    }
    else if (note_status === "active")
    {
        buttons = <>
            <Button variant="outline-success" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "archived") }}>
                <i className="bi bi-archive-fill"></i>
            </Button>
            <Button variant="outline-danger" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "deleted") }}>
                <i className="bi bi-trash-fill"></i>
            </Button>
        </>
    }
    else if (note_status === "deleted")
    {
        buttons = <>
            <Button variant="outline-success" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "archived") }}>
                <i className="bi bi-archive-fill"></i>
            </Button>
            <Button variant="outline-info" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "active") }}>
            <i className="bi bi-arrow-bar-up"></i>
            </Button>
        </>
    }
    else if (note_status === "archived")
    {
        buttons = <>
            <Button variant="outline-warning" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "active") }}>
            <i className="bi bi-arrow-bar-up"></i>
            </Button>
            <Button variant="outline-danger" size="sm" onClick={() => { onUpdateNoteStatus(note_id, "deleted") }}>
                <i className="bi bi-trash-fill"></i>
            </Button>
        </>
    }


    return (
        <Card style={{backgroundColor: color}} id={"note_" + note_id}>
            <Row>
                <Card.Body as={Col} onClick={onNoteClick} xs={9} style={{padding: "30px"}}> 

                    <Card.Title className='text-truncate'>
                        { title }
                    </Card.Title>

                    <Card.Text style={{height: "20px"}} className='text-truncate'>
                        { content }
                    </Card.Text>

                </Card.Body>
                <Col xs={3}>
                    <Row className='btn-group-vertical' style={{width: "100%", padding: "15%", height: "100%"}}>
                        { (noteState === "hover" || updatingNoteStatus) && buttons }
                    </Row>
                </Col>
            </Row>
            
        </Card>
    );
}

export { NoteCover };