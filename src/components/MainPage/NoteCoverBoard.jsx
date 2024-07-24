import { useState, useCallback } from 'react';
import { get_notes_by_filter } from '../../backendapi';
import { set_app_state } from '../../appcontoller';

import { NoteCover } from './NoteCover';
import { Col, Row, Spinner } from 'react-bootstrap';


let note_list = []
let s_notes_label = null, s_notes_status = null


function NoteCoverBoard(props) {

  const [state, setState] = useState("idle");

  const {notes_label, notes_status} =
      localStorage.getItem("main_page_config") === null ? 
      { notes_label: "", notes_status: "active"} : 
      JSON.parse(localStorage.getItem("main_page_config"));

  const check_notes = (localStorage.getItem("note_edited") === null) ? "false" : localStorage.getItem("note_edited")
  if (check_notes === "true")
  {
    localStorage["note_edited"] = "false"
    setState("loading")
  }

  const onUpdateNoteStatus = () =>  { setState("loading") }

  const onOpenNote = (note_id) =>
  {
    localStorage["note_edit_id"] = note_id;
    set_app_state("note-edit");
    props.app_rerender();
  }

  if (s_notes_label !== notes_label || s_notes_status !== notes_status)
  {
    s_notes_label = notes_label;
    s_notes_status = notes_status;
    setState("loading")
  }

  


  if (state === "loading")
  {
    get_notes_by_filter(notes_label, notes_status)
    .then( (response) =>
    {
      note_list = response.map( (note) =>
        <Col xs={6} key={note.note_id} style={{padding: "10px"}}>
          <NoteCover 
            title={note.header || "..."}
            content={note.text || "..."}
            color={note.hex_color}
            note_status={note.status}
            note_id={note.note_id}

            update_note_status_callback={onUpdateNoteStatus}
            open_note_callback={onOpenNote}
          />
        </Col>
      );
      
      setState("idle")
    });
  }


  /*
    title, 
    content, 
    color, 
    note_status, // active, archived, deleted
    note_id, 

    onUpdateNoteStatus_callback,
    open_note_callback
*/


// States ^.^
/*  idle
    loading
    wating_note_response
*/

  return (
    <Row style={{padding: "10px"}}>
      {
        state === "loading" ? 
        <Spinner style={{margin: "25% 50%"}} animation='grow' /> :
        note_list
      }
    </Row>
  );
}

export { NoteCoverBoard }