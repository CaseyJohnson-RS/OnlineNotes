import Spinner from "react-bootstrap/Spinner"
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export function Loader()
{
    return (
    <Container>
    <Row  style={{height: "250px"}}></Row>
      <Row  style={{height: "550px"}}>
        <Col/>
        <Col xs={8}>
            <h3 className="fade-in">Loading...</h3>
        </Col>
        <Col><Spinner animation="grow" /></Col>
        <Col/>
      </Row>
    </Container>)
}