import { useState, useCallback, useEffect } from 'react';
import { set_label, unset_label, get_user_labels, get_note, update_note } from '../backendapi';

import { Row, Col, Form, Button, ButtonGroup, Spinner } from 'react-bootstrap';
import { set_app_state } from '../appcontoller';


let user_labels = [];
let note_data = null;


function Label(props)
{
    const [, updateState] = useState();
    const rerender = useCallback(() => updateState({}), []);

    const { label, note_id } = props;

    const choosen = note_data.labels.includes(label);

    const onClick = () => 
    {
        if (choosen)
        {
            note_data.labels.splice(note_data.labels.indexOf(label), 1);
            unset_label(note_id,label)
            .then( (result) =>
            {
                if (!result)
                {
                    note_data.labels.push(label);
                    rerender();
                }
            });
            rerender();
        } 
        else
        {
            note_data.labels.push(label)
            set_label(note_id,label)
            .then( (result) =>
            {
                if (!result)
                {
                    note_data.labels.splice(note_data.labels.indexOf(label), 1);
                    rerender();
                }
            })
            rerender();
        }        
    }

    return (
        <>
        <Row style={{padding: "10px 20px"}} ></Row>
        <Button 
            className="text-start" 
            variant={ (choosen ? "" : "outline-") + "secondary" }
            onClick={ onClick }
            style={{width: "100%"}}
        >
            <i className="bi bi-tag-fill"></i>
            <span>
                { " " + label }
            </span>
        </Button>
        </>
        
    )
}


function NoteEditor(props) {

    const [state, setState] = useState("loading");
    const note_id = localStorage["note_edit_id"];

    const custom_validation = () =>
    {
        document.getElementById('noteEdit_header').addEventListener('input', function() {
            setState("unsaved")
        });
        document.getElementById('noteEdit_text').addEventListener('input', function() {
            setState("unsaved")
        });
    }
    useEffect(custom_validation);

    const onSave = () =>
    {
        setState("saving");

        const header = document.getElementById('noteEdit_header').value;
        const text = document.getElementById('noteEdit_text').value;

        update_note(note_id, {header: header, text: text, status: note_data.status})
        .then( (res) =>
        {
            if (res)
                setState("saved")
            else
                setState("error")
        })
    }

    if (state === "loading")
    {
        get_user_labels()
        .then( (result) =>
        {
            if (!result)
                setState("error")
            else
            {
                user_labels = result;
                get_note(note_id)
                .then( (res) =>
                {
                    if (res === null)
                        setState("error")
                    else
                    {
                        note_data = res;
                        setState("saved");
                        console.log(note_data);
                    }
                })
            }
        })
    }

    const loading = state === "loading"
    const error = state === "error"
    const saving = state === "saving"
    const saved = state === "saved"

    return (
    <>
        <Row style={{height: "20px"}} />
        <Row>
        <Col xs={9}>
        <Form>
            <Form.Group className="mb-3" controlId="noteEdit_header">
                <Form.Control 
                    type="text" 
                    placeholder={loading ? "Loading..." : "Header"} 
                    size='lg' 
                    disabled={loading || error || saving}
                    defaultValue={ (loading || error) ? "" : note_data.header}
                    maxLength={128}
                />
            </Form.Group>
            <Form.Group className="mb-3" controlId="noteEdit_text">
                <Form.Control 
                    as="textarea" 
                    rows={3} 
                    placeholder={loading ? "Loading..." : (error ? "Something went wrong..." : "Your thoughts...") } 
                    size='lg' 
                    style={{ height: '500px', resize: "none" }}
                    disabled={loading || error || saving}
                    defaultValue={ (loading || error) ? "" : note_data.text}
                    maxLength={20000}
                />
            </Form.Group>
            {
                saving ?
                <Spinner animation='grow' /> :
                <ButtonGroup >
                    <Button onClick={onSave} disabled={loading || error || saved}>
                        Save changes
                    </Button>
                    <Button 
                        variant='outline-secondary' 
                        disabled={!saved}
                        onClick={() => { 
                            localStorage["note_edited"] = true;
                            set_app_state("main-page"); 
                            props.app_rerender();
                        }}
                        >
                        Cancel
                    </Button>
                </ButtonGroup>
            }
            
        </Form>
        </Col>
        <Col xs={3}>
            {
                (loading || error) ?
                <Spinner animation='grow' style={{margin: "50%"}}/> :
                user_labels.map( (label) =>
                    <Label 
                        key={label}
                        label={label}
                        note_id={note_id}
                    />
                )
            }
        </Col>
        </Row>
    </>
    );
}

export { NoteEditor }