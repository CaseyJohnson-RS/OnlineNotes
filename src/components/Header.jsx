import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';


function Header(props)
{
  let { 
    label="",
    state="authorization",
    nickname="Test nickname",
    admin=false,

    admin_btn_callback=null,
    settings_btn_callback=null,
    profile_btn_callback=null
  } = props

  nickname = (nickname.length <= 32 ? nickname : "Profile")
  label = (label.length === 0 ? <><i className="bi bi-journal-bookmark-fill"></i> Online Notes </> : label)

  let admin_btn = <></>
  let settings_btn = <></>
  let profile_btn = <></>

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  if (state === "authorization" || state === "server-error")
  {
    profile_btn = 
      <Button variant="outline-primary" href='https://github.com/CaseyJohnson-RS/OnlineNotes' target='_blank'>
        <i className="bi bi-github"></i> Code of the project
      </Button>
  } 
  else if (state === "main-page")
  {
    if (admin)
    {
      admin_btn = 
        <Button variant="outline-info" onClick={admin_btn_callback}> 
          <i class="bi bi-person-fill-gear"></i>
        </Button>
    }
    settings_btn = 
      <Button variant="outline-secondary" onClick={settings_btn_callback}> 
        <i class="bi bi-gear-fill"></i>
      </Button>
    profile_btn = 
      <Button variant="outline-primary" onClick={profile_btn_callback}>
        { nickname }
      </Button>
  }

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  return (<Navbar expand="lg" className="bg-body-tertiary">
      <Container>

        <Navbar.Brand>
          { label }
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