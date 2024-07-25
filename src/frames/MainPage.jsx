import { useState, useCallback } from 'react';

import { Row, Col, Button, Spinner } from 'react-bootstrap';

import { LabelChooser } from '../components/MainPage/LabelChooser';
import { NoteCoverBoard } from '../components/MainPage/NoteCoverBoard';
import { create_note } from '../backendapi';
import { set_app_state } from '../appcontoller';


function MainPage(props) {

  const [createNoteState, setCreateNoteState] = useState("idle")

  const onCreateNote = () => 
  {
    setCreateNoteState("loading");

    create_note()
    .then( (resp) =>
    {
      console.log(resp);
      if (resp === null)
        return;
      else
      {
        localStorage["note_edit_id"] = resp;
        set_app_state("note-edit");
        props.app_rerender();
      }

      setCreateNoteState("idle")
    })
  }

  return (
    <>
    
      <Row>
        <Col xs={3}>
          <LabelChooser app_rerender={props.app_rerender}/>
        </Col>
        <Col xs={9}>
        <Row style={{padding: "10px"}}>
          <Col>
          {
            createNoteState === "loading" ?
            <Spinner animation='grow' /> :
            <Button variant='success' onClick={onCreateNote}>New note</Button>
          }
          
          </Col>
        </Row>
        <Row>
          <NoteCoverBoard app_rerender={props.app_rerender}/>
        </Row>
        </Col>
      </Row>
    </>
  );
}

export { MainPage }