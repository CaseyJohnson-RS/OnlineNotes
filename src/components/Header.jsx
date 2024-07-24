import { get_app_state, auth_states, special_states, set_app_state } from '../appcontoller'

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import SettingModal from './SettingsModal';

import { useState } from 'react';


function Header(props)
{
  const [settingsShow, setSettingsShow] = useState(false);
  const app_state = get_app_state();

  let profile_info = 
    localStorage.getItem("profile_info") !== null ? 
    JSON.parse(localStorage["profile_info"]) : 
    {
      id: 0,
      email: "",
      nickname: "",
      active: true,
      role: "user"
    }
  
  let label = "";
  let nickname = (profile_info.nickname.length <= 32 ? profile_info.nickname : "Profile");
  let admin = profile_info.role === "admin";
  let admin_btn = <></>;
  let settings_btn = <></>;
  let profile_btn = <></>;


  if (app_state !== "main-page")
  {
    profile_btn = 
    <Button variant="outline-primary" href='https://github.com/CaseyJohnson-RS/OnlineNotes' target='_blank'>
      <i className="bi bi-github"></i> Code of the project
    </Button>

    if (app_state === "note-edit")
      label = "Note editor"
    else if (app_state === "profile")
      label = "Profile"
    else
      label = "Online Notes"
  } 
  else if (app_state === "main-page")
  {
    const main_page_config = 
      localStorage.getItem("main_page_config") === null ? 
      { notes_label: "", notes_status: "active"} : 
      JSON.parse(localStorage.getItem("main_page_config"));
    
    if (main_page_config.notes_label.length > 0)
      label = main_page_config.notes_label;
    else if (main_page_config.notes_status.length > 0 && main_page_config.notes_status !== "active")
      label = "Notes " + main_page_config.notes_status;
    else label = "Online Notes";

    if (admin)
    {
      admin_btn = 
        <Button variant="outline-info" > 
          <i className="bi bi-person-fill-gear"></i>
        </Button>
    }
    settings_btn = 
      <Button variant="outline-secondary" onClick={() => setSettingsShow(true)}> 
        <i className="bi bi-gear-fill"></i>
      </Button>
    profile_btn = 
      <Button variant="outline-primary" onClick={() => 
        {
          set_app_state("profile");
          props.app_rerender();
        }
      }>
        { nickname }
      </Button>
  }


  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  return (<Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <SettingModal show={settingsShow} closeModal={ () => setSettingsShow(false) }/>

        <Navbar.Brand>
        <i className="bi bi-journal-bookmark-fill"></i>
          { " " + label }
        </Navbar.Brand>
        
        <Row>

          <Col xs="auto">
            { admin_btn }
          </Col>

          <Col xs="auto">
            { settings_btn }
          </Col>

          <Col xs="auto">
            { profile_btn }
          </Col>
          
        </Row>

      </Container>
    </Navbar>);
}

export { Header }