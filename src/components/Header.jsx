import { get_app_state, auth_states, special_states } from '../appcontoller'

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';


function Header(props)
{
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
  
  console.log("Profile info:");
  console.log(profile_info);
  let label = "";
  let nickname = (profile_info.nickname.length <= 32 ? profile_info.nickname : "Profile");
  let admin = profile_info.role === "admin";
  let admin_btn = <></>;
  let settings_btn = <></>;
  let profile_btn = <></>;


  if (auth_states.includes(app_state) || special_states.includes(app_state))
  {
    profile_btn = 
    <Button variant="outline-primary" href='https://github.com/CaseyJohnson-RS/OnlineNotes' target='_blank'>
      <i className="bi bi-github"></i> Code of the project
    </Button>
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
      <Button variant="outline-secondary" > 
        <i className="bi bi-gear-fill"></i>
      </Button>
    profile_btn = 
      <Button variant="outline-primary" >
        { nickname }
      </Button>
  }

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  return (<Navbar expand="lg" className="bg-body-tertiary">
      <Container>

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